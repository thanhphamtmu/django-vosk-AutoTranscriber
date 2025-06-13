from rest_framework import serializers

from .models import AudioFile


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ["id", "audio", "language", "status", "transcript", "dialogues"]
        read_only_fields = ["transcript", "dialogues", "status"]

