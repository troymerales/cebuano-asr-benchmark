---
title: Bisaya ASR Demo
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.26.0
app_file: prod_app.py
pinned: false
---

# Bisaya ASR Demo

Upload or record Bisaya (Cebuano) speech and transcribe it with a
Whisper small model fine-tuned on a Bisaya speech corpus. Runs on CPU --
expect real per-request latency, especially on a cold start.

Part of a larger benchmark comparing this fine-tuned Whisper model
against a Kaldi HMM-GMM model and ElevenLabs Scribe on the same corpus:
https://github.com/troymerales/cebuano-asr-benchmark
