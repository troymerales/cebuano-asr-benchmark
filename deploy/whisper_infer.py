"""Whisper transcription -- loads the fine-tuned checkpoint
fine-tune-whisper-kaggle.ipynb pushes to the Hugging Face Hub, the same
model evaluate_whisper.ipynb evaluates. Set BISAYA_WHISPER_MODEL_ID to a
local directory instead if you have a manually exported checkpoint --
transformers' pipeline() accepts a Hub repo id or a local path
transparently, so no code change is needed either way.
"""

import os

MODEL_ID = os.environ.get("BISAYA_WHISPER_MODEL_ID", "troxyz1268/whisper-small-bisaya")
LANGUAGE = "tl"  # matches training (Tagalog -- Whisper's closest code to Bisaya/Cebuano)

_pipe = None
_load_error = None


def is_available():
    return _load_error is None


def transcribe(audio_path):
    global _pipe, _load_error
    if _load_error is not None:
        raise RuntimeError(_load_error)

    if _pipe is None:
        from transformers import pipeline
        try:
            # chunk_length_s/stride_length_s: this project's audio (and any
            # realistic microphone/upload here) commonly exceeds Whisper's
            # fixed 30s input window -- same long-form chunking approach
            # verified in evaluate_whisper.ipynb. Without it, generate()
            # raises on inputs over 30s instead of transcribing them.
            _pipe = pipeline(
                "automatic-speech-recognition",
                model=MODEL_ID,
                chunk_length_s=30,
                stride_length_s=5,
            )
        except Exception as e:
            _load_error = f"Failed to load Whisper model ({MODEL_ID}): {e}"
            raise RuntimeError(_load_error)

    result = _pipe(audio_path, generate_kwargs={"language": LANGUAGE, "task": "transcribe"})
    return result["text"]
