"""Production demo UI: Whisper-only Bisaya transcription for lightweight
cloud hosting (Streamlit Community Cloud, etc.). Kaldi is intentionally
excluded here -- it needs a compiled Kaldi checkout under WSL2/Ubuntu,
not available in standard cloud containers. See deploy/README.md.

Run from this directory:

    streamlit run prod_app.py
"""

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

_here = Path(__file__).resolve().parent
load_dotenv(_here.parent / ".env")  # deploy/.env, if this folder is run from within the full repo

import streamlit as st
from transformers import pipeline

MODEL_ID = os.environ.get("BISAYA_WHISPER_MODEL_ID", "troxyz1268/whisper-small-bisaya")
LANGUAGE = "tl"  # matches training (Tagalog -- Whisper's closest code to Bisaya/Cebuano)


@st.cache_resource(show_spinner="Loading Whisper model...")
def _get_pipeline():
    # chunk_length_s/stride_length_s: real audio here commonly exceeds
    # Whisper's fixed 30s input window -- same long-form chunking
    # approach verified in evaluate_whisper.ipynb. st.cache_resource
    # keeps this loaded once per server process, not per request.
    return pipeline(
        "automatic-speech-recognition",
        model=MODEL_ID,
        chunk_length_s=30,
        stride_length_s=5,
    )


def _save_to_temp(uploaded_file):
    suffix = Path(getattr(uploaded_file, "name", None) or "audio.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name


def transcribe(audio_path):
    asr = _get_pipeline()
    result = asr(audio_path, generate_kwargs={"language": LANGUAGE, "task": "transcribe"})
    text = result["text"]
    return text if text.strip() else "(no speech recognized)"


st.set_page_config(page_title="Bisaya ASR Demo")
st.title("Bisaya ASR Demo")
st.write(
    f"Upload or record Bisaya (Cebuano) speech and transcribe it with "
    f"the fine-tuned Whisper model (`{MODEL_ID}`)."
)

uploaded = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "flac", "ogg"])
recorded = st.audio_input("Or record from your microphone")
audio_file = uploaded or recorded

if st.button("Transcribe"):
    if audio_file is None:
        st.warning("Upload or record audio first.")
    else:
        audio_path = _save_to_temp(audio_file)
        try:
            text = transcribe(audio_path)
            st.text_area("Transcript", text, label_visibility="collapsed")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.unlink(audio_path)
