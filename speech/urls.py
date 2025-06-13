from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.upload_audio, name="upload_audio"),
    path("list/", views.list_audio, name="list_audio"),
    path("export/txt/<int:pk>/", views.export_txt, name="export_txt"),
    path("export/pdf/<int:pk>/", views.export_pdf, name="export_pdf"),
    # API
    path("api/audio/", views.AudioFileUploadAPI.as_view(), name="api_audio"),
]
