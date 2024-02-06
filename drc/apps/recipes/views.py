from rest_framework import mixins, status, viewsets, generics, views, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from drc.apps.core.permissions import IsOwnerOrReadOnly

from . import models, serializers, renderers
from drc.apps.core.mixins import MultipleFieldLookupMixin
from drc.apps.likes import models as like_models
from drc.apps.cooked import models as cooked_models

#from silk.profiling.profiler import silk_profile

from django.db.models import Count

#from src.apps.core.decorators import cache_per_user
#from django.utils.decorators import method_decorator

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.RecipeJSONRenderer,)
    lookup_field = 'slug'
    queryset = models.Recipe.objects \
        .select_related('author','author__user') \
        .prefetch_related('instructions','instructions__instruction_ingredient','items','items__ingredients') \
        .only('id','slug','title','description','total_time','servings','cuisine','created_at','updated_at',
            'author__id','author__user__username') \
        .all()

#    @silk_profile(name='get_queryset')
    def get_queryset(self):

        queryset = models.Recipe.objects \
            .select_related('author','author__user') \
            .prefetch_related('recipe_image') \
            .only('id','title','slug','total_time','slug','author__id','author__user__username') \
            .all()


        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__username=author)

        cuisine = self.request.query_params.get('cuisine', None)
        if cuisine is not None:
            queryset = queryset.filter(cuisine__iexact=cuisine)

        liked = self.request.query_params.get('liked', None)
        if liked is not None:
            queryset = queryset.filter(like__user__user__username=liked)

        cooked = self.request.query_params.get('cooked', None)
        if cooked is not None:
            queryset = queryset.filter(cooked_recipe__user__user__username=cooked)

        return queryset

    def create(self, request):

        context = {
            'author': self.request.user.profile,
            'request': request
        }

        serializer_data = request.data.get('recipe', {})

        serializer = self.serializer_class(
            data=serializer_data,
            context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

#    @silk_profile(name='retrieve')
#    @method_decorator(cache_per_user(60*5))
    def retrieve(self, request, slug=None):
        print('request', request)

        context = {
            'request': request
        }

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, slug):

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except models.Recipe.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('recipe', {})

        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

#    @method_decorator(cache_per_user(60*5))
    def list(self, request):

        likes = {}
        recipes = models.Recipe.objects.annotate(like_count=Count('like__id')).values_list('id', 'like_count')

        for recipe_id, like_count in recipes:
            likes[recipe_id] = like_count

        context = {
            'request': request,
            'likes': likes,
        }
        
        queryset = self.get_queryset()
        serializer = serializers.ShortRecipeSerializer(
            queryset,
            many=True,
            context=context
        )
        return Response(serializer.data)


class RecipeImageCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.RecipeImageSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.RecipeImageJSONRenderer,)

    
    def post(self, request, recipe_slug=None):

        context = {
            'author': self.request.user
        }

        try:
            context['recipe'] = models.Recipe.objects.get(slug=recipe_slug)
        except models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        serializer = self.serializer_class(
            data=request.data,
            context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class RecipeImageRetrieveUpdateDestroyAPIView(MultipleFieldLookupMixin,
    generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RecipeImageSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.RecipeImageJSONRenderer,)

    def get_object(self):
        recipe_slug = self.kwargs['recipe_slug']
        photo_id = self.kwargs['photo_id']

        try:
            queryset = models.RecipeImage.objects.get(id=photo_id, recipe__slug=recipe_slug)
        except models.RecipeImage.DoesNotExist:
            raise NotFound('An image with this slug does not exist.')

        return queryset

class InstructionIngredientListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.InstructionIngredientSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.InstructionIngredientJSONRenderer,)
    lookup_field = 'instruction__id'
    lookup_url_kwarg = 'instruction_id'
    queryset = models.InstructionIngredient.objects.all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)
    
    def create(self, request, recipe_slug=None, instruction_id=None):

        context = {
            'author': self.request.user.profile,
        }

        serializer_data = request.data.get('instruction_ingredient', {})

        try:
            context['instruction'] = models.Instruction.objects.get(id=instruction_id)
        except models.Instruction.DoesNotExist:
            raise NotFound('An instruction with this ID does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstructionIngredientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.InstructionIngredientSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.InstructionIngredientJSONRenderer,)

    def get_object(self):
        instruction_id = self.kwargs['instruction_id']
        instruction_ingredient_id = self.kwargs['instruction_ingredient_id']

        try:
            queryset = models.InstructionIngredient.objects.get(id=instruction_ingredient_id, instruction=instruction_id)
        except models.InstructionIngredient.DoesNotExist:
            raise NotFound('An ingredient tied to this instruction does not exist.')

        return queryset

class InstructionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.InstructionSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.InstructionJSONRenderer,)
    lookup_field = 'recipe__slug'
    lookup_url_kwarg = 'recipe_slug'
    queryset = models.Instruction.objects.prefetch_related('instruction_ingredient').all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, recipe_slug=None):

        context = {
            'author': self.request.user
        }

        serializer_data = request.data.get('instruction', {})

        try:
            context['recipe'] = models.Recipe.objects.get(slug=recipe_slug)
        except models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstructionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.InstructionSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.InstructionJSONRenderer,)
    
    def get_object(self):
        recipe_slug = self.kwargs['recipe_slug']
        instruction_id = self.kwargs['instruction_id']

        try:
            queryset = models.Instruction.objects.get(id=instruction_id, recipe__slug=recipe_slug)
        except models.Instruction.DoesNotExist:
            raise NotFound('An instruction step with this slug does not exist.')
        return queryset

# class InstructionImageCreateAPIView(generics.CreateAPIView):
#     serializer_class = serializers.InstructionImageSerializer
#     permission_classes = (AllowAny,)
    
#     def post(self, request, recipe_slug=None, instruction_id=None):

#         context = {
#             'author': self.request.user
#         }

#         try:
#             context['instruction'] = models.Instruction.objects.get(id=instruction_id)
#         except models.Instruction.DoesNotExist:
#             raise NotFound('An instruction tied to this recipe does not exist.')

#         serializer = self.serializer_class(
#             data=request.data,
#             context=context
#         )

#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data,status=status.HTTP_201_CREATED)


# class InstructionImageRetrieveUpdateDestroyAPIView(MultipleFieldLookupMixin,
#     generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.InstructionImageSerializer
#     permission_classes = (AllowAny,)
#     renderer_classes = (renderers.InstructionImageJSONRenderer,)

#     def get_object(self):
#         instruction_id = self.kwargs['instruction_id']
#         photo_id = self.kwargs['photo_id']

#         try:
#             instruction = models.Instruction.objects.get(id=instruction_id)
#             queryset = models.InstructionImage.objects.get(id=photo_id, instruction=instruction)
#         except models.InstructionImage.DoesNotExist:
#             raise NotFound('An image with tied to this instruction does not exist.')

#         return queryset


class ItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ItemSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.ItemJSONRenderer,)
    lookup_field = 'recipe__slug'
    lookup_url_kwarg = 'recipe_slug'
    queryset = models.Item.objects.prefetch_related('ingredients').all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, recipe_slug=None):

        context = {
            'author': self.request.user
        }

        serializer_data = request.data.get('item', {})

        try:
            context['recipe'] = models.Recipe.objects.get(slug=recipe_slug)
        except models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ItemSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.ItemJSONRenderer,)
    
    def get_object(self):
        recipe_slug = self.kwargs['recipe_slug']
        item_id = self.kwargs['item_id']

        try:
            queryset = models.Item.objects.get(id=item_id, recipe__slug=recipe_slug)
        except models.Item.DoesNotExist:
            raise NotFound('An item tied to this slug does not exist.')

        return queryset


class IngredientListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.IngredientJSONRenderer,)
    lookup_field = 'item__id'
    lookup_url_kwarg = 'item_id'
    queryset = models.Ingredient.objects.all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, recipe_slug=None, item_id=None):

        context = {
            'author': self.request.user.profile
        }

        serializer_data = request.data.get('ingredient', {})

        try:
            context['item'] = models.Item.objects.get(id=item_id)
        except models.Item.DoesNotExist:
            raise NotFound('A item with this id does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IngredientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.IngredientJSONRenderer,)
    
    def get_object(self):
        item_id = self.kwargs['item_id']
        ingredient_id = self.kwargs['ingredient_id']

        try:
            queryset = models.Ingredient.objects.get(id=ingredient_id, item__id=item_id)
        except models.Ingredient.DoesNotExist:
            raise NotFound('An ingredient tied to this item does not exist.')

        return queryset

class RecipeFeedListAPIView(generics.ListAPIView):
    serializer_class = serializers.ShortRecipeSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.RecipeJSONRenderer,)

    def get_queryset(self):
        user = self.request.user

        following = user.profile.follow.all()

        # authored recipes from people I follow
        created_recipes = models.Recipe.objects.all().filter(author__in=following)

        # liked recipes from people I follow
        following_likes = like_models.Like.objects.all().filter(user_id__in=following)
        liked_recipes = models.Recipe.objects.all().filter(like__in=following_likes)

        # cooked recipes from people I follow
        cooked_recipes = cooked_models.CookedRecipe.objects.all().filter(user_id__in=following)
        cooked_recipes = models.Recipe.objects.all().filter(cooked_recipe__in=cooked_recipes)

        # union of individual results
        queryset = created_recipes | liked_recipes | cooked_recipes
        return queryset.distinct()


class SearchListAPIView(generics.ListAPIView):
    serializer_class = serializers.RecipeSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.RecipeJSONRenderer,)
    queryset = models.Recipe.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','cuisine','description','items__name']
