"""Local demo UI: upload/record Bisaya speech, transcribe it with any
combination of this project's three ASR systems -- this is an experiment
comparing them, not a product picking one, so it's a checklist rather
than a single engine picker. Run from this directory (or the repo root):

    streamlit run local_app.py

Advanced-user setup: the Kaldi engine needs WSL2/Ubuntu and a built Kaldi
checkout; ElevenLabs needs an API key. See deploy/README.md.
"""

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

# "a local .env inside deploy/ or deploy/local/" -- check the more specific
# one first (doesn't override already-set vars), then fall back to the
# shared one at the deploy/ root.
_here = Path(__file__).resolve().parent
load_dotenv(_here / ".env")
load_dotenv(_here.parent / ".env")

import streamlit as st

import elevenlabs_infer
import kaldi_infer
import whisper_infer

ENGINES = ["Kaldi", "ElevenLabs", "Whisper"]
INFER = {"Kaldi": kaldi_infer, "ElevenLabs": elevenlabs_infer, "Whisper": whisper_infer}


def _save_to_temp(uploaded_file):
    suffix = Path(getattr(uploaded_file, "name", None) or "audio.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name


st.set_page_config(page_title="Bisaya ASR Demo (Local)")
st.title("Bisaya ASR Demo -- Local")
st.write(
    "Upload or record Bisaya (Cebuano) speech and transcribe it with "
    "any combination of this project's three ASR systems, side by side."
)

kaldi_ready, kaldi_detail = kaldi_infer.availability_status()
elevenlabs_ready = elevenlabs_infer.is_available()
st.markdown(
    f"- **Kaldi:** {'ready' if kaldi_ready else 'not available -- ' + kaldi_detail}\n"
    f"- **ElevenLabs:** {'ready' if elevenlabs_ready else 'not available -- ELEVENLABS_API_KEY is not set (see deploy/README.md)'}\n"
    f"- **Whisper:** ready (`{whisper_infer.MODEL_ID}`, loaded from the Hugging Face Hub on first use)"
)

banner_slot = st.empty()

selected_engines = st.multiselect("Models to run", ENGINES, default=list(ENGINES))

uploaded = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "flac", "ogg"])
recorded = st.audio_input("Or record from your microphone")
audio_file = uploaded or recorded

if st.button("Transcribe"):
    if audio_file is None:
        banner_slot.warning("Upload or record audio first.")
    elif not selected_engines:
        banner_slot.warning("Select at least one model to run.")
    else:
        audio_path = _save_to_temp(audio_file)
        results = {}
        quota_message = None
        try:
            for name in selected_engines:
                try:
                    text = INFER[name].transcribe(audio_path)
                    results[name] = text if text.strip() else "(no speech recognized)"
                except elevenlabs_infer.QuotaExceededError as e:
                    results[name] = f"Error: {e}"
                    quota_message = str(e)
                except Exception as e:
                    results[name] = f"Error: {e}"
        finally:
            os.unlink(audio_path)

        if quota_message:
            banner_slot.error(f"⚠️ {quota_message}")

        # Shown only for the models actually selected, since this is an
        # experiment comparing whatever's checked, not a fixed 3-box layout.
        for name in selected_engines:
            st.subheader(f"{name} Transcript")
            st.text_area(f"{name}_output", results[name], label_visibility="collapsed")
