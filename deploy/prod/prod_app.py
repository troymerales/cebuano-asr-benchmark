"""Production demo UI: Whisper-only Bisaya transcription for lightweight
cloud hosting (Hugging Face Spaces, Streamlit Community Cloud, etc.).
Kaldi is intentionally excluded here -- it needs a compiled Kaldi
checkout under WSL2/Ubuntu, not available in standard cloud containers.
See deploy/README.md.

Run from this directory:

    python prod_app.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv

_here = Path(__file__).resolve().parent
load_dotenv(_here / ".env")
load_dotenv(_here.parent / ".env")  # deploy/.env, if this folder is run from within the full repo

import gradio as gr
from transformers import pipeline

MODEL_ID = os.environ.get("BISAYA_WHISPER_MODEL_ID", "troxyz1268/whisper-small-bisaya")
LANGUAGE = "tl"  # matches training (Tagalog -- Whisper's closest code to Bisaya/Cebuano)

_pipe = None
_load_error = None


def _get_pipeline():
    global _pipe, _load_error
    if _load_error is not None:
        raise RuntimeError(_load_error)
    if _pipe is None:
        try:
            # chunk_length_s/stride_length_s: real audio here commonly
            # exceeds Whisper's fixed 30s input window -- same long-form
            # chunking approach verified in evaluate_whisper.ipynb.
            _pipe = pipeline(
                "automatic-speech-recognition",
                model=MODEL_ID,
                chunk_length_s=30,
                stride_length_s=5,
            )
        except Exception as e:
            _load_error = f"Failed to load Whisper model ({MODEL_ID}): {e}"
            raise RuntimeError(_load_error)
    return _pipe


def transcribe(audio_path):
    if audio_path is None:
        return "Upload or record audio first."
    try:
        asr = _get_pipeline()
        result = asr(audio_path, generate_kwargs={"language": LANGUAGE, "task": "transcribe"})
        text = result["text"]
    except Exception as e:
        return f"Error: {e}"
    return text if text.strip() else "(no speech recognized)"


with gr.Blocks(title="Bisaya ASR Demo") as demo:
    gr.Markdown("# Bisaya ASR Demo")
    gr.Markdown(
        f"Upload or record Bisaya (Cebuano) speech and transcribe it with "
        f"the fine-tuned Whisper model (`{MODEL_ID}`)."
    )

    audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Audio")
    output = gr.Textbox(label="Transcript", lines=4)
    button = gr.Button("Transcribe")
    button.click(fn=transcribe, inputs=[audio], outputs=[output])

if __name__ == "__main__":
    demo.launch()
