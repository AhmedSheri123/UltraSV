from rest_framework import serializers
from accounts.models import Notification


class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'message_ar', 'message_en', 'is_seen')
