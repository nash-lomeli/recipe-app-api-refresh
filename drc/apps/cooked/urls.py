from django.urls import path
from . import views
app_name = 'cooked'

urlpatterns = [
    path('<str:recipe_slug>/',
        views.CookedAPIView.as_view(),
        name='cooked'
    ),
    path('<str:recipe_slug>/list/',
        views.CookedListAPIView.as_view(),
        name='cooked-list'
    ),
]