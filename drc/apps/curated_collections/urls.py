from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CuratedCollectionViewSet)

app_name = 'curated_collections'

urlpatterns = [
    path('',include(router.urls)),
    path('<int:curated_collection_id>/upload-recipe/<str:recipe_slug>/',
        views.CollectionRecipeCreateAPIView.as_view(),
        name='collection-recipe-create'
    ),
    path('<int:curated_collection_id>/recipes/<int:collection_recipe_id>/',
        views.CollectionRecipeRetrieveUpdateDestroyAPIView.as_view(),
        name='manage-collection-recipe'
    ),
    path('<int:curated_collection_id>/recipes/',
        views.CollectionRecipeListAPIView.as_view(),
        name='curated_collection-recipe-list'
    ),
]