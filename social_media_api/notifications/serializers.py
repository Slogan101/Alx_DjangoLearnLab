from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target_type = serializers.SerializerMethodField()
    target_id = serializers.IntegerField(source='target_object_id')

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'target_id', 'timestamp', 'read']

    def get_target_type(self, obj):
        return obj.target_content_type.model
