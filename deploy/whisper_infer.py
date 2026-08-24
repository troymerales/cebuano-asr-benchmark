"""Whisper transcription -- stub until fine-tuning (fine_tune_whisper_kaggle.ipynb)
finishes and a checkpoint is exported to models/whisper-bisaya/.

Auto-activates: once that directory holds a real checkpoint, is_available()
starts returning True and transcribe() loads and runs it, no code changes
needed in app.py.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(os.environ.get("BISAYA_WHISPER_MODEL_DIR", PROJECT_ROOT / "models" / "whisper-bisaya")).resolve()

NOT_AVAILABLE_MESSAGE = (
    "Whisper model is still being fine-tuned and isn't available yet. "
    "See fine_tune_whisper_kaggle.ipynb -- once training finishes, export the "
    f"checkpoint to {MODEL_DIR} and this engine activates automatically."
)

_pipe = None


def is_available():
    return (MODEL_DIR / "config.json").exists()


def transcribe(audio_path):
    global _pipe
    if not is_available():
        raise RuntimeError(NOT_AVAILABLE_MESSAGE)

    if _pipe is None:
        from transformers import pipeline
        _pipe = pipeline("automatic-speech-recognition", model=str(MODEL_DIR))

    # "tagalog" matches the language fine_tune_whisper_kaggle.ipynb trains
    # with -- Whisper's closest supported code to Bisaya/Cebuano.
    result = _pipe(audio_path, generate_kwargs={"language": "tagalog"})
    return result["text"]
