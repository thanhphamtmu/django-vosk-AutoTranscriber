import json
import os
import subprocess
import tempfile
import wave
import unicodedata
from vosk import KaldiRecognizer, Model
from langdetect import detect
from django.conf import settings

class AudioProcessorService:
    _model_cache = {}

    @staticmethod
    def normalize_text(text):
        return unicodedata.normalize("NFC", text).strip().capitalize()

    @classmethod
    def get_model(cls, lang):
        if lang not in cls._model_cache:
            model_dir = {
                "vi": "vosk-model-small-vn-0.4",
                "en": "vosk-model-small-en-us-0.15"
            }.get(lang)
            if not model_dir:
                raise ValueError(f"Ngôn ngữ không hỗ trợ: {lang}")
            model_path = os.path.join(settings.BASE_DIR, "speech", model_dir)
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model không tồn tại: {model_path}")
            cls._model_cache[lang] = Model(model_path)
        return cls._model_cache[lang]

    @staticmethod
    def detect_language(text):
        try:
            lang = detect(text)
            return "vi" if lang.startswith("vi") else "en"
        except:
            return "vi"

    @classmethod
    def process(cls, file_path, lang=None):
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        try:
            convert_cmd = [
                "ffmpeg", "-y", "-i", file_path,
                "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", temp_wav
            ]
            result = subprocess.run(convert_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg lỗi: {result.stderr.decode()}")

            full_text = []
            segments = []

            with wave.open(temp_wav, "rb") as wf:
                fr = wf.getframerate()
                data = wf.readframes(4000)

                rec = KaldiRecognizer(cls.get_model(lang or "vi"), fr)
                rec.SetWords(True)
                rec.AcceptWaveform(data)
                first_result = json.loads(rec.Result())
                text_sample = cls.normalize_text(first_result.get("text", ""))

                if not lang:
                    lang = cls.detect_language(text_sample)
                    rec = KaldiRecognizer(cls.get_model(lang), fr)
                    rec.SetWords(True)
                    rec.AcceptWaveform(data)

                text = cls.normalize_text(first_result.get("text", ""))
                if text:
                    full_text.append(text)
                    segments.append(cls.format_segment(first_result))

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        text = cls.normalize_text(res.get("text", ""))
                        if text:
                            full_text.append(text)
                            segments.append(cls.format_segment(res))

                final = json.loads(rec.FinalResult())
                text = cls.normalize_text(final.get("text", ""))
                if text:
                    full_text.append(text)
                    segments.append(cls.format_segment(final))

            return " ".join(full_text), "\n".join(segments), lang
        finally:
            if os.path.exists(temp_wav):
                os.remove(temp_wav)

    @staticmethod
    def format_segment(result):
        if "result" not in result:
            return ""
        words = result["result"]
        if not words:
            return ""
        start = words[0]["start"]
        end = words[-1]["end"]
        text = AudioProcessorService.normalize_text(result.get("text", ""))
        return f"[{AudioProcessorService.format_ts(start)} - {AudioProcessorService.format_ts(end)}]: {text}"

    @staticmethod
    def format_ts(seconds):
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"
