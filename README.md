![image](https://github.com/user-attachments/assets/3022e9c6-fedf-46a7-854c-43c7f05fbf08)
# 🎙️ Audio Transcription Platform (VOSK + Django)

Nền tảng web và REST API để tải lên file âm thanh, tự động chuyển đổi giọng nói sang văn bản (tiếng Việt hoặc tiếng Anh), hỗ trợ realtime qua WebSocket, nhận diện ngôn ngữ tự động, xử lý nền bằng Celery.

## 🚀 Tính năng

- ✅ Tải lên file `.wav`, `.mp3`, `.m4a`, v.v.
- ✅ Nhận diện giọng nói với [VOSK](https://alphacephei.com/vosk/)
- ✅ Tự động nhận diện ngôn ngữ (Việt/Anh)
- ✅ Trích xuất đoạn hội thoại với timestamp
- ✅ Trạng thái xử lý: `pending`, `done`, `error`
- ✅ Giao diện upload realtime (FilePond + WebSocket)
- ✅ Tìm kiếm, lọc danh sách audio
- ✅ Xuất kết quả `.txt` / `.pdf`
- ✅ REST API sử dụng JWT
- ✅ Xử lý nền với Celery + Redis

## 🛠️ Công nghệ

- Python 3.10+
- Django 4.x
- Django REST Framework
- Django Channels (WebSocket)
- Celery + Redis
- Vosk Speech Recognition
- FFMPEG (chuyển đổi âm thanh)
- langdetect (phát hiện ngôn ngữ)
- ReportLab (PDF export)
- JWT (SimpleJWT)

## 🧱 Cấu trúc dự án

```
├── services/audio_processor.py     # Xử lý audio, phát hiện ngôn ngữ
├── speech/
│   ├── models.py                   # Model AudioFile (audio, language, status, transcript,...)
│   ├── views.py                    # Giao diện + REST API
│   ├── forms.py                    # Form upload
│   ├── templates/                  # HTML giao diện (upload, list)
│   ├── tasks.py                    # Celery background task
│   ├── consumers.py                # WebSocket consumer
│   ├── serializers.py              # DRF serializers
│   ├── routing.py                  # WebSocket routing
```

## 🔧 Cài đặt

### 1. Tạo môi trường ảo & cài thư viện

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Tải mô hình VOSK

- Tiếng Việt: `vosk-model-small-vn-0.4`
- Tiếng Anh: `vosk-model-small-en-us-0.15`

Nguồn: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

Giải nén vào:

```
speech/vosk-model-small-vn-0.4/
speech/vosk-model-small-en-us-0.15/
```

### 3. Cài FFMPEG

Ubuntu:
```bash
sudo apt update && sudo apt install ffmpeg
```

macOS/Windows: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 4. Redis + Celery

Chạy Redis bằng Docker:
```bash
docker run -d -p 6379:6379 --name redis-server redis
```

Khởi chạy Celery worker:
```bash
celery -A myproject worker --loglevel=info
```

### 5. Migrate và chạy server

```bash
python manage.py migrate
python manage.py runserver
```

## 🔐 API

- `POST /api/audio/`: Tải file (yêu cầu JWT)
- `GET /api/audio/`: Danh sách file

## 🌐 Giao diện Web

- `/upload/`: Giao diện tải file realtime
- `/list/`: Danh sách file, tìm kiếm, xuất kết quả
- `/export/txt/<id>/`: Tải kết quả `.txt`
- `/export/pdf/<id>/`: Tải kết quả `.pdf`

## 📡 WebSocket

- `ws://<host>/ws/audio/`: Nhận thông báo trạng thái và kết quả realtime

## 📄 License

MIT License.
