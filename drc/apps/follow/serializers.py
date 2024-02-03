from rest_framework import serializers

from drc.apps.profiles import models


class FollowSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.Profile
        fields = (
            'id','username','is_following','is_follower',
            'following','followers',
        )

        read_only_fields = ('id','user_id',)

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
