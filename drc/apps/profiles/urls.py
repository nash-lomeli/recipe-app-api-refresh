from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('<str:username>/',
        views.ProfileRetrieveAPIView.as_view(),
        name='user-profile'
    ),
    path('',
        views.ProfieListAPIView.as_view(),
        name='profile-list'
    ),
]
