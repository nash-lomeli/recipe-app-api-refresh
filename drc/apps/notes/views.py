from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from . import models, serializers, renderers
from drc.apps.recipes import models as recipe_models, serializers as recipe_serializers


class NoteRecipeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.NoteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (renderers.NoteRecipeJSONRenderer,)
    lookup_field = 'recipe__slug'
    lookup_url_kwarg = 'recipe_slug'
    queryset = models.NoteRecipe.objects.all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)
    
    def create(self, request, recipe_slug=None):

        context = {
            'user': self.request.user.profile,
        }

        serializer_data = request.data.get('note_recipe', {})

        try:
            context['recipe'] = recipe_models.Recipe.objects.get(slug=recipe_slug)
        except recipe_models.Recipe.DoesNotExist:
            raise NotFound('A Recipe with this slug does not exist.')

        serializer = self.serializer_class(
            data=serializer_data,
            context=context,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteRecipeIngredientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.NoteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (renderers.NoteRecipeJSONRenderer,)

    def get_object(self):
        recipe_slug = self.kwargs['recipe_slug']
        note_recipe_id = self.kwargs['note_recipe_id']

        try:
            queryset = models.NoteRecipe.objects.get(id=note_recipe_id, recipe__slug=recipe_slug)
        except models.NoteRecipe.DoesNotExist:
            raise NotFound('A note tied to this recipe does not exist.')

        return queryset



