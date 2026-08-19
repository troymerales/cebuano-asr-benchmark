# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A reproduction of one specific pipeline from Ing (2023), *Filipino and Bisaya
ASR System using TDNN-HMM towards application in a healthcare chatbot*
(De La Salle University master's thesis) — the best-performing model the
thesis found for Bisaya: a **2-gram, 3-state, speaker-adaptive-trained (SAT)
HMM-GMM model using the PS27 27-phoneme set** (5.41% WER in the thesis).
That choice is deliberate and documented in `conclusion.md` (the thesis's
own "Conclusions and Recommendations") and in each training notebook's own
Section 1 — every neural (DNN/TDNN) variant the thesis tested for Bisaya
scored equal to or worse than this HMM-GMM configuration, so there is no
TDNN/DNN stage implemented here. There is no source package, build system,
linter, or test suite — this is a set of Jupyter notebooks, each one a
runnable, human-read pipeline, validated empirically by the WER/CER a run
prints at the end, not by an automated test suite.

There are two independent, non-interacting experiments in this repo:
1. **Training a model from scratch with Kaldi** (`wsl_train.ipynb` and its
   ancestors, see below).
2. **Evaluating a commercial ASR API** (`main.ipynb`, ElevenLabs Scribe)
   against the same corpus, for comparison. Does not depend on the Kaldi
   notebooks having been run, and vice versa.

`Bisaya_Filipino_ASR_Reproduction_Guide.md` is the full implementation
blueprint distilled from the thesis (background/theory only where it
explains an implementation decision); it covers the full HMM-GMM→TDNN-HMM
design space the thesis explored. The notebooks in this repo implement only
the one pipeline `conclusion.md` identifies as best for Bisaya, not that
whole space.

## The training-notebook lineage — read this before touching any of them

These four notebooks are **not independent alternatives** — each is a
rewrite of the previous one for a new environment, implementing the *same*
pipeline. Changes to the actual ASR logic (lexicon rules, split seed, GMM
recipe, decode/LM-weight sweep) should conceptually apply to all of them;
environment-only changes (paths, install steps, checkpointing strategy)
should not leak backward.

1. **`train.ipynb`** — the original, portable version of the pipeline.
   Explains every non-paper-specified decision in its Section 1 (model
   architecture, phoneme set, n-gram order, HMM topology, CMVN scope, speed
   perturbation, LM weight sweep, split seed) — this table is the canonical
   reference; later notebooks just point back to it instead of repeating it.
2. **`kagglebasis.ipynb`** — an early, now-superseded Kaggle data-loading
   experiment. It combined all Parquet shards with
   `pa.concat_tables()` + `pq.write_table()`, then read the combined file
   back — which breaks on that Kaggle image's pyarrow for the nested
   `audio` struct column (`ArrowNotImplementedError` on multi-row-group
   reads, or `ArrowInvalid: offset overflow` if forced into one row group).
   Don't resurrect that combine-then-rewrite approach.
3. **`kaggle_train.ipynb`** — a Kaggle-hardened rewrite of `train.ipynb`:
   points at the exact Kaggle input dataset path, and — the fix for
   `kagglebasis.ipynb`'s bug — loads every Parquet shard straight into
   pandas and concatenates in memory, no intermediate rewrite. Also made
   *every* stage (not just GMM training) individually resumable via a
   `stage()` helper, since Kaggle sessions get killed. **Kept unchanged as
   a historical reference — the project has moved off Kaggle. Do not edit
   this file; do not run it.**
4. **`wsl_train.ipynb`** — **the active notebook.** A local-WSL2/Ubuntu
   migration of `kaggle_train.ipynb`, done with minimal changes (see its
   own intro cell for the itemized diff from `kaggle_train.ipynb`). This is
   the one to run and the one to modify for any change to the actual
   pipeline.

`LOCAL_WSL_SETUP.md` documents `wsl_train.ipynb` specifically: environment
assumptions, Windows↔WSL path handling, the full stage-by-stage workflow,
dependencies, and a from-scratch step-by-step run guide. Read it before
changing anything path- or environment-related in `wsl_train.ipynb`.

## Running the training pipeline

No package manager / lockfile in this repo — dependencies are plain
`apt`/`pip` installs, documented in full in `LOCAL_WSL_SETUP.md` ("Running"
and "Dependencies" sections). Short version, from inside WSL2/Ubuntu:

```bash
python3 -m venv ~/asr-venv
source ~/asr-venv/bin/activate
pip install jupyterlab ipykernel pandas pyarrow tqdm
cd "/mnt/c/path/to/this/repo"
jupyter lab wsl_train.ipynb
```

Then run `wsl_train.ipynb`'s cells in order, top to bottom — later cells
depend on earlier ones having run. Every stage is wrapped in a `stage()`
call that checks whether its output already exists before doing any work,
so re-running top to bottom after an interruption only redoes whatever
didn't finish. There is no separate build/lint/test command; "does it
work" is judged by whether each stage's expected output file appears, and
ultimately by the WER printed at the end of the decode stage.

**Known environment gotchas** (hit and fixed during the Kaggle→WSL
migration, worth knowing before debugging what looks like a new issue):
- `libatlas-base-dev` isn't packaged on newer Ubuntu releases. Kaldi's
  math library is built from source instead, via Kaldi's own
  `tools/extras/install_openblas.sh`, with `src/configure` pointed at it
  via `--mathlib=OPENBLAS --openblas-root=...`. Don't re-add
  `libatlas-base-dev` to the apt install list.
- `sudo apt-get` run from inside a Jupyter cell's subprocess has no TTY to
  prompt for a password and fails immediately — run the apt install once
  by hand in a plain WSL terminal first (see `LOCAL_WSL_SETUP.md` step 9).
- **Editing `wsl_train.ipynb` directly while the user has it open in a live
  Jupyter session is unreliable** — Jupyter's autosave can silently
  overwrite an external edit to the `.ipynb` file with its own stale
  in-memory copy. Prefer describing the exact cell change for the user to
  paste in themselves over editing the file directly, unless they've
  confirmed the notebook isn't open live.

For `main.ipynb` (the ElevenLabs Scribe comparison): needs
`pandas`, `python-dotenv`, `elevenlabs`, and a `.env` file (git-ignored)
providing `ELEVENLABS_API_KEY`.

## Pipeline architecture (shared across `train.ipynb` / `kaggle_train.ipynb` / `wsl_train.ipynb`)

Each notebook is one linear sequence of stages operating on the same
`WORK_DIR` (holding the Kaldi checkout, `data/`, `mfcc/`, `exp/`) and the
same `CORPUS_DIR` (Parquet shards under `data/bisaya_audio/`, one row per
utterance with a nested `audio` struct column and a `speaker_id`/
`transcript` per row — not pre-split into train/test). The stage sequence:

1. **Kaldi setup** — build Kaldi's `tools/` (OpenFST) and `src/` from
   source, plus KenLM (Kaldi's bundled installer deliberately omits
   `lmplz`, so KenLM is built directly instead), then symlink `steps/`/
   `utils/` from Kaldi's `egs/wsj/s5` recipe and write `path.sh`/`cmd.sh`.
2. **Data loading + split** — every Parquet shard loaded into pandas and
   concatenated in memory (see the `kagglebasis.ipynb` note above for why
   not to rewrite this as a combined-Parquet step). Split **by speaker**
   (not utterance), ~80/20, fixed seed 42, so the split is reproducible and
   speaker-independent — this seed is a checked invariant
   (`train_speakers.isdisjoint(test_speakers)`), not just a default.
3. **Kaldi data-dir construction** — `build_kaldi_data_dir()` writes each
   utterance's audio out as an individual `.wav` (piped through `sox` to a
   consistent 16 kHz mono) plus `wav.scp`/`text`/`utt2spk`, one call per
   split.
4. **Speed perturbation** — standard Kaldi 3-way (0.9×/1.0×/1.1×), training
   split only.
5. **Lexicon (PS27)** — `word_to_phones()` is a hand-written, deterministic
   grapheme-to-phoneme mapping constrained to PS27's 27 monophones (an
   `assert` enforces every produced phone is in that set). This is a rule-
   based approximation of the thesis's own transcriber-produced PS27
   dictionary, not a learned or paper-sourced G2P model — see each
   notebook's Summary section for that caveat. Changing phoneme rules here
   is the main lever for lexicon-quality experiments.
6. **Language model** — KenLM `lmplz` (2-gram, `--discount_fallback`) on
   the training transcripts, converted to a Kaldi `G.fst` via
   `utils/format_lm.sh`. 2-gram is a `conclusion.md`-driven choice, not a
   default — don't casually bump the order without re-checking that
   rationale.
7. **Features** — MFCC (Kaldi defaults: 25 ms/10 ms) + per-speaker CMVN,
   computed separately for the (speed-perturbed) train split and the test
   split.
8. **GMM training progression** — monophone → triphone (delta features,
   `tri1`) → LDA+MLLT (`tri2`) → SAT (`tri3`, **the final model**), each
   stage aligning on the previous stage's output before the next stage
   trains. SAT/`tri3` is what gets decoded, not any earlier stage.
9. **Decode + evaluate** — `mkgraph.sh` against the 2-gram `G.fst` and the
   `tri3` model, `decode_fmllr.sh` on the test set with an LM-weight sweep
   (1–25), then `utils/best_wer.sh` to print the best WER. This final
   number is the thing to compare against `conclusion.md`'s 5.41% figure
   (expect a gap — different, smaller corpus).

Every one of these stages is wrapped in a `stage(name, done, fn)` call
(`done()` checks for the stage's expected output file) — this is *the*
pattern used for resumability throughout, not just in one or two places.
When adding a new stage, follow it rather than open-coding an `if`.

## `wsl_train.ipynb`-specific layout

- `KALDI_ROOT` defaults to `~/kaldi` and is assumed already cloned —
  `wsl_train.ipynb` never runs `git clone` for Kaldi. `WORK_DIR` (Kaldi
  checkout/build artifacts, `data/`, `mfcc/`, `exp/`) also lives on the
  WSL-native filesystem (`~/bisaya_asr` by default), *not* under `/mnt/...`
  — Kaldi's build and training stages create very large numbers of small
  files, which is measurably slower over WSL2's Windows bind mount than on
  native ext4.
- `CORPUS_DIR` and `RESULTS_DIR`, by contrast, default to Windows-hosted,
  relative paths (`data/bisaya_audio`, `output/`, both next to the
  notebook) — reading a handful of large Parquet files, and writing the
  final model/graph/WER output back out, aren't the many-small-file
  pattern that's slow over `/mnt/...`.
- All four of `KALDI_ROOT`/`WORK_DIR`/`CORPUS_DIR`/`RESULTS_DIR` are
  overridable via environment variables (`KALDI_ROOT`, `BISAYA_WORK_DIR`,
  `BISAYA_CORPUS_DIR`, `BISAYA_RESULTS_DIR`) — nothing is hardcoded to a
  specific username or drive letter.
- Final artifacts (`exp/tri3`: trained model, decode graph, WER output) are
  copied from `WORK_DIR` back out to `RESULTS_DIR` on Windows in the
  notebook's last stage, so they're browsable outside WSL.

See `LOCAL_WSL_SETUP.md` for the full rationale and a complete stage-by-
stage walkthrough.
