"""Super simple demo UI: upload/record Bisaya speech, transcribe it with
both ASR systems this project built, side by side -- this is an experiment
comparing them, not a product picking one, so there's no engine selector.
Run from the repo root:

    python3 deploy/app.py

See deployment.md for environment requirements (the Kaldi engine needs
WSL2/Ubuntu; Whisper needs internet access to pull the fine-tuned
checkpoint from the Hugging Face Hub on first use).
"""

import gradio as gr

import kaldi_infer
import whisper_infer


def _run(engine_transcribe, audio_path):
    try:
        text = engine_transcribe(audio_path)
    except Exception as e:
        return f"Error: {e}"
    return text if text.strip() else "(no speech recognized)"


def transcribe_both(audio_path):
    if audio_path is None:
        message = "Upload or record audio first."
        return message, message
    return (
        _run(kaldi_infer.transcribe, audio_path),
        _run(whisper_infer.transcribe, audio_path),
    )


kaldi_ready, kaldi_detail = kaldi_infer.availability_status()

status_md = (
    f"- **Kaldi:** {'ready' if kaldi_ready else 'not available -- ' + kaldi_detail}\n"
    f"- **Whisper:** ready (`{whisper_infer.MODEL_ID}`, loaded from the Hugging Face Hub on first use)"
)

with gr.Blocks(title="Bisaya ASR Demo") as demo:
    gr.Markdown("# Bisaya ASR Demo")
    gr.Markdown(
        "Upload or record Bisaya (Cebuano) speech and transcribe it with "
        "both ASR systems from this project side by side."
    )
    gr.Markdown(status_md)

    audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Audio")
    button = gr.Button("Transcribe")
    with gr.Row():
        kaldi_output = gr.Textbox(label="Kaldi (HMM-GMM)", lines=4)
        whisper_output = gr.Textbox(label="Whisper (fine-tuned)", lines=4)
    button.click(fn=transcribe_both, inputs=[audio], outputs=[kaldi_output, whisper_output])

if __name__ == "__main__":
    demo.launch()
