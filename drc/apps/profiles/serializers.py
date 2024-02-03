from rest_framework import serializers

from . import models


class ShortProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.Profile
        fields = (
            'id','username','is_following',
        )

        read_only_fields = ('id','username','is_following')

    def get_is_following(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return False
        
        if request.user.is_authenticated == False:
            return False
        
        follower = request.user.profile
        followee = obj

        return follower.is_following(followee)


class ProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')


    class Meta:
        model = models.Profile
        fields = (
            'id','username','description','cuisine',
            'street_address','city','state','postal_code',
            'is_following','is_follower','following','followers',
            'recipe_count','like_count','is_merchant',
        )

        read_only_fields = ('id','is_following',
            'is_follower','following','followers',
            'recipe_count','like_count','is_merchant',
        )


    def get_is_following(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return False
        
        if request.user.is_authenticated == False:
            return False
        
        follower = request.user.profile
        followee = obj

        return follower.is_following(followee)

    def get_is_follower(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return False
        
        if request.user.is_authenticated == False:
            return False

        follower = request.user.profile
        followee = obj

        return follower.is_follower(followee)