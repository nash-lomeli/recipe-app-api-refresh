from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from . import serializers, renderers

class RegistrationAPIView(views.APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.UserJSONRenderer,)
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):

        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):

        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.UserJSONRenderer),
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user_data = request.data

        serializer_data = {
            'email': user_data.get('email', request.user.email),
            'username': user_data.get('username', request.user.username),
            'password': user_data.get('password', None),
            'profile': {
                'name': user_data.get('name', request.user.profile.name),
                'description': user_data.get('description', request.user.profile.description),
                'cuisine': user_data.get('cuisine', request.user.profile.cuisine),
                'street_address': user_data.get('street_address', request.user.profile.street_address),
                'city': user_data.get('city', request.user.profile.city),
                'state': user_data.get('state', request.user.profile.state),
                'postal_code': user_data.get('postal_code', request.user.profile.postal_code),
            },
        }

        serializer = self.serializer_class(
            request.user,
            data=serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
