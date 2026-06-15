from rest_framework import serializers
from .models import UserContribution

class UserContributionSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_avatar = serializers.CharField(source='user.avatar', read_only=True)

    author_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserContribution
        fields = [
            'id', 'target_id', 'target_type', 'category', 'content', 
            'likes_count', 'created_at', 'updated_at', 
            'author_name', 'author_avatar', 'author_id'
        ]
        read_only_fields = ['id', 'likes_count', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        return obj.user.nickname if getattr(obj.user, 'nickname', '') else obj.user.username
