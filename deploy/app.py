"""Super simple demo UI: upload/record Bisaya speech, transcribe it with
either ASR system this project built. Run from the repo root:

    python3 deploy/app.py

See deployment.md for environment requirements (the Kaldi engine needs
WSL2/Ubuntu; Whisper needs a fine-tuned checkpoint that doesn't exist yet).
"""

import gradio as gr

import kaldi_infer
import whisper_infer

ENGINE_KALDI = "Kaldi (HMM-GMM)"
ENGINE_WHISPER = "Whisper (fine-tuning in progress)"
ENGINES = [ENGINE_KALDI, ENGINE_WHISPER]


def transcribe(audio_path, engine):
    if audio_path is None:
        return "Upload or record audio first."
    try:
        if engine == ENGINE_KALDI:
            text = kaldi_infer.transcribe(audio_path)
        else:
            text = whisper_infer.transcribe(audio_path)
    except Exception as e:
        return f"Error: {e}"
    return text if text.strip() else "(no speech recognized)"


kaldi_ready, kaldi_detail = kaldi_infer.availability_status()
whisper_ready = whisper_infer.is_available()

status_md = (
    f"- **Kaldi:** {'ready' if kaldi_ready else 'not available -- ' + kaldi_detail}\n"
    f"- **Whisper:** {'ready' if whisper_ready else 'not available yet -- fine-tuning in progress (see fine_tune_whisper_kaggle.ipynb)'}"
)

with gr.Blocks(title="Bisaya ASR Demo") as demo:
    gr.Markdown("# Bisaya ASR Demo")
    gr.Markdown(
        "Upload or record Bisaya (Cebuano) speech and transcribe it with "
        "either ASR system from this project."
    )
    gr.Markdown(status_md)

    engine = gr.Radio(ENGINES, value=ENGINE_KALDI, label="Engine")
    audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Audio")
    output = gr.Textbox(label="Transcript", lines=4)
    button = gr.Button("Transcribe")
    button.click(fn=transcribe, inputs=[audio, engine], outputs=output)

if __name__ == "__main__":
    demo.launch()
