from django.urls import path
from . import views
app_name = 'like'

urlpatterns = [
    path('<str:recipe_slug>/',
        views.LikeAPIView.as_view(),
        name='like'
    ),
    path('<str:recipe_slug>/list/',
        views.LikeListAPIView.as_view(),
        name='like-list'
    ),
]