import os
import time
from django.db import models
from django.utils.text import slugify
from .vosk_utils import process_audio_file


def upload_to_with_timestamp(instance, filename):
    name, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = slugify(name)
    return f"uploads/{timestamp}_{safe_name}{ext}"


class AudioFile(models.Model):
    audio = models.FileField(upload_to=upload_to_with_timestamp, blank=True, null=True)
    transcript = models.TextField(blank=True, editable=False)
    dialogues = models.TextField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding and self.audio
        super().save(*args, **kwargs)

        if is_new and (not self.transcript or not self.dialogues):
            try:
                path = self.audio.path
                self.transcript, self.dialogues = process_audio_file(path)
                super().save(update_fields=["transcript", "dialogues"])
            except Exception as e:
                raise RuntimeError(f"Lỗi xử lý file âm thanh: {e}")
