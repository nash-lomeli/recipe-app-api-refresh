from django.urls import path

from . import views

app_name = 'follow'

urlpatterns = [
    path('<int:user_id>/',
        views.FollowAPIView.as_view(),
        name='follow'
    ),
    path('<int:user_id>/followers/',
        views.FollowerListAPIView.as_view(),
        name='followers-list'
    ),
    path('<int:user_id>/following/',
        views.FollowingListAPIVIew.as_view(),
        name='following-list'
    ),
]
