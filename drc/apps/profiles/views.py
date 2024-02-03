from rest_framework import status, generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from . import models, renderers, serializers
from drc.apps.core.permissions import IsOwnerOrReadOnly
##from silk.profiling.profiler import silk_profile

#from src.apps.core.decorators import cache_per_user
#from django.utils.decorators import method_decorator


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = models.Profile.objects.select_related('user').all().only('id','description','cuisine',
        'street_address','city','state','postal_code','cuisine','user__id','user__username')
    renderer_classes = (renderers.ProfileJSONRenderer,)
    serializer_class = serializers.ProfileSerializer

#    @silk_profile(name='ProfileRetrieveAPIView-retrieve')
#    @method_decorator(cache_per_user(60*5))
    def retrieve(self, request, username, *args, **kwargs):

        context = {
            'request': request
        }

        try:
            profile = self.queryset.get(user__username=username)
        except models.Profile.DoesNotExist:
            raise NotFound('A profile with this information does not exist.')

        serializer = self.serializer_class(
            profile,
            context=context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfieListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = models.Profile.objects.select_related('user').all().order_by('-created_at')  \
        .only('id','user__id','user__username')
    renderer_classes = (renderers.ProfileJSONRenderer,)
    serializer_class = serializers.ShortProfileSerializer
