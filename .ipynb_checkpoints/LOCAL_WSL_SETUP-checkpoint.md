# Local WSL2 Setup — Bisaya ASR Training

This project's training workflow has moved off Kaggle and onto a local
machine running **WSL2 / Ubuntu**. The active notebook is
[`wsl_train.ipynb`](wsl_train.ipynb). [`kaggle_train.ipynb`](kaggle_train.ipynb)
is left unchanged as a reference for the previous Kaggle-hosted workflow
and is no longer run.

## Environment

- **Host**: Windows, with **WSL2** running **Ubuntu**.
- **Kaldi**: already cloned at `~/kaldi` inside WSL. `wsl_train.ipynb`
  never runs `git clone` for it — it only verifies the checkout looks
  complete and builds `tools/` (OpenFST) and `src/` against it if that
  hasn't been done yet. Override the location with the `KALDI_ROOT`
  environment variable if your checkout isn't at `~/kaldi`.
- **KenLM**: not pre-installed as a separate thing to track — the notebook
  looks for a system `lmplz` first (`shutil.which("lmplz")`), and only if
  none is found builds one from source inside `~/kaldi/tools/kenlm`
  (Kaldi's own `install_kenlm_query_only.sh` deliberately doesn't build
  `lmplz`, so a full build is required either way). If you already have a
  system-wide KenLM with `lmplz` on `PATH`, the notebook reuses it instead
  of building a second copy.
- **Required system dependencies** (installed via `apt-get`, Section 3 of
  the notebook): `build-essential automake autoconf libtool subversion git
  zlib1g-dev gfortran libatlas-base-dev sox perl cmake libboost-all-dev
  libeigen3-dev`.

## Windows ↔ WSL paths

WSL2 mounts your Windows drives under `/mnt/`:

```
C:\Users\<you>\...   ->   /mnt/c/Users/<you>/...
D:\ASR\dataset        ->   /mnt/d/ASR/dataset
```

This project's preferred strategy is to **keep large datasets and project
files on Windows** and reference them from WSL through that `/mnt/...`
bind mount, rather than copying them into the WSL/Ubuntu filesystem. The
project directory itself (including `wsl_train.ipynb`) stays on Windows;
Jupyter is launched from inside WSL against that same Windows-mounted
directory (see "Running" below).

**Exception — Kaldi's own working directory.** Kaldi's build and training
stages create very large numbers of small files: object files while
compiling `src/`; then, per split, per-utterance `.wav`/`.ark`/`.scp`
shards, alignment logs, and lattices while extracting features, training,
and decoding. On WSL2, paths under `/mnt/...` are bridged to the Windows
NTFS volume through the 9P/DrvFs protocol, which is dramatically slower
than WSL2's native ext4 filesystem for exactly that many-small-file access
pattern — this is a well-known, general WSL2 characteristic, not specific
to Kaldi. So `WORK_DIR` (which holds the recipe scaffolding plus `data/`,
`mfcc/`, and `exp/`) defaults to a directory under `$HOME` inside WSL, not
a `/mnt/...` path. See "Storage considerations" below for exactly what
that means file-by-file.

## Dataset configuration

Configure the dataset location with the `BISAYA_CORPUS_DIR` environment
variable before launching Jupyter, e.g.:

```bash
export BISAYA_CORPUS_DIR=/mnt/d/ASR/dataset/bisaya_audio
```

If unset, it defaults to `data/bisaya_audio` **relative to wherever the
notebook's kernel is running from** — i.e. this project's own
`data/bisaya_audio/` folder next to `wsl_train.ipynb`, which is where the
dataset already lives in this repo. Nothing in the notebook hardcodes a
Windows username or drive letter; the default is a plain relative path,
and the override is a plain environment variable.

Similarly, `BISAYA_RESULTS_DIR` (default: `output`, also relative to the
notebook — i.e. this project's own `output/` folder) controls where final
results are copied at the end of a run —
see Section 15 / "Storage considerations" below.

## Workflow

`wsl_train.ipynb` implements the same single pipeline as
`kaggle_train.ipynb`, unchanged except for what had to change to run
locally (see the notebook's own intro cell for the itemized diff):

1. **Configuration** — resolves `WORK_DIR`, `KALDI_ROOT`, `CORPUS_DIR`,
   `RESULTS_DIR`, all overridable via environment variables.
2. **Install dependencies** — `apt-get`-installs the Ubuntu build
   toolchain (via `sudo`), then `pip`-installs `pandas`/`pyarrow`/`tqdm`.
3. **Verify Kaldi checkout, build tools + KenLM** — checks `~/kaldi` looks
   complete (no cloning), builds `tools/` (OpenFST) if needed, resolves or
   builds `lmplz`.
4. **Build Kaldi binaries (`src/`)** — the slow step (30–90 min cold).
5. **Recipe scaffolding** — writes `path.sh`/`cmd.sh`, symlinks
   `steps/`/`utils/` from Kaldi's `egs/wsj/s5`.
6. **Data loading** — reads every Parquet shard in `CORPUS_DIR` directly
   with `pandas.read_parquet()` and concatenates in memory.
7. **Speaker-independent train/test split** (~80/20, fixed seed) and Kaldi
   data-dir construction (`wav.scp`/`text`/`utt2spk`), writing per-utterance
   `.wav` files under `WORK_DIR` (not `CORPUS_DIR`).
8. **Speed perturbation** (0.9×/1.0×/1.1×) on the training set only.
9. **Lexicon + phoneme data** — a rule-based grapheme-to-phoneme lexicon
   constrained to the **PS27** 27-monophone inventory, then
   `prepare_lang.sh`.
10. **Language model** — a 2-gram word-level LM via KenLM's `lmplz`,
    converted to a Kaldi `G.fst` with `format_lm.sh`.
11. **MFCC + CMVN feature extraction** (25 ms window, 10 ms shift,
    per-speaker CMVN).
12. **HMM-GMM training** — monophone → triphone (delta features) →
    LDA+MLLT → SAT (speaker-adaptive training). SAT (`tri3`) is the final
    model.
13. **Decode + evaluate** — builds the `tri3`/2-gram decode graph, decodes
    the test set, sweeps the LM weight (1–25), prints the best WER.
14. **Copy final results to Windows** — copies `exp/tri3` (final model,
    decode graph, WER output) from `WORK_DIR` to `RESULTS_DIR`.

Every stage checks for its own completed output first and skips straight
past it if found, so re-running the notebook top to bottom after an
interrupted kernel or a machine restart only re-does whatever didn't
finish last time. Unlike `kaggle_train.ipynb`, there's no tar/untar
checkpoint step for this — WSL's disk is already persistent across
sessions.

## Dependencies

**Ubuntu packages** (`apt-get`, requires `sudo`):
`build-essential automake autoconf libtool subversion git zlib1g-dev
gfortran libatlas-base-dev sox perl cmake libboost-all-dev libeigen3-dev`

**Python packages** (`pip`, installed by the notebook itself in Section 3):
`pandas`, `pyarrow`, `tqdm`

**Python packages you must install yourself before the notebook can even
open** (the notebook can't bootstrap the environment that runs it):
`jupyterlab` (or `notebook`) and `ipykernel`

**Kaldi build dependencies**: satisfied by the Ubuntu packages above
(`build-essential`, `automake`, `autoconf`, `libtool`, `subversion`, `git`,
`zlib1g-dev`, `gfortran`, `libatlas-base-dev`, `sox`, `perl`).

**KenLM build dependencies**: `cmake`, `libboost-all-dev`, `libeigen3-dev`
(all in the Ubuntu package list above) — needed only if no system `lmplz`
is already on `PATH`.

## Running

This Ubuntu installation manages Python packages via `apt` (PEP 668
"externally managed environment") — installing packages straight into the
system Python with `pip` is blocked. Set up a virtual environment once,
inside WSL:

```bash
python3 -m venv ~/asr-venv
source ~/asr-venv/bin/activate
pip install jupyterlab ipykernel pandas pyarrow tqdm
```

Then, each time you want to work on this notebook:

```bash
# from a WSL terminal
source ~/asr-venv/bin/activate
cd "/mnt/c/path/to/this/project"      # wherever this repo actually lives on Windows
jupyter lab wsl_train.ipynb
```

`sudo apt-get` (Section 3 of the notebook) needs a cached sudo timestamp
to run non-interactively from inside a notebook's subprocess — if that
cell appears to hang, run the same `apt-get install ...` line once from a
plain WSL terminal (which will prompt for your password normally), then
re-run the cell; it will find everything already installed and skip
straight through.

Set any of `BISAYA_CORPUS_DIR`, `BISAYA_RESULTS_DIR`, `BISAYA_WORK_DIR`,
`KALDI_ROOT` before launching `jupyter lab` (`export VAR=...` in the same
shell) if the defaults don't match your machine.

## Storage considerations

**Stays on Windows** (accessed through `/mnt/...`, never copied into WSL):
- The dataset itself (`CORPUS_DIR`, Parquet shards) — read directly.
- `wsl_train.ipynb` and this repo's other project files.
- Final results (`RESULTS_DIR`) — the trained SAT model, its decode
  graph, and decode/WER output, copied there once decoding finishes.

**Lives inside WSL** (`WORK_DIR`, default `~/bisaya_asr`, native ext4 —
not copied from/into Windows at all, generated fresh from the dataset and
Kaldi each run):
- Kaldi recipe scaffolding (`path.sh`, `cmd.sh`, `steps/`, `utils/`
  symlinks).
- Per-utterance `.wav` files written out from the dataset.
- `data/` (Kaldi data dirs: `wav.scp`, `text`, `utt2spk`, lexicon, lang
  directories, LM files).
- `mfcc/` (MFCC/CMVN feature `.ark`/`.scp` files).
- `exp/` (GMM training stages, alignments, decode graph, decode lattices,
  logs) — except `exp/tri3`, which gets copied out to Windows in Section
  15 once training/decoding finish.

This split exists because Kaldi's build and training stages create very
large numbers of small files, and that access pattern is measurably
slower over WSL2's `/mnt/...` Windows bind mount than on native ext4 — see
"Windows ↔ WSL paths" above. Nothing here is a duplicate copy of the
dataset: the dataset is read from Windows once per run and never written
back to; the WSL-side files are Kaldi's own generated intermediates, not
data that also exists on the Windows side.

`~/kaldi` itself (the Kaldi checkout, plus its `tools/kenlm` build) also
lives inside WSL, for the same reason, and is expected to already be
there per this project's migration brief — this notebook never touches it
beyond building against it.
