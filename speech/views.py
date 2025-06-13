import os
import time
from io import BytesIO

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

# --- Giao diện người dùng ---
from django.utils.text import slugify
from reportlab.pdfgen import canvas
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# from rest_framework.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from .forms import AudioFileForm
from .models import AudioFile
from .serializers import AudioFileSerializer


def rename_uploaded_file(file):
    ext = os.path.splitext(file.name)[1]
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    base_name = slugify(os.path.splitext(file.name)[0]) or "audio"
    return f"{timestamp}_{base_name}{ext}"


def upload_audio(request):
    if request.method == "POST":
        file = request.FILES.get("audio")
        if file:
            file.name = rename_uploaded_file(file)

        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            broadcast_update(instance)
            return redirect("list_audio")
    else:
        form = AudioFileForm()
    return render(request, "upload.html", {"form": form})


def list_audio(request):
    query = request.GET.get("q", "")
    files = AudioFile.objects.all()
    if query:
        files = files.filter(audio__icontains=query) | files.filter(
            transcript__icontains=query
        )

    paginator = Paginator(files.order_by("-id"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "list.html", {"page_obj": page_obj, "query": query})


def export_txt(request, pk):
    file = get_object_or_404(AudioFile, pk=pk)
    response = HttpResponse(file.transcript, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="transcript_{pk}.txt"'
    return response


def export_pdf(request, pk):
    file = get_object_or_404(AudioFile, pk=pk)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    textobject = p.beginText(40, 800)
    for line in file.transcript.splitlines():
        textobject.textLine(line)
        if textobject.getY() < 50:
            p.drawText(textobject)
            p.showPage()
            textobject = p.beginText(40, 800)
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="transcript_{pk}.pdf"'
    return response


# --- REST API ---
class AudioFileUploadAPI(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all().order_by("-id")
    serializer_class = AudioFileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        broadcast_update(instance)


# --- WebSocket Broadcast ---
def broadcast_update(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "audio_updates",
        {
            "type": "audio_update",
            "data": {
                "id": instance.id,
                "filename": instance.audio.name,
                "transcript": instance.transcript[:50],
            },
        },
    )
