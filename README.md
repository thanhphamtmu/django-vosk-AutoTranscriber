![image](https://github.com/user-attachments/assets/3022e9c6-fedf-46a7-854c-43c7f05fbf08)
# 🎙️ Audio Transcription Platform (VOSK + Django)

Hệ thống web và API REST giúp người dùng tải lên file âm thanh, tự động chuyển đổi thành văn bản (tiếng Việt hoặc tiếng Anh), hỗ trợ realtime qua WebSocket, tích hợp Celery để xử lý nền.

## 🚀 Tính năng

- ✅ Tải lên file âm thanh `.wav`, `.mp3`, `.m4a`, v.v.
- ✅ Tự động chuyển giọng nói thành văn bản với [VOSK](https://alphacephei.com/vosk/)
- ✅ Nhận diện ngôn ngữ (tự động hoặc chọn trước)
- ✅ Trích xuất thời gian và phân đoạn hội thoại
- ✅ Hiển thị trạng thái xử lý (`pending`, `done`, `error`)
- ✅ Giao diện upload realtime (FilePond)
- ✅ Danh sách, tìm kiếm, xuất `.txt`, `.pdf`
- ✅ WebSocket thông báo realtime
- ✅ REST API sử dụng JWT

## 🛠️ Công nghệ sử dụng

- Python 3.10+
- Django 4.x
- Django REST Framework
- Django Channels (WebSocket)
- Celery + Redis (xử lý nền)
- Vosk Speech Recognition (Việt/Anh)
- FFMPEG (chuyển đổi âm thanh)
- ReportLab (xuất PDF)
- JWT (SimpleJWT)

## 🧱 Cấu trúc dự án

```
├── services/
│   └── audio_processor.py  # Xử lý audio, đa ngôn ngữ
├── speech/
│   ├── models.py           # Model AudioFile
│   ├── views.py            # Giao diện & API
│   ├── tasks.py            # Celery task xử lý audio
│   ├── serializers.py      # DRF serializers
│   ├── consumers.py        # WebSocket consumer
│   ├── forms.py            # Form upload
│   ├── templates/          # HTML giao diện
```

## 🔧 Cài đặt

### 1. Môi trường

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Tải mô hình VOSK

- Vietnamese: `vosk-model-small-vn-0.4`
- English: `vosk-model-small-en-us-0.15`

Tải từ: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

Giải nén vào thư mục:
```
/speech/vosk-model-small-vn-0.4
/speech/vosk-model-small-en-us-0.15
```

### 3. Cài FFMPEG

Ubuntu:
```bash
sudo apt update && sudo apt install ffmpeg
```

macOS/Windows: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 4. Redis + Celery

Cài Redis:
```bash
sudo apt install redis
```
✅ 5. Chạy Redis bằng Docker (nếu không muốn cài local)
```
docker run -d -p 6379:6379 --name redis-server redis 
``` 
Chạy worker Celery:
```bash
celery -A myproject worker --loglevel=info
```

### 5. Khởi chạy server

```bash
python manage.py migrate
python manage.py runserver
```

## 🔐 API REST

- `POST /api/audio/`: Upload file (yêu cầu JWT)
- `GET /api/audio/`: Danh sách audio (JWT)

## 🌐 Giao diện Web

- `/upload/`: Tải file lên realtime
- `/list/`: Danh sách, tìm kiếm, theo dõi trạng thái
- `/export/txt/<id>/`: Xuất `.txt`
- `/export/pdf/<id>/`: Xuất `.pdf`

## 📡 WebSocket

- `ws://<host>/ws/audio/`: Cập nhật realtime transcript & trạng thái

## 📄 License

MIT License
