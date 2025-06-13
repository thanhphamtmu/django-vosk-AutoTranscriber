from celery import shared_task
from .models import AudioFile
from services.audio_processor import AudioProcessorService
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def push_status_update(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "audio_updates",
        {
            "type": "audio_update",
            "data": {
                "id": instance.id,
                "status": instance.status,
                "filename": instance.audio.name,
                "transcript": instance.transcript[:50],
            },
        },
    )

@shared_task
def process_audio_async(audiofile_id):
    obj = AudioFile.objects.get(pk=audiofile_id)
    try:
        path = obj.audio.path
        transcript, dialogues, lang = AudioProcessorService.process(path, obj.language or None)
        obj.transcript = transcript
        obj.dialogues = dialogues
        obj.language = obj.language or lang
        obj.status = "done"
        obj.save(update_fields=["transcript", "dialogues", "language", "status"])
    except Exception as e:
        obj.status = "error"
        obj.save(update_fields=["status"])
        raise RuntimeError(f"Celery task lỗi: {e}")
    finally:
        push_status_update(obj)
