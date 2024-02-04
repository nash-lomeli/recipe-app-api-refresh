from rest_framework import generics, views, status	
from rest_framework.response import Response	
from rest_framework.permissions import IsAuthenticated

from drc.apps.recipes import models as recipe_models	

from . import models, serializers, renderers	


class SaveAPIView(views.APIView):	
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_slug=None):	
        user = self.request.user.profile	

        try:	
            recipe = recipe_models.Recipe.objects.get(slug=recipe_slug)	
        except recipe_models.Recipe.DoesNotExist:	
            raise TypeError('A recipe with this information does not exist.')	

        saved_recipe = models.SaveRecipe.objects.filter(user=user, recipe=recipe)	

        action = None	

        if saved_recipe.exists():	
            saved_recipe.delete()	
            action = 'Unsaved'	
        else:	
            models.SaveRecipe.objects.create(user=user, recipe=recipe)	
            action = 'Saved'	

        data = {	
            'action': action	
        }	

        return Response(data, status=status.HTTP_200_OK)	


class SaveListAPIView(generics.ListAPIView):	
    serializer_class = serializers.SaveRecipeSerializer	
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.SaveRecipeJSONRenderer,)	

    def get_queryset(self):	
        user = self.request.user.profile	

        queryset = models.SaveRecipe.objects.filter(	
            user=user	
        ).order_by('-created_at')	
        return queryset	
