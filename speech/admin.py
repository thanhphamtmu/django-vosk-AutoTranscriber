from django.contrib import admin
from .models import AudioFile

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("id", "audio", "language", "status", "short_transcript")
    readonly_fields = ("transcript", "dialogues")

    def short_transcript(self, obj):
        return obj.transcript[:75] + "..." if obj.transcript else "(Chưa xử lý)"
