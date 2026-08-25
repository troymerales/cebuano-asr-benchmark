# Deployment

Two separate Gradio apps, for two separate audiences:

```
deploy/
  README.md
  .env.example       # copy into deploy/local/.env and/or deploy/prod/.env
  local/
    local_app.py      # all three engines, model-selection checklist
    kaldi_infer.py     # live Kaldi decode for one audio file
    whisper_infer.py   # Whisper inference (Hugging Face Hub checkpoint)
    elevenlabs_infer.py # ElevenLabs Scribe API call
    requirements.txt
  prod/
    prod_app.py        # Whisper only, self-contained, cloud-ready
    requirements.txt
```

Both are separate from the benchmark notebooks (`train_kaldi.ipynb`,
`evaluate_*.ipynb`, `compare.ipynb`) -- these are for trying the models
interactively, not for computing WER/CER.

## 0. Environment setup (do this first, for either app)

Copy `deploy/.env.example` to a `.env` file before launching either app --
`local_app.py` looks for `deploy/local/.env` first, then falls back to
`deploy/.env`; `prod_app.py` looks for `deploy/prod/.env` first, then the
same fallback. Only fill in the variables the app you're running actually
needs (see the comments in `.env.example`).

## 1. `local_app.py` -- for advanced users

Runs **all three** systems (Kaldi, ElevenLabs, Whisper) with a checklist
to pick any combination -- transcript boxes appear only for the models
you've checked. This is the one to use for actually comparing the
systems, but it needs real setup:

- **Kaldi** decodes live, so it needs the same environment
  `train_kaldi.ipynb` does -- **WSL2/Ubuntu (or native Linux)**, a built
  Kaldi checkout (`KALDI_ROOT`), the exported model at `models/tri3/`,
  and `sox`.
- **ElevenLabs** needs `ELEVENLABS_API_KEY` in your `.env`. If the key
  runs out of credits mid-demo, the API returns 401/429 and the UI shows
  a prominent warning banner ("ElevenLabs transcription failed: Token
  quota exceeded...") instead of a generic error -- the other two engines
  keep working regardless.
- **Whisper** just needs internet access to pull
  `troxyz1268/whisper-small-bisaya` from the Hugging Face Hub on first
  use -- no extra setup.

**Run:**

```bash
source ~/asr-venv/bin/activate   # same venv train_kaldi.ipynb uses is fine
pip install -r deploy/local/requirements.txt
cd deploy/local
python local_app.py
```

Gradio prints a local URL (`http://127.0.0.1:7860`) -- open it from
Windows; WSL2 forwards `localhost` automatically.

**Config (env vars, all optional except `ELEVENLABS_API_KEY`):**

| Var | Default | Purpose |
|---|---|---|
| `KALDI_ROOT` | `~/kaldi` | Kaldi checkout |
| `BISAYA_KALDI_MODEL_DIR` | `models/tri3` | exported model to decode with |
| `BISAYA_KALDI_LMWT` | `13` | fixed LM weight for decoding |
| `BISAYA_DEPLOY_WORK_DIR` | `~/bisaya_deploy_work` | scratch dir for the per-request Kaldi data/mfcc/decode dirs |
| `ELEVENLABS_API_KEY` | *(required for ElevenLabs)* | ElevenLabs API key |
| `BISAYA_WHISPER_MODEL_ID` | `troxyz1268/whisper-small-bisaya` | Hub repo id or local path to the Whisper checkpoint |

`BISAYA_DEPLOY_WORK_DIR` must be a WSL-native path (not under `/mnt/c/...`)
-- Kaldi's shell scripts do unquoted path handling internally and this
repo's own path has spaces in it (`windows 10`, `speech model`), which
breaks them. `kaldi_infer.py` reaches `models/tri3/` through a space-free
symlink it creates inside the work dir, so this is transparent as long as
you don't override the default onto a `/mnt/c` path yourself.

`kaldi_infer.py` builds a one-utterance Kaldi data dir per request, runs
`steps/make_mfcc.sh` + `steps/decode_fmllr.sh` against `models/tri3/graph`
(same as `evaluate_kaldi.ipynb`'s decode, just for one ad-hoc utterance
instead of the test set), and reads the hypothesis straight off the decoded
lattice with `lattice-best-path` -- there's no reference transcript to
score against, so `BISAYA_KALDI_LMWT` is a fixed value instead of the swept
`--min-lmwt`/`--max-lmwt` range the eval notebook uses. If transcripts look
off, try a different value (the eval notebook's sweep covers 1-25).

## 2. `prod_app.py` -- for cloud hosting

A lightweight, **Whisper-only** experience meant for standard cloud
container environments (Hugging Face Spaces, Streamlit Community Cloud,
etc.) that can't build Kaldi or hold API secrets safely for public
traffic. No engine picker, no Kaldi, no ElevenLabs -- just upload/record
and get a transcript from the fine-tuned model.

Self-contained: `deploy/prod/` has everything it needs (`prod_app.py` +
`requirements.txt`) to be pushed as its own deployment unit, with no
dependency on the rest of this repo.

**Run:**

```bash
pip install -r deploy/prod/requirements.txt
cd deploy/prod
python prod_app.py
```

**Config (env var, optional):**

| Var | Default | Purpose |
|---|---|---|
| `BISAYA_WHISPER_MODEL_ID` | `troxyz1268/whisper-small-bisaya` | Hub repo id or local path to the Whisper checkpoint |

Runs on CPU by default (no GPU logic here) -- fine for a free-tier
showcase, just expect real per-request latency, especially cold-start on
first use.

## Notes

- Each engine reports why it isn't usable in its own output box instead
  of crashing the app -- one engine failing never blocks the others in
  `local_app.py`.
- Neither app is for benchmarking -- for WER/CER, use `evaluate_kaldi.ipynb`
  / `evaluate_elevenlabs.ipynb` / `compare.ipynb` (and whatever notebook
  currently scores Whisper -- check the repo root, this changed recently).
