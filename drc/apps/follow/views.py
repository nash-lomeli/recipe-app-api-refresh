from rest_framework import status, generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from . import renderers, serializers

from drc.apps.profiles import models


class FollowAPIView(views.APIView):
    serializer_class = serializers.FollowSerializer
    renderer_classes = (renderers.FollowerJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id=None):
        follower = self.request.user.profile
        context = {'request': request}
        
        try:
            followee = models.Profile.objects.get(id=user_id)
        except models.Profile.DoesNotExist:
            raise NotFound('A profile with this information does not exist.')

        if follower.id == followee.id:
            raise Exception('You can not follow yourself.')

        if followee in follower.follow.all():
            follower.follow.remove(followee)
        else:
            follower.follow.add(followee)

        serializer = self.serializer_class(followee,context=context)
       
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.FollowerJSONRenderer,)
    serializer_class = serializers.FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        queryset = models.Profile.objects.get(
            pk=user_id
        ).followed_by.all()

        return queryset


class FollowingListAPIVIew(generics.ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.FollowingJSONRenderer,)
    serializer_class = serializers.FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = models.Profile.objects.get(
            pk=user_id
        ).follow.all()

        return queryset