# Deployment

A small Gradio UI (`app.py`) for trying out the two ASR systems this project
built: upload or record Bisaya speech, pick an engine, get a transcript.

```
deploy/
  app.py             # Gradio UI
  kaldi_infer.py      # live Kaldi decode for one audio file
  whisper_infer.py    # Whisper inference -- stub until a checkpoint exists
  requirements.txt
```

This app is separate from the benchmark notebooks (`train_kaldi.ipynb`,
`evaluate_*.ipynb`, `compare.ipynb`) -- it's for trying the models
interactively, not for computing WER/CER.

## 1. Deploying Kaldi

The Kaldi engine decodes live, so it needs the same environment
`train_kaldi.ipynb` does -- **WSL2/Ubuntu (or native Linux)**, since Kaldi
doesn't build on native Windows.

**Requirements:**
- The exported model at `models/tri3/` (produced by `train_kaldi.ipynb`'s
  export stage).
- A built Kaldi checkout (`KALDI_ROOT`, default `~/kaldi` -- same one
  `train_kaldi.ipynb` used).
- `sox` (already a dependency of the training pipeline).

**Run:**

```bash
source ~/asr-venv/bin/activate   # same venv train_kaldi.ipynb uses is fine
pip install -r deploy/requirements.txt
cd "/mnt/c/path/to/this/repo"
python3 deploy/app.py
```

Gradio prints a local URL (`http://127.0.0.1:7860`) -- open it from Windows;
WSL2 forwards `localhost` automatically.

**Config (env vars, all optional):**

| Var | Default | Purpose |
|---|---|---|
| `KALDI_ROOT` | `~/kaldi` | Kaldi checkout |
| `BISAYA_KALDI_MODEL_DIR` | `models/tri3` | exported model to decode with |
| `BISAYA_KALDI_LMWT` | `13` | fixed LM weight for decoding |
| `BISAYA_DEPLOY_WORK_DIR` | `~/bisaya_deploy_work` | scratch dir for the per-request Kaldi data/mfcc/decode dirs |

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

## 2. Deploying Whisper (once it finishes)

`fine_tune_whisper_kaggle.ipynb` is still training. Until then,
`whisper_infer.py` always reports itself unavailable, but the "Whisper"
option is already visible in the UI (selecting it shows the same message).

**To activate it once training finishes:**

1. Run `fine_tune_whisper_kaggle.ipynb` on Kaggle through to
   `trainer.push_to_hub(**kwargs)` (or just `trainer.save_model(...)`).
2. Export the checkpoint (`config.json`, model weights, tokenizer,
   `preprocessor_config.json`) into `models/whisper-bisaya/` in this repo.
3. `pip install transformers torch` (not needed until this point).
4. Restart `app.py`.

`whisper_infer.is_available()` checks for `models/whisper-bisaya/config.json`
and flips the Whisper engine on automatically -- no code changes needed.
Inference uses `language="tagalog"`, matching the language the fine-tuning
notebook trains with (Whisper's closest built-in code to Bisaya/Cebuano;
see that notebook's intro for the caveat).

## Notes

- Both engines are exposed on the same page regardless of which environment
  you're running in; an engine that isn't usable there (e.g. Kaldi on plain
  Windows) reports why instead of crashing the app.
- This UI is for manual spot-checks, not benchmarking -- for WER/CER, use
  `evaluate_kaldi.ipynb` / `evaluate_elevenlabs.ipynb` / `compare.ipynb`.
