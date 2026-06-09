import os
import queue
import sys
import json
from dataclasses import dataclass
from typing import Optional

try:
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


@dataclass
class RecognitionResult:
    text: str
    engine: str


class VoiceEngine:
    """Voice recognition engine with local offline fallback."""

    def __init__(self, model_path: Optional[str] = None, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.model_path = model_path or os.environ.get("VOSK_MODEL_PATH") or "models/vosk-model-small-en-us-0.15"
        self.engine_name = None
        self._validate_engine()

    def _validate_engine(self):
        if VOSK_AVAILABLE and os.path.isdir(self.model_path):
            self.engine_name = "vosk"
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            return

        if SR_AVAILABLE:
            self.engine_name = "sphinx"
            self.recognizer = sr.Recognizer()
            return

        raise RuntimeError(
            "No local speech engine available. Install vosk and sounddevice, "
            "or speech_recognition with pocketsphinx."
        )

    def listen(self, timeout: int = 8) -> RecognitionResult:
        if self.engine_name == "vosk":
            return self._listen_vosk(timeout)
        if self.engine_name == "sphinx":
            return self._listen_sphinx(timeout)
        raise RuntimeError("Unsupported voice engine")

    def _listen_vosk(self, timeout: int) -> RecognitionResult:
        audio_queue = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(f"[voice] Audio warning: {status}")
            audio_queue.put(bytes(indata))

        print("[voice] Listening with VOSK. Speak now...")
        try:
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000, dtype="int16", channels=1, callback=callback):
                self.recognizer.Reset()
                final_text = []
                for _ in range(timeout * 5):
                    try:
                        data = audio_queue.get(timeout=1)
                    except queue.Empty:
                        continue

                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "").strip()
                        if text:
                            final_text.append(text)
                            break
                    else:
                        partial = json.loads(self.recognizer.PartialResult()).get("partial", "")
                        if partial:
                            print(f"[voice] partial: {partial}")

                if not final_text:
                    result = json.loads(self.recognizer.FinalResult())
                    final_text = [result.get("text", "").strip()]

                recognized = final_text[0] if final_text else ""
                print(f"[voice] Recognized: {recognized}")
                return RecognitionResult(text=recognized.lower(), engine="vosk")
        except Exception as exc:
            raise RuntimeError(f"Voice capture failed: {exc}")

    def _listen_sphinx(self, timeout: int) -> RecognitionResult:
        import speech_recognition as sr

        microphone = sr.Microphone()
        print("[voice] Listening with PocketSphinx fallback. Speak now...")
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

        try:
            text = self.recognizer.recognize_sphinx(audio)
            print(f"[voice] Recognized: {text}")
            return RecognitionResult(text=text.lower(), engine="sphinx")
        except sr.UnknownValueError:
            return RecognitionResult(text="", engine="sphinx")
        except sr.RequestError as exc:
            raise RuntimeError(f"PocketSphinx error: {exc}")
