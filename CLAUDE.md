# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A benchmark comparing two Bisaya ASR systems on the same corpus:

1. A **Kaldi HMM-GMM model trained from scratch** — a 2-gram, 3-state,
   speaker-adaptive-trained (SAT) HMM-GMM using the PS27 27-phoneme set,
   reproducing the best-performing Bisaya configuration from Ing (2023),
   *Filipino and Bisaya ASR System using TDNN-HMM towards application in a
   healthcare chatbot* (De La Salle University master's thesis; full text
   and the derived implementation blueprint are in `references/`). Every
   neural (DNN/TDNN) variant that thesis tested for Bisaya scored equal to
   or worse than this HMM-GMM configuration, which is why there is no
   TDNN/DNN stage here.
2. **ElevenLabs Scribe**, a commercial ASR API, evaluated zero-shot on the
   same corpus for comparison.

There is no source package, build system, linter, or test suite — this is
four Jupyter notebooks, each a runnable pipeline stage, validated
empirically by the WER/CER printed at the end of a run.

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
