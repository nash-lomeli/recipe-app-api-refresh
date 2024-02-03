from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from drc.apps.profiles.serializers import ProfileSerializer
from django.contrib.auth import models as group_models

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email','username','password','token')

    def create(self, validated_data):
        print('create',validated_data)

        return get_user_model().objects.create_user(**validated_data)


class GroupSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = group_models.Group
        fields = (
            'id','name'
        )


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
 
    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )

        return {
            'id': user.id,
            'email': email,
            'username': user.username,
            'token': user.token,
            'groups': user.groups.all()
        }



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False,
        allow_null=True,
    )
    groups = GroupSerializer(many=True, read_only=True)
    profile = ProfileSerializer(write_only=True)

    name = serializers.CharField(source='profile.name', read_only=True)
    description = serializers.CharField(source='profile.description', read_only=True)
    cuisine = serializers.CharField(source='profile.cuisine', read_only=True)
    street_address = serializers.CharField(source='profile.street_address', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    state = serializers.CharField(source='profile.state', read_only=True)
    postal_code = serializers.CharField(source='profile.postal_code', read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id','email','username','password','token','profile','name',
            'cuisine','description','street_address','city',
            'state','postal_code','groups',
        )

        read_only_fields = ('id','token',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():

            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for (key, value) in profile.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance
