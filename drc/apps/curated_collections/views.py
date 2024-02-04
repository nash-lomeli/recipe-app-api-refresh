from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import models, serializers, renderers

from drc.apps.recipes import models as recipe_models
#from silk.profiling.profiler import silk_profile
from django.db.models import Count

#from src.apps.core.decorators import cache_per_user
#from django.utils.decorators import method_decorator

class CuratedCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CuratedCollectionSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.CuratedCollectionJSONRenderer,)
    lookup_field = 'id'
    queryset = models.CuratedCollection.objects. \
            prefetch_related('collection_recipe','collection_recipe__recipe'#,'collection_recipe__recipe__recipe_image'
                ,'collection_recipe__recipe__author','collection_recipe__recipe__author__user',
                ).all()

    def create(self, request):

        context = {
            'request': request
        }

        serializer_data = request.data.get('curated_collection', {})

        serializer = self.serializer_class(
            data=serializer_data,
            context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, id=None):

        likes = {}
        recipes = recipe_models.Recipe.objects.filter(id__in=(models.CollectionRecipe.objects.all().values_list('recipe_id'))).annotate(like_count=Count('like__id')).values_list('id', 'like_count')

        for recipe_id, like_count in recipes:
            likes[recipe_id] = like_count

        context = {
            'request': request,
            'likes': likes,
        }

        try:
            serializer_instance = self.queryset.get(id=id)
        except models.CuratedCollection.DoesNotExist:
            raise NotFound('A collection with this ID does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=context,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, id):

        try:
            serializer_instance = self.queryset.get(id=id)
        except models.CuratedCollection.DoesNotExist:
            raise NotFound('A collection with this ID does not exist.')

        serializer_data = request.data.get('curated_collection', {})

        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

#    @silk_profile(name='CuratedCollectionViewSet-List')
#    @method_decorator(cache_per_user(60*5))
    def list(self, request):

        likes = {}
        recipes = recipe_models.Recipe.objects.filter(id__in=(models.CollectionRecipe.objects.all().values_list('recipe_id'))).annotate(like_count=Count('like__id')).values_list('id', 'like_count')

        for recipe_id, like_count in recipes:
            likes[recipe_id] = like_count

        context = {
            'request': request,
            'likes': likes,
        }

        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset,
            many=True,
            context=context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionRecipeCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CollectionRecipeSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.CollectionRecipeJSONRenderer,)

    def create(self, request, curated_collection_id=None, recipe_slug=None):

        context = {
            'request': request
        }

        serializer_data = request.data.get('collection_recipe', {})

        try:
            context['recipe'] = recipe_models.Recipe.objects.get(slug=recipe_slug)
        except recipe_models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        try:
            context['curated_collection'] = models.CuratedCollection.objects.get(id=curated_collection_id)
        except models.CuratedCollection.DoesNotExist:
            raise NotFound('A collection with this id does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionRecipeListAPIView(generics.ListAPIView):
    serializer_class = serializers.CollectionRecipeSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.CollectionRecipeJSONRenderer,)
    lookup_field = 'curatedCollection__id'
    lookup_url_kwarg = 'curated_collection_id'
    queryset = models.CollectionRecipe.objects.prefetch_related('recipe','recipe__recipe_image'
                ,'recipe__author','recipe__author__user',
                ).select_related('recipe__author','recipe__author__user',).all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)


class CollectionRecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CollectionRecipeSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.CollectionRecipeJSONRenderer,)

    def get_object(self):
        curated_collection_id = self.kwargs['curated_collection_id']
        collection_recipe_id = self.kwargs['collection_recipe_id']

        try:
            queryset = models.CollectionRecipe.objects.prefetch_related('recipe','recipe__recipe_image'
                ,'recipe__author','recipe__author__user',
                ).select_related('recipe__author','recipe__author__user',).get(id=collection_recipe_id, curatedCollection__id=curated_collection_id)
        except models.CollectionRecipe.DoesNotExist:
            raise NotFound('A collection recipe tied to this collection does not exist.')

        return queryset

