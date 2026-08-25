# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A benchmark comparing two Bisaya ASR systems on the same corpus:

1. A **Kaldi HMM-GMM model trained from scratch** — a 2-gram, 3-state,
   speaker-adaptive-trained (SAT) HMM-GMM using the PS27 27-phoneme set,
   reproducing the best-performing Bisaya configuration from Ing (2023) --
   see README.md's Citation section for the full reference. Every neural
   (DNN/TDNN) variant that this work tested for Bisaya scored equal to or worse
   than this HMM-GMM configuration, which is why there is no TDNN/DNN
   stage here. `references/` (if present) is a local, git-ignored copy of
   source material for personal use only -- it is not part of this repo
   and must never be committed or redistributed.
2. **ElevenLabs Scribe**, a commercial ASR API, evaluated zero-shot on the
   same corpus for comparison.

There is no source package, build system, linter, or test suite. The core
benchmark is four Jupyter notebooks, each a runnable pipeline stage,
validated empirically by the WER/CER printed at the end of a run (see
"Notebook structure and dependency chain" below). Two more notebooks and
a small deployment demo exist alongside it but are **not** part of that
pipeline — see "Whisper fine-tuning" and "Deployment demo" further down.

## Notebook structure and dependency chain

```
train_kaldi.ipynb  ->  exported Kaldi model (models/tri3/, output/tri3/)
        |
        v
evaluate_kaldi.ipynb  ---\
                          +--> compare.ipynb
evaluate_elevenlabs.ipynb -/
```

Each notebook is self-contained for its own purpose and reads/writes only
saved files under `output/` — none of them import from another notebook.

1. **`train_kaldi.ipynb`** (WSL2/Ubuntu only — Kaldi doesn't build on
   native Windows) — trains the Kaldi HMM-GMM model from scratch: data
   prep, lexicon, LM, GMM training progression, decode, then exports
   `output/tri3/` (full decode/model output) and `models/tri3/` (curated
   subset needed to decode new audio — see `models/tri3/README.md`).
2. **`evaluate_kaldi.ipynb`** (Windows/plain Python) — reads
   `train_kaldi.ipynb`'s already-decoded output (Kaldi itself can't run on
   native Windows, so no inference happens in this notebook, only scoring
   of predictions Kaldi already produced under WSL) and computes **raw**
   (non-normalized) WER/CER, exporting `output/kaldi/results.csv`.
   Requires `train_kaldi.ipynb` to have run through decode + export.
3. **`evaluate_elevenlabs.ipynb`** (plain Python) — calls the ElevenLabs
   API over the full corpus, computes **raw** WER/CER, and exports
   `output/elevenlabs/results.csv`. Independent of (1)/(2) entirely —
   needs only the corpus and an `ELEVENLABS_API_KEY`.
4. **`compare.ipynb`** (plain Python) — the only notebook that applies
   text normalization. Loads both raw `results.csv` files, computes
   normalized WER/CER itself (via `normalize_bisaya()`, defined once,
   here only), and produces the side-by-side comparison: headline table,
   raw-vs-normalized breakdown, word/char confusion tables, charts.
   Requires (2) and (3) to have each run at least once.

**Normalization lives in exactly one place** (`compare.ipynb`'s
`normalize_bisaya()`): lowercase, strip punctuation/hyphens, fold u/o
together. Do not reintroduce it into the eval notebooks — they export raw
reference/prediction text and raw metrics only, by design, so there is a
single source of truth for what "normalized" means.

## Running the pipeline

No package manager / lockfile — dependencies are plain `pip`/`apt`
installs.

**`train_kaldi.ipynb`** (WSL2/Ubuntu, assumes an existing Kaldi checkout
at `KALDI_ROOT`, default `~/kaldi` — this notebook never clones Kaldi):

```bash
python3 -m venv ~/asr-venv && source ~/asr-venv/bin/activate
pip install jupyterlab ipykernel pandas pyarrow tqdm
cd "/mnt/c/path/to/this/repo"
jupyter lab train_kaldi.ipynb
```

Run cells in order, top to bottom. Every stage is wrapped in
`stage(name, done, fn)`, which skips work whose output already exists —
re-running after an interruption only redoes whatever didn't finish.

**`evaluate_elevenlabs.ipynb`, `evaluate_kaldi.ipynb`, `compare.ipynb`**
(plain Python, Windows or Linux, no WSL/Kaldi dependency): `pip install
pandas pyarrow jiwer matplotlib`, plus `python-dotenv` and `elevenlabs`
for `evaluate_elevenlabs.ipynb` (needs a git-ignored `.env` with
`ELEVENLABS_API_KEY`).

**Known WSL/Kaldi build gotchas** (apply to `train_kaldi.ipynb` only):
- `libatlas-base-dev` isn't packaged on newer Ubuntu — Kaldi's math
  library is built from source via `tools/extras/install_openblas.sh`
  instead (`--mathlib=OPENBLAS --openblas-root=...`). Don't re-add it.
- `sudo apt-get` from inside a Jupyter cell's subprocess has no TTY for
  the password prompt — run the apt install once by hand in a plain WSL
  terminal first, then re-run the cell.
- This Ubuntu image ships only `python3`, no bare `python` — needed by a
  diagnostic script `decode_fmllr.sh` shells out to; `train_kaldi.ipynb`
  installs `python-is-python3` for this.
- `decode_fmllr.sh` splits work per-speaker, so `--nj` can't exceed the
  test set's speaker count; and it takes `--min-lmwt`/`--max-lmwt` only
  via `--scoring-opts`, not as top-level flags.
- Alignment beams (`ALIGN_BEAM`/`ALIGN_RETRY_BEAM`, Section 13) are
  widened well past Kaldi's WSJ-recipe defaults — this corpus's
  utterances (up to ~330s) are far longer than those defaults assume.
- **Editing a notebook directly while it's open in a live Jupyter session
  is unreliable** — Jupyter's autosave can silently overwrite an external
  edit with its own stale in-memory copy. Confirm the notebook isn't open
  live before editing the `.ipynb` file directly, or describe the exact
  cell change for the user to paste in themselves.

## Corpus and join key

`CORPUS_DIR` (default `data/bisaya_audio`) holds Parquet shards, one row
per utterance, with a nested `audio` struct column and a `speaker_id`/
`transcript` per row — not pre-split into train/test. `train_kaldi.ipynb`
splits it **by speaker**, ~80/20, fixed seed 42 (checked invariant:
`train_speakers.isdisjoint(test_speakers)`).

Both `evaluate_kaldi.ipynb` and `evaluate_elevenlabs.ipynb` load every
Parquet shard the same way (`sorted()` glob order,
`pd.concat(..., ignore_index=True)`) and stamp a `corpus_index` column
(each row's position in that concatenation). This is the join key
`compare.ipynb` uses to line up the same utterances across both systems'
`results.csv` exports, and it's also how Kaldi utterance IDs
(`{speaker_id}-{corpus_index:06d}`) get mapped back to corpus metadata.
**Keep both notebooks' corpus-loading code in that exact order** — the
join breaks silently otherwise.

## `output/` and `models/` layout

Both gitignored (reproducible build output, same as `data/`):

```
output/
  tri3/                    # train_kaldi.ipynb: full exp/tri3 (model + decode + logs)
  kaldi/results.csv        # evaluate_kaldi.ipynb: raw reference/prediction/WER/CER/metadata
  elevenlabs/results.csv   # evaluate_elevenlabs.ipynb: same shape, for ElevenLabs Scribe
models/
  tri3/                    # curated subset of output/tri3/ -- just what's needed to decode new audio
```

Neither `results.csv` has `norm_*` columns — see "Normalization lives in
exactly one place" above.

## Whisper fine-tuning (standalone, not part of the benchmark)

`fine_tune_whisper.ipynb` and `fine-tune-whisper-kaggle.ipynb` are **not**
part of the `train_kaldi.ipynb` -> `compare.ipynb` pipeline above -- neither
exports a `results.csv`, neither is read by `compare.ipynb`, and this is
deliberate (a fine-tuned Whisper is an exploratory third system, not
wired into the two-system benchmark's WER/CER comparison).

- **`fine_tune_whisper.ipynb`** is the unmodified Hugging Face
  ["Fine-Tune Whisper for Multilingual ASR"](https://huggingface.co/blog/fine-tune-whisper)
  Colab tutorial (Hindi/Common Voice) -- kept only as an unmodified
  reference. Never edit this file; adapt `fine-tune-whisper-kaggle.ipynb`
  instead.
- **`fine-tune-whisper-kaggle.ipynb`** is the real, actively-run notebook:
  fine-tunes `openai/whisper-small` on this project's actual Bisaya
  corpus, on Kaggle (GPU quota, Kaggle Secrets for `HF_TOKEN`, corpus
  attached as a Kaggle Dataset -- see the notebook's own "Kaggle Setup"
  section). Uses `language="tl"` (Tagalog) as Whisper's closest built-in
  code -- there's no Cebuano/Bisaya token.

**Kaggle-environment gotchas** (hard-won from real runs, apply to
`fine-tune-whisper-kaggle.ipynb` specifically):
- **Pin `datasets<4.0`.** 4.0+ made `torchcodec` a hard requirement for
  decoding `Audio` columns, and torchcodec needs an FFmpeg build whose
  shared libs (`libavutil.so.57-60`) aren't present on Kaggle's image --
  `Could not load libtorchcodec` the moment any audio is touched.
  `HF_DATASETS_DISABLE_TORCHCODEC=1` does **not** prevent this. `datasets
  <4.0` (tested: 3.6.0) uses the classic soundfile-based decoder
  (`{"array", "sampling_rate", "path"}` dict) instead.
- **`.filter()`/`.map()` touch every column, not just the ones the
  function uses**, unless you pass `input_columns=[...]`. Filtering by
  `speaker_id` without `input_columns=["speaker_id"]` silently decodes
  the entire `audio` column for every row just to determine batch size --
  confirmed locally: ~21s vs ~0s for the identical filter on this corpus.
- **`num_proc=1` is not "no multiprocessing."** It still routes through a
  forked `multiprocess.Pool` in current `datasets` versions, which can
  deadlock (or silently corrupt decoded `Audio` objects into `None`)
  when combined with torchcodec's native ffmpeg-backed decoder. Omit
  `num_proc` entirely for genuine single-process execution.
- **Kaggle's preinstalled `torch`/`torchaudio`/`torchvision` can be
  mismatched** (e.g. `torch==2.13.0` vs `torchaudio==2.10.0+cu128`).
  `transformers` opportunistically imports both while building Whisper's
  feature extractor/processor, and their CUDA-version checks crash on
  the mismatch, taking down `from transformers import Whisper...`
  entirely. `pip uninstall` on these is not reliable on Kaggle; instead
  monkeypatch `transformers.utils.import_utils.is_torchaudio_available`
  / `is_torchvision_available` to `False` before the first
  `WhisperFeatureExtractor`/`WhisperProcessor` import (see that cell) --
  this notebook needs neither package.
- **Every utterance in this corpus exceeds Whisper's fixed 30-second
  input window** (median ~120s, max ~300s). Truncating audio to 30s
  while keeping the full transcript as the label breaks the audio/text
  alignment for training. `prepare_dataset` instead uses the corpus's
  word-level timestamps (`words`: list of `{text, start, end}`) to split
  each utterance into <=28s chunks with correctly matched audio/text.

## Deployment demo (`deploy/`)

Two standalone Gradio UIs for trying the ASR systems interactively --
separate from the benchmark notebooks above, not for computing WER/CER
(see `deploy/README.md` for full setup/run instructions). Split into two
apps because they target different audiences and environments:

```
deploy/
  README.md
  .env.example
  local/
    local_app.py         # all three engines, checklist to pick any combination
    kaldi_infer.py         # live Kaldi decode for one audio file (needs WSL2/Ubuntu)
    whisper_infer.py       # Whisper inference (Hugging Face Hub checkpoint)
    elevenlabs_infer.py    # ElevenLabs Scribe API call
    requirements.txt
  prod/
    prod_app.py           # Whisper only, self-contained, cloud-ready
    requirements.txt
```

- **`local_app.py`** -- for advanced users with the full local
  environment set up (WSL2/Ubuntu + built Kaldi checkout + exported
  `models/tri3/` for Kaldi, an `ELEVENLABS_API_KEY` for ElevenLabs).
  Model selection is a `gr.CheckboxGroup` (Kaldi/ElevenLabs/Whisper, all
  checked by default) -- transcript boxes are shown/hidden to match
  exactly what's checked, since this is an experiment comparing systems,
  not a product that picks one. Each engine's failure is caught and
  shown in its own output box rather than blocking the others; an
  ElevenLabs 401/429 (out of API credits) is specifically caught as
  `elevenlabs_infer.QuotaExceededError` and surfaced as a prominent
  warning banner across the top instead of a generic per-box error.
- **`prod_app.py`** -- Whisper-only, no engine picker, meant for
  lightweight cloud hosting (Hugging Face Spaces, Streamlit Community
  Cloud). Kaldi is omitted entirely: it needs a compiled Kaldi checkout
  under WSL/C++, which standard cloud containers can't provide. Written
  to be self-contained (no imports outside `deploy/prod/`) so the folder
  can be pushed as its own deployment unit.

Both load `troxyz1268/whisper-small-bisaya` (the checkpoint
`fine-tune-whisper-kaggle.ipynb` pushes to the Hub) from the Hub by
default via `BISAYA_WHISPER_MODEL_ID` -- override for a different Hub
repo or a local export. Both read a `.env` from their own directory
first, falling back to `deploy/.env` if present (see `deploy/.env.example`
for the full variable list, and `deploy/README.md` for setup).
