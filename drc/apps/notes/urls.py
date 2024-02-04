from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('<str:recipe_slug>/',
        views.NoteRecipeListCreateAPIView.as_view(),
        name='list-create-note_recipe'
    ),
    path('<str:recipe_slug>/<int:note_recipe_id>/',
        views.NoteRecipeIngredientRetrieveUpdateDestroyAPIView.as_view(),
        name='list-create-note_recipe'
    ),
]
