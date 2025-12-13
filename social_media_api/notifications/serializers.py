from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    actor_id = serializers.IntegerField(source='actor.id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_id', 'verb', 'target_content_type', 'target_object_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'actor', 'actor_id', 'verb', 'target_content_type', 'target_object_id', 'timestamp']
