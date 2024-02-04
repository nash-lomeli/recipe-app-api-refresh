from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from . import models, serializers, renderers
from drc.apps.recipes import (models as recipe_models, 
    serializers as recipe_serializers, renderers as recipe_renderers
)
class LikeAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = recipe_serializers.RecipeSerializer
    renderer_classes = (recipe_renderers.RecipeJSONRenderer,)

    def post(self, request, recipe_slug=None):
        user = self.request.user.profile
        serializer_context = {'request': request}

        try:
            recipe = recipe_models.Recipe.objects.get(slug=recipe_slug)
        except recipe_models.Recipe.DoesNotExist:
            raise NotFound('A recipe with this slug does not exist.')

        like = models.Like.objects.filter(recipe=recipe, user=user)

        if like.exists():
            like.delete()
        else:
            models.Like.objects.create(recipe=recipe, user=user)

        serializer = self.serializer_class(recipe, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeListAPIView(generics.ListAPIView):
    serializer_class = serializers.LikeListSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.LikeJSONRenderer,)

    def get_queryset(self):
        recipe_slug = self.kwargs['recipe_slug']

        recipe = recipe_models.Recipe.objects.get(slug=recipe_slug)

        queryset = models.Like.objects.filter(recipe=recipe)
        return queryset





