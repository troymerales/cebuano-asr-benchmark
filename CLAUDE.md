# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A benchmark comparing three Bisaya ASR systems on the same corpus:

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
3. A **Whisper small model fine-tuned on this corpus**, on Kaggle (GPU) --
   see "Whisper fine-tuning" further down. Unlike ElevenLabs, this system
   is trained on 80% of the corpus's speakers, the same speaker-independent
   split Kaldi uses.

There is no source package, build system, linter, or test suite. All five
notebooks live under `notebooks/`, each self-contained (see "Notebook
structure and dependency chain" below for the run order and how they hand
off to each other). A small deployment demo exists alongside the
benchmark but is **not** part of it -- see "Deployment demo" further down.

## Notebook structure and dependency chain

All five notebooks live under `notebooks/`:

```
notebooks/train_kaldi.ipynb  ->  exported Kaldi model (models/tri3/, output/tri3/)
        |
        v
notebooks/evaluate_kaldi.ipynb  ------\
                                       |
notebooks/evaluate_elevenlabs.ipynb --+--> notebooks/compare.ipynb
                                       |
notebooks/finetune_whisper.ipynb -----/
        (runs on Kaggle; output/whisper/results.csv is downloaded
        from there and dropped in manually -- see below)
```

Each notebook is self-contained for its own purpose and reads/writes only
saved files under `output/` — none of them import from another notebook.
Because `notebooks/train_kaldi.ipynb` and `notebooks/compare.ipynb` (etc.)
no longer sit at the repo root, every notebook's own default relative
paths (`CORPUS_DIR`, `RESULTS_DIR`, `MODELS_DIR`) are `../data/...`,
`../output`, `../models` -- one level up from `notebooks/` back to the
repo root. This assumes Jupyter's normal default: a notebook's kernel
working directory is the directory containing the `.ipynb` file itself.

1. **`notebooks/train_kaldi.ipynb`** (WSL2/Ubuntu only — Kaldi doesn't
   build on native Windows) — trains the Kaldi HMM-GMM model from
   scratch: data prep, lexicon, LM, GMM training progression, decode,
   then exports `output/tri3/` (full decode/model output) and
   `models/tri3/` (curated subset needed to decode new audio — see
   `models/tri3/README.md`, if present).
2. **`notebooks/evaluate_kaldi.ipynb`** (Windows/plain Python) — reads
   `train_kaldi.ipynb`'s already-decoded output (Kaldi itself can't run on
   native Windows, so no inference happens in this notebook, only scoring
   of predictions Kaldi already produced under WSL) and computes **raw**
   (non-normalized) WER/CER, exporting `output/kaldi/results.csv`.
   Requires `train_kaldi.ipynb` to have run through decode + export.
3. **`notebooks/evaluate_elevenlabs.ipynb`** (plain Python) — calls the
   ElevenLabs API over the full corpus, computes **raw** WER/CER, and
   exports `output/elevenlabs/results.csv`. Independent of (1)/(2)
   entirely — needs only the corpus and an `ELEVENLABS_API_KEY`.
4. **`notebooks/finetune_whisper.ipynb`** (Kaggle, GPU — not run locally)
   — fine-tunes `openai/whisper-small` on the same speaker-independent
   split Kaldi uses, then (in a section at the bottom) evaluates the
   fine-tuned checkpoint on the held-out test set and exports a
   `results.csv` you download from Kaggle's Output tab and drop into
   `output/whisper/results.csv` locally. A further section evaluates the
   original pre-fine-tuning checkpoint on the same test set as an
   ablation (exported separately, not read by `compare.ipynb`). See
   "Whisper fine-tuning" further down for the full detail.
5. **`notebooks/compare.ipynb`** (plain Python) — the only notebook that
   applies text normalization. Loads all three raw `results.csv` files,
   computes normalized WER/CER itself (via `normalize_bisaya()`, defined
   once, here only), and produces the side-by-side comparison: headline
   table, raw-vs-normalized breakdown, word/char confusion tables,
   charts. Requires (2), (3), and (4) to have each run at least once.

**Normalization lives in exactly one place** (`compare.ipynb`'s
`normalize_bisaya()`): lowercase, strip punctuation/hyphens, fold u/o
together. Do not reintroduce it into the eval notebooks — they export raw
reference/prediction text and raw metrics only, by design, so there is a
single source of truth for what "normalized" means.

## Running the pipeline

No package manager / lockfile — dependencies are plain `pip`/`apt`
installs.

**`notebooks/train_kaldi.ipynb`** (WSL2/Ubuntu, assumes an existing Kaldi
checkout at `KALDI_ROOT`, default `~/kaldi` — this notebook never clones
Kaldi):

```bash
python3 -m venv ~/asr-venv && source ~/asr-venv/bin/activate
pip install jupyterlab ipykernel pandas pyarrow tqdm
cd "/mnt/c/path/to/this/repo"
jupyter lab notebooks/train_kaldi.ipynb
```

Run cells in order, top to bottom. Every stage is wrapped in
`stage(name, done, fn)`, which skips work whose output already exists —
re-running after an interruption only redoes whatever didn't finish.

**`notebooks/evaluate_elevenlabs.ipynb`, `notebooks/evaluate_kaldi.ipynb`,
`notebooks/compare.ipynb`** (plain Python, Windows or Linux, no WSL/Kaldi
dependency): `pip install pandas pyarrow jiwer matplotlib`, plus
`python-dotenv` and `elevenlabs` for `evaluate_elevenlabs.ipynb` (needs a
git-ignored `.env` at the repo root with `ELEVENLABS_API_KEY` --
`load_dotenv()`'s default upward search finds it fine from `notebooks/`).


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

`CORPUS_DIR` (default `../data/bisaya_audio`, relative to `notebooks/`)
holds Parquet shards, one row per utterance, with a nested `audio` struct
column and a `speaker_id`/`transcript` per row — not pre-split into
train/test. `train_kaldi.ipynb` splits it **by speaker**, ~80/20, fixed
seed 42 (checked invariant: `train_speakers.isdisjoint(test_speakers)`).
`finetune_whisper.ipynb` (on Kaggle) recomputes the identical split
independently from the same seed, rather than sharing state with
`train_kaldi.ipynb` across two different machines/environments.

`evaluate_kaldi.ipynb`, `evaluate_elevenlabs.ipynb`, and
`finetune_whisper.ipynb` all load every Parquet shard the same way
(`sorted()` glob order, `pd.concat(..., ignore_index=True)`) and stamp a
`corpus_index` column (each row's position in that concatenation). This
is the join key `compare.ipynb` uses to line up the same utterances
across all three systems' `results.csv` exports, and it's also how Kaldi
utterance IDs (`{speaker_id}-{corpus_index:06d}`) get mapped back to
corpus metadata. **Keep every notebook's corpus-loading code in that
exact order** — the join breaks silently otherwise.

## `output/` and `models/` layout

Both gitignored (reproducible build output, same as `data/`):

```
output/
  tri3/                    # train_kaldi.ipynb: full exp/tri3 (model + decode + logs)
  kaldi/results.csv        # evaluate_kaldi.ipynb: raw reference/prediction/WER/CER/metadata
  elevenlabs/results.csv   # evaluate_elevenlabs.ipynb: same shape, for ElevenLabs Scribe
  whisper/results.csv      # finetune_whisper.ipynb's eval section: same shape, for fine-tuned Whisper
                            # (downloaded from Kaggle's Output tab, dropped in manually)
  whisper/results_pretrained.csv  # same notebook's pre-fine-tuning baseline ablation -- NOT read by compare.ipynb
models/
  tri3/                    # curated subset of output/tri3/ -- just what's needed to decode new audio
```

None of the `results.csv` files have `norm_*` columns — see "Normalization
lives in exactly one place" above.

## Whisper fine-tuning (`notebooks/finetune_whisper.ipynb`, on Kaggle)

Unlike `train_kaldi.ipynb` -> `compare.ipynb`, this notebook **does** feed
into the benchmark -- it's system 3, and its eval section's
`output/whisper/results.csv` is one of the three files `compare.ipynb`
reads. It just can't run locally (needs a GPU), so it lives on Kaggle as
the hosted notebook `troymerales/finetune-whisper` (kernel id
131784027), and the local copy under `notebooks/finetune_whisper.ipynb`
is a synced-down mirror, not something you run directly. A top cell
("Claude Edit Log") tracks the version history of fixes pushed directly
to the Kaggle copy -- check it (and the actual `current_version_number`
via the Kaggle API/UI) before assuming the local mirror matches what's
live, since edits happen on Kaggle first and get synced down, not the
other way around.

Fine-tunes `openai/whisper-small` on this project's actual Bisaya corpus
(GPU quota, Kaggle Secrets for `HF_TOKEN`, corpus attached as a Kaggle
Dataset -- see the notebook's own "Kaggle Setup" section), pushing the
result to the Hugging Face Hub (`troxyz1268/whisper-small-bisaya`). Uses
`language="tl"` (Tagalog) as Whisper's closest built-in code -- there's
no Cebuano/Bisaya token. Below the training cells, two further sections:

- **"Evaluate on Held-Out Test Set"** -- loads the fine-tuned checkpoint
  fresh from the Hub (not the in-kernel trained objects, so it's correct
  whether or not training ran in that session), evaluates it on the same
  19-utterance held-out test set `evaluate_kaldi.ipynb`/
  `evaluate_elevenlabs.ipynb` use locally (recomputes the speaker split
  independently, seed 42), and exports `output/whisper/results.csv` for
  `compare.ipynb`. Supports resuming from a precomputed checkpoint
  attached as a Kaggle Dataset Input (Kaggle wipes `/kaggle/working/` on
  every kernel stop/restart, so a finished run's checkpoint doesn't
  survive on its own) -- found automatically by filename via a recursive
  glob (`Path("/kaggle/input").glob("**/<filename>.parquet")`), since
  this environment nests attached inputs three levels deep
  (`/kaggle/input/datasets/<user>/<slug>/...`), not the flat
  `/kaggle/input/<slug>/...` some Kaggle docs assume.
- **"Compare Pre- vs. Post-Fine-Tuning"** -- runs the *original,
  unmodified* `openai/whisper-small` checkpoint over the same held-out
  set as a baseline ablation, exporting `output/whisper/results_pretrained.csv`
  separately -- **not** read by `compare.ipynb`. Three matplotlib charts,
  each showing pre- and post-fine-tuning together (pooled WER/CER,
  paired per-utterance WER, error composition).

**Kaggle-environment gotchas** (hard-won from real runs):
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
- **`torch.cuda.is_available()` only confirms the driver sees a GPU, not
  that the installed torch build has kernels for it.** Confirmed via a
  real `CUDA error: no kernel image is available for execution on the
  device` -- on a T4, from skipping the "Prepare Environment" reinstall
  cells; on an assigned Tesla P100 (compute capability 6.0/sm_60), even
  with those cells run, since Kaggle's default preinstalled
  `torch==2.13.0+cu130` dropped kernel support for Pascal-class GPUs
  entirely. Device selection should run a real tiny op on `cuda`
  (`torch.zeros(1, device="cuda") + 1`) and fall back to CPU if that
  raises, instead of trusting `is_available()` alone; and the torch
  reinstall in "Prepare Environment" targets the `cu126` wheel index
  specifically (`pip install --force-reinstall torch==<version>
  --index-url https://download.pytorch.org/whl/cu126`), which still
  covers Pascal alongside newer architectures, unlike `cu130`.
- **Kaggle wipes `/kaggle/working/` on every kernel stop/restart** --
  a checkpoint parquet from a finished (or partially finished)
  transcription run doesn't survive on its own. The eval section's
  checkpoint-loading cells check for a precomputed checkpoint attached as
  a Kaggle Dataset Input before falling back to the normal resumable-load
  logic, found by filename via a **recursive** glob
  (`Path("/kaggle/input").glob("**/<filename>")`) -- this environment
  nests attached inputs three levels deep
  (`/kaggle/input/datasets/<user>/<slug>/...`), not the flat
  `/kaggle/input/<slug>/...` some Kaggle docs assume (confirmed via
  `find /kaggle/input -name "*.parquet"` against a real attached input).

## Deployment demo (`deploy/`)

Two standalone Streamlit UIs for trying the ASR systems interactively --
separate from the benchmark notebooks above, not for computing WER/CER
(see `deploy/README.md` for full setup/run instructions). Built with
Streamlit rather than Gradio: Hugging Face Spaces started requiring a
PRO account for Gradio (and Docker) Spaces as of mid-2026, even on free
CPU hardware, so both apps target Streamlit Community Cloud instead,
which is still free for public apps. Split into two apps because they
target different audiences and environments:

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
    README.md              # description shown on the deployed app
```

- **`local_app.py`** -- for advanced users with the full local
  environment set up (WSL2/Ubuntu + built Kaldi checkout + exported
  `models/tri3/` for Kaldi, an `ELEVENLABS_API_KEY` for ElevenLabs).
  Model selection is a `st.multiselect` (Kaldi/ElevenLabs/Whisper, all
  checked by default) -- transcript boxes are rendered only for what's
  checked, since this is an experiment comparing systems, not a product
  that picks one. Each engine's failure is caught and shown in its own
  output box rather than blocking the others; an ElevenLabs 401/429 (out
  of API credits, or an account flagged for unusual activity) is
  specifically caught as `elevenlabs_infer.QuotaExceededError` and
  surfaced via a `st.empty()` placeholder reserved at the top of the
  page, so the warning renders above the results regardless of when in
  the script it's actually set.
- **`prod_app.py`** -- Whisper-only, no engine picker, meant for
  lightweight cloud hosting (Streamlit Community Cloud). Kaldi is
  omitted entirely: it needs a compiled Kaldi checkout under WSL/C++,
  which standard cloud containers can't provide. Written to be
  self-contained (no imports outside `deploy/prod/`) so the folder can
  be deployed as its own unit; the model is loaded once per server
  process via `@st.cache_resource`.

Both apps write uploaded/recorded audio (`st.file_uploader` +
`st.audio_input`) to a temp file before passing it to the inference
functions, which all expect a file path, not raw bytes -- cleaned up in
a `finally` block after each transcription.

Both load `troxyz1268/whisper-small-bisaya` (the checkpoint
`finetune_whisper.ipynb` pushes to the Hub) from the Hub by default via
`BISAYA_WHISPER_MODEL_ID` -- override for a different Hub repo or a local
export. Both read the one shared `deploy/.env` (see `deploy/.env.example`
for the full variable list, and `deploy/README.md` for setup) -- not a
per-app `.env`, by deliberate choice, to avoid keeping two copies of the
same secrets in sync.
