from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.RecipeViewSet)

app_name='recipes'

urlpatterns = [
    path('feed/',
        views.RecipeFeedListAPIView.as_view(),
        name='list-feed-recipes',
    ),
    # path('q/',
    #     views.SearchListAPIView.as_view(),
    #     name='search-recipes',
    # ),
    path('',
        include(router.urls)
    ),
    path('<str:recipe_slug>/upload-image/',
        views.RecipeImageCreateAPIView.as_view(),
        name='recipe-image-create',
    ),
    path('<str:recipe_slug>/image/<int:photo_id>/',
        views.RecipeImageRetrieveUpdateDestroyAPIView.as_view(),
        name='recipe-image-edit',
    ),
    path('<str:recipe_slug>/instructions/',
        views.InstructionListCreateAPIView.as_view(),
        name='list-create-instructions',
    ),
    path('<str:recipe_slug>/instructions/<int:instruction_id>/',
        views.InstructionRetrieveUpdateDestroyAPIView.as_view(),
        name='manage-instructions',
    ),
    # path('<str:recipe_slug>/instructions/<int:instruction_id>/upload-image/',
    #     views.InstructionImageCreateAPIView.as_view(),
    #     name='instruction-image-create',
    # ),
    # path('<str:recipe_slug>/instructions/<int:instruction_id>/image/<int:photo_id>/',
    #     views.InstructionImageRetrieveUpdateDestroyAPIView.as_view(),
    #     name='instruction-image-edit',
    # ),
    path('<str:recipe_slug>/items/',
        views.ItemListCreateAPIView.as_view(),
        name='list-create-items',
    ),
    path('<str:recipe_slug>/items/<int:item_id>/',
        views.ItemRetrieveUpdateDestroyAPIView.as_view(),
        name='manage-items',
    ),
    path('<str:recipe_slug>/items/<int:item_id>/ingredients/',
        views.IngredientListCreateAPIView.as_view(),
        name='list-create-ingredients',
    ),
    path('<str:recipe_slug>/items/<int:item_id>/ingredients/<int:ingredient_id>/',
        views.IngredientRetrieveUpdateDestroyAPIView.as_view(),
        name='manage-ingredients',
    ),
    path('<str:recipe_slug>/instructions/<int:instruction_id>/ingredients/',
        views.InstructionIngredientListCreateAPIView.as_view(),
        name='list-create-instruction-ingredient',
    ),
    path('<str:recipe_slug>/instructions/<int:instruction_id>/ingredients/<int:instruction_ingredient_id>/',
        views.InstructionIngredientRetrieveUpdateDestroyAPIView.as_view(),
        name='manage-instruction-ingredient',
    ),
]
