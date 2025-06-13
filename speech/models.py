import os
import time
from django.db import models
from django.utils.text import slugify
from services.audio_processor import AudioProcessorService
from speech.tasks import process_audio_async

LANGUAGE_CHOICES = [
    ("vi", "Tiếng Việt"),
    ("en", "English"),
]

STATUS_CHOICES = [
    ("pending", "Đang xử lý"),
    ("done", "Đã hoàn tất"),
    ("error", "Lỗi"),
]

def upload_to_with_timestamp(instance, filename):
    name, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = slugify(name)
    return f"uploads/{timestamp}_{safe_name}{ext}"


class AudioFile(models.Model):
    audio = models.FileField(upload_to=upload_to_with_timestamp, blank=True, null=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="vi")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    transcript = models.TextField(blank=True, editable=False)
    dialogues = models.TextField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding and self.audio
        if is_new:
            self.status = "pending"
        super().save(*args, **kwargs)
        if is_new and (not self.transcript or not self.dialogues):
            process_audio_async.delay(self.id)
