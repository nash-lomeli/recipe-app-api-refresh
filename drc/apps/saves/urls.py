from django.urls import path	

from . import views	

app_name = 'saves'	

urlpatterns = [	
    path('<str:recipe_slug>/',	
        views.SaveAPIView.as_view(),	
        name='save-recipe'	
    ),	
    path('list',	
        views.SaveListAPIView.as_view(),	
        name='save-list'	
    ),	
] 