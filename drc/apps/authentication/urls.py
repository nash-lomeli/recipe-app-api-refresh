from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/',
        views.RegistrationAPIView.as_view(),
        name='user-registration'
    ),
    path('login/',
        views.LoginAPIView.as_view(),
        name='user-login'
    ),
    path('settings/',
        views.UserRetrieveUpdateAPIView.as_view(),
        name='user-settings'
    ),
]
