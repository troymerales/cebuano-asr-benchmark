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
load_dotenv(_here.parent / ".env")

import streamlit as st

import elevenlabs_infer
import kaldi_infer
import soap_infer
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
soap_ready = soap_infer.is_available()
st.markdown(
    f"- **Kaldi:** {'ready' if kaldi_ready else 'not available -- ' + kaldi_detail}\n"
    f"- **ElevenLabs:** {'ready' if elevenlabs_ready else 'not available -- ELEVENLABS_API_KEY is not set (see deploy/README.md)'}\n"
    f"- **Whisper:** ready (`{whisper_infer.MODEL_ID}`, loaded from the Hugging Face Hub on first use)\n"
    f"- **SOAP notes (Gemini):** {'ready' if soap_ready else 'not available -- GEMINI_API_KEY is not set (see deploy/README.md)'}"
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
        soap_sections = None
        soap_error = None
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

            # SOAP generation always runs off Whisper's transcript -- it's
            # this project's best free WER/CER -- regardless of which
            # models were checked above, so run it separately if it wasn't
            # one of the selected engines.
            whisper_text = results.get("Whisper")
            if whisper_text is None or whisper_text.startswith("Error:"):
                try:
                    whisper_text = whisper_infer.transcribe(audio_path)
                except Exception as e:
                    whisper_text = None
                    soap_error = f"Could not transcribe with Whisper for SOAP generation: {e}"

            if whisper_text:
                try:
                    soap_sections = soap_infer.generate_soap(whisper_text)
                except soap_infer.SoapUnavailableError as e:
                    soap_error = str(e)
                except Exception as e:
                    soap_error = f"SOAP generation failed: {e}"
        finally:
            os.unlink(audio_path)

        if quota_message:
            banner_slot.error(f"⚠️ {quota_message}")

        st.subheader("SOAP Note")
        if soap_sections:
            for section in soap_infer.SECTIONS:
                st.markdown(f"**{section}**")
                st.write(soap_sections.get(section) or "_(empty)_")
        else:
            st.info(soap_error or "SOAP note unavailable.")

        # Shown only for the models actually selected, since this is an
        # experiment comparing whatever's checked, not a fixed 3-box layout.
        # Laid out as columns (side by side) rather than stacked, so
        # multiple transcripts sit on one horizontal line.
        st.subheader("Raw transcription")
        cols = st.columns(len(selected_engines))
        for col, name in zip(cols, selected_engines):
            with col:
                st.markdown(f"**{name}**")
                st.text_area(f"{name}_output", results[name], label_visibility="collapsed")
