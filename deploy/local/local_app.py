"""Local demo UI: upload/record Bisaya speech, transcribe it with any
combination of this project's three ASR systems -- this is an experiment
comparing them, not a product picking one, so it's a checklist rather
than a single engine picker. Run from this directory (or the repo root):

    python local_app.py

Advanced-user setup: the Kaldi engine needs WSL2/Ubuntu and a built Kaldi
checkout; ElevenLabs needs an API key. See deploy/README.md.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# "a local .env inside deploy/ or deploy/local/" -- check the more specific
# one first (doesn't override already-set vars), then fall back to the
# shared one at the deploy/ root.
_here = Path(__file__).resolve().parent
load_dotenv(_here / ".env")
load_dotenv(_here.parent / ".env")

import gradio as gr

import elevenlabs_infer
import kaldi_infer
import whisper_infer

ENGINES = ["Kaldi", "ElevenLabs", "Whisper"]
INFER = {"Kaldi": kaldi_infer, "ElevenLabs": elevenlabs_infer, "Whisper": whisper_infer}


def update_visibility(selected_engines):
    return tuple(gr.update(visible=name in selected_engines) for name in ENGINES)


def transcribe_selected(audio_path, selected_engines):
    texts = {name: "" for name in ENGINES}
    quota_message = None

    if audio_path is None:
        for name in selected_engines:
            texts[name] = "Upload or record audio first."
    else:
        for name in selected_engines:
            try:
                text = INFER[name].transcribe(audio_path)
                texts[name] = text if text.strip() else "(no speech recognized)"
            except elevenlabs_infer.QuotaExceededError as e:
                texts[name] = f"Error: {e}"
                quota_message = str(e)
            except Exception as e:
                texts[name] = f"Error: {e}"

    banner = gr.update(
        visible=quota_message is not None,
        value=(
            f'<div style="padding:10px 14px;border-left:4px solid #d32f2f;'
            f'background:#fdecea;color:#611a15;font-weight:600;">'
            f"⚠️ {quota_message}</div>"
            if quota_message else ""
        ),
    )
    return (banner,) + tuple(texts[name] for name in ENGINES)


kaldi_ready, kaldi_detail = kaldi_infer.availability_status()
elevenlabs_ready = elevenlabs_infer.is_available()

status_md = (
    f"- **Kaldi:** {'ready' if kaldi_ready else 'not available -- ' + kaldi_detail}\n"
    f"- **ElevenLabs:** {'ready' if elevenlabs_ready else 'not available -- ELEVENLABS_API_KEY is not set (see deploy/README.md)'}\n"
    f"- **Whisper:** ready (`{whisper_infer.MODEL_ID}`, loaded from the Hugging Face Hub on first use)"
)

with gr.Blocks(title="Bisaya ASR Demo (Local)") as demo:
    gr.Markdown("# Bisaya ASR Demo -- Local")
    gr.Markdown(
        "Upload or record Bisaya (Cebuano) speech and transcribe it with "
        "any combination of this project's three ASR systems, side by side."
    )
    gr.Markdown(status_md)

    banner = gr.Markdown(visible=False)

    engines = gr.CheckboxGroup(ENGINES, value=list(ENGINES), label="Models to run")
    audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Audio")
    button = gr.Button("Transcribe")

    columns = {}
    outputs = {}
    with gr.Row():
        for name in ENGINES:
            with gr.Column(visible=True) as col:
                outputs[name] = gr.Textbox(label=f"{name} Transcript", lines=4)
            columns[name] = col

    engines.change(
        fn=update_visibility,
        inputs=[engines],
        outputs=[columns[name] for name in ENGINES],
    )
    button.click(
        fn=transcribe_selected,
        inputs=[audio, engines],
        outputs=[banner] + [outputs[name] for name in ENGINES],
    )

if __name__ == "__main__":
    demo.launch()
