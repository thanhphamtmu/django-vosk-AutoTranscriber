![image](https://github.com/user-attachments/assets/1e72dccd-4a01-4b9e-abc9-2d6475144990)

# 🎙️ Audio Transcription Platform (VOSK + Django)

Hệ thống web và API REST giúp người dùng tải lên các file âm thanh, tự động chuyển đổi thành văn bản tiếng Việt, cung cấp giao diện web, API bảo mật, và cập nhật realtime qua WebSocket.

## 🚀 Tính năng

- ✅ Tải lên file âm thanh `.wav`, `.mp3`, `.m4a`, v.v.
- ✅ Tự động chuyển giọng nói thành văn bản với [VOSK](https://alphacephei.com/vosk/)
- ✅ Trích xuất thời gian và phân đoạn hội thoại
- ✅ Xem danh sách, tìm kiếm và xuất kết quả sang `.txt`, `.pdf`
- ✅ Cập nhật realtime qua WebSocket
- ✅ API REST chuẩn JWT để tích hợp bên thứ ba

## 🛠️ Công nghệ sử dụng

- Python 3.10+
- Django 4.x
- Django REST Framework
- Django Channels (ASGI, WebSocket)
- Vosk Speech Recognition (Vietnamese)
- FFMPEG (chuyển đổi âm thanh)
- ReportLab (PDF export)
- JWT (SimpleJWT)

## 🧱 Cấu trúc dự án
![django-vosk-AutoTranscriber diagram](https://github.com/user-attachments/assets/10bf6b18-679a-4b88-949f-1b428bebcce2)


```
├── vosk_utils.py        # Xử lý nhận dạng giọng nói
├── models.py            # Model lưu file và transcript
├── views.py             # Views upload, list, export
├── serializers.py       # API serializers
├── forms.py             # Form upload file
├── urls.py              # Routing HTTP
├── routing.py           # Routing WebSocket
├── consumers.py         # WebSocket consumer
├── admin.py             # Giao diện admin
```

## 🔧 Cài đặt

### 1. Cài đặt môi trường

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Tải mô hình VOSK (Vietnamese)

Tải từ: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

Giải nén vào thư mục:
```
/speech/vosk-model-small-vn-0.4
```

### 3. Cài đặt FFMPEG

Ubuntu:
```bash
sudo apt update && sudo apt install ffmpeg
```

Windows/macOS: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 4. Chạy migrations và server

```bash
python manage.py migrate
python manage.py runserver
```

## 🔐 API sử dụng

- **POST /api/audio/**: Upload file audio
- **GET /api/audio/**: Danh sách file và transcript
> Yêu cầu `JWT Authentication`

## 🌐 Giao diện web

- `/upload/`: Tải file lên
- `/list/`: Danh sách và tìm kiếm transcript
- `/export/txt/<id>/`: Xuất `.txt`
- `/export/pdf/<id>/`: Xuất `.pdf`

## 📡 WebSocket

- `ws://<host>/ws/audio/`: Nhận realtime update khi file mới được xử lý

## 📄 License

MIT License.
