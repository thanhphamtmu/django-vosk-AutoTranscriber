import json
import os
import subprocess
import tempfile
import unicodedata
import wave
from vosk import KaldiRecognizer, Model
from django.conf import settings

_model = None



def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(settings.BASE_DIR, "speech", "vosk-model-small-vn-0.4")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model Vosk không tìm thấy tại {model_path}")
        _model = Model(model_path)
    return _model


def normalize_text(text):
    text = unicodedata.normalize("NFC", text)
    return text.strip().capitalize()


def process_audio_file(file_path):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    try:
        convert_cmd = [
            "ffmpeg",
            "-y",
            "-i", file_path,
            "-ar", "16000",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            temp_wav,
        ]
        result = subprocess.run(
            convert_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg lỗi: {result.stderr.decode()}")

        full_text = []
        segments = []

        with wave.open(temp_wav, "rb") as wf:
            rec = KaldiRecognizer(get_model(), wf.getframerate())
            rec.SetWords(True)

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    text = normalize_text(res.get("text", ""))
                    if text:
                        full_text.append(text)
                        segments.append(format_segment(res))

            final = json.loads(rec.FinalResult())
            text = normalize_text(final.get("text", ""))
            if text:
                full_text.append(text)
                segments.append(format_segment(final))

        return " ".join(full_text), "\n".join(segments)

    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)


def format_segment(result):
    if "result" not in result:
        return ""
    words = result["result"]
    if not words:
        return ""

    start = words[0]["start"]
    end = words[-1]["end"]
    text = normalize_text(result.get("text", ""))

    start_ts = format_timestamp(start)
    end_ts = format_timestamp(end)
    return f"[{start_ts} - {end_ts}]: {text}"


def format_timestamp(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"
