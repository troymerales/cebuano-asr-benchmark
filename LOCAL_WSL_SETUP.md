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
  zlib1g-dev gfortran sox perl cmake libboost-all-dev libeigen3-dev unzip`.
  (`unzip` is required by Kaldi's own `tools/extras/check_dependencies.sh`
  — without it, `make` in `tools/` fails at its `check_required_programs`
  step with `unzip is not installed`.)
- **Math library (OpenBLAS)**: Kaldi needs a BLAS/LAPACK implementation to
  build. `libatlas-base-dev` — what this pipeline used to `apt`-install for
  this — isn't in the package repos on every Ubuntu release (it's gone on
  newer ones). Section 4 instead builds OpenBLAS from source via Kaldi's
  own `tools/extras/install_openblas.sh` (which is what Kaldi's dependency
  checker recommends anyway, regardless of what your distro happens to
  package), into `~/kaldi/tools/OpenBLAS/install`, and `src/configure` is
  pointed at it with `--mathlib=OPENBLAS --openblas-root=...`.
- **`sph2pipe` (bundled with Kaldi's SCTK, built as part of `tools/`) can
  fail to compile on newer GCC** (confirmed on GCC 15) with
  `shorten_x.c: error: too many arguments to function 'word_get'; expected
  0, have 1` — its ~2011-era K&R-style C is rejected by GCC's now-stricter
  defaults. Fix: build `tools/` with `CCFLAGS=-std=gnu17` (e.g.
  `make -j$(nproc) CCFLAGS=-std=gnu17` in `~/kaldi/tools`) — this makes
  `sph2pipe`'s empty-parameter-list declarations mean "unspecified
  arguments" again instead of "exactly zero," which is all this old code
  needs. The flag propagates automatically into `sph2pipe`'s sub-`make`.
- **OpenBLAS 0.3.13 itself (the version Kaldi's `install_openblas.sh`
  pins) also fails to build on newer GCC** (confirmed on GCC 15), with two
  *different* errors from the same underlying cause as `sph2pipe` above —
  GCC 14+ turned several old-C warnings into hard errors by default:
  - `-Wincompatible-pointer-types`, in an AVX-512 kernel file
    (`sasum_microk_skylakex-2.c`, passing a `float*` where `_mm_loadu_si128`
    now wants `const __m128i_u*`).
  - `-Wimplicit-function-declaration`, in OpenBLAS's own generated
    `linktest.c` sanity check (calls exported symbols without prototypes).

  Fix: `wsl_train.ipynb`'s `_install_openblas()` lets Kaldi's stock script
  do the download/extract (tolerating its now-expected failure at the
  `make` step), then re-runs the actual build+install itself with
  `CC="gcc -Wno-error=implicit-function-declaration
  -Wno-error=incompatible-pointer-types -Wno-error=int-conversion"` — this
  downgrades that whole GCC 14+ warning family back to non-fatal for this
  one build, without touching Kaldi's own script. Confirmed working
  end-to-end (`Install OK!`) against this exact environment.
- **KenLM's `CMakeLists.txt` requires a `system` Boost component that no
  longer exists to find** — `CMake Error ... Could NOT find Boost
  (missing: system)`, even though `program_options`/`thread`/
  `unit_test_framework` are all found fine. Boost.System has been
  header-only for years; this Ubuntu's Boost (1.90) finally dropped the
  compiled compatibility stub package entirely (`libboost-system-dev`
  isn't even in the repos), so there's no `libboost_system.*` file
  anywhere to find, and KenLM's `find_package(Boost REQUIRED COMPONENTS
  ... system ...)` fails outright rather than just skipping it. Nothing in
  KenLM actually links against a compiled Boost.System. Fix (applied in
  `_install_kenlm()`, right after cloning, before `cmake`):
  `sed -i '/^  system$/d' CMakeLists.txt` — drops that one component from
  the requested list. Confirmed working end-to-end (`lmplz` builds and
  runs) against this exact environment.
- **`compute-mfcc-feats` (the binary Section 5's `stage()` check uses to
  detect a finished `src/` build) lives in `src/featbin/`, not
  `src/bin/`.** The original path (inherited from `kaggle_train.ipynb`)
  was simply wrong — Kaldi puts feature-extraction binaries in their own
  `featbin/` directory, separate from `bin/`'s generic ones. With the
  wrong path, the build itself was fine, but `stage()` could never see it
  as complete and would print a false "expected binary not found" warning
  on every future run, re-attempting the (harmlessly fast, thanks to
  `make`'s own incremental tracking) build every time. Fixed in
  `wsl_train.ipynb` to point at `src/featbin/compute-mfcc-feats`.
- **`utils/validate_data_dir.sh` can false-positive on
  "non-printable characters"** in `text` on a fresh Ubuntu install. That
  check specifically looks for the locale `C.UTF-8` or, failing that,
  `en_US.UTF-8` — this Ubuntu only has `C.utf8` installed (different exact
  name; `locale -a` lists `C`, `C.utf8`, `POSIX`, nothing else), so neither
  matches, and the script silently falls back to the plain `C` locale for
  its printable-character check, which misclassifies ordinary non-ASCII
  UTF-8 bytes (e.g. accented Bisaya characters) as "non-printable." Not a
  real data problem — confirmed by rerunning the same check with the
  locale that's actually installed (`LC_ALL=C.utf8`), which finds zero
  flagged lines. Fix: `build_kaldi_data_dir()` in `wsl_train.ipynb` passes
  `--non-print` to skip this specific (broken, in this environment) check;
  everything else `validate_data_dir.sh` checks still runs normally. If
  you'd rather have the check fully active, the alternative is generating
  the missing locale yourself (`sudo apt-get install locales && sudo
  locale-gen en_US.UTF-8`) instead of using `--non-print` — not done here
  since it needs another `sudo` step and the `--non-print` fix is already
  confirmed safe for this corpus.
- **`utils/format_lm.sh` unconditionally runs `gunzip -c` on the ARPA
  file**, regardless of its name/extension — it assumes an already-gzipped
  LM (the Kaldi convention, e.g. from IRSTLM/SRILM), but `lmplz` (Section
  11) writes plain text. Without gzipping first, this fails with `gzip:
  ...2gram.arpa: not in gzip format`, and `arpa2fst` then gets an empty
  stream through the broken pipe (`\data\ section missing or empty`).
  This is a **pre-existing bug inherited unchanged from
  `kaggle_train.ipynb`/`train.ipynb`** (same logic there), not something
  the WSL migration introduced — it just hadn't been hit before. Fixed in
  `wsl_train.ipynb`'s `_build_lm()`: gzips `2gram.arpa` (keeping the
  original with `-k`) before handing it to `format_lm.sh`. Confirmed
  working end-to-end (`Succeeded in formatting LM`) against this exact
  corpus. Separately, expect (and ignore) `arpa2fst` warnings like `word
  '2015' not in symbol table` — the PS27 G2P lexicon (Section 10) silently
  drops purely-numeric transcript tokens (dates, quantities written as
  digits) since they have no letters to map to phones; this is a
  pre-existing, documented lexicon-coverage limitation, not a bug.
- **`corpus_df`/`train_df`/`test_df` (Sections 7-8) can exhaust RAM on a
  small machine if left alive** — they hold the entire corpus's raw audio
  bytes decoded in memory (this repo's Parquet shards are ~1.9 GB
  compressed, several times that decoded), and nothing needs them anymore
  once Section 8 finishes writing every utterance out to its own `.wav`
  file. On Kaggle's ~30 GB-RAM notebooks this was never a problem; on a
  7.6 GB WSL VM it can pin most of available RAM for the rest of the
  session, so a later stage that tries to spawn a subprocess (MFCC
  extraction, GMM training) fails with `OSError: [Errno 12] Cannot
  allocate memory` — not a Kaldi problem, just no memory left to `fork()`
  a new process at all. Confirmed directly: the Jupyter kernel process
  itself was measured at 90%+ of total RAM in this situation. Fixed by
  adding `del corpus_df, train_df, test_df; gc.collect()` at the end of
  Section 8, once those DataFrames are no longer needed. If you hit this
  in an already-running session before reloading the fix, run that same
  cleanup by hand in a new cell rather than restarting the kernel.
- **`steps/make_mfcc.sh` requires `conf/mfcc.conf` by default, and nothing
  ever created it.** Every real `egs/*/s5` Kaldi recipe ships this file
  checked in, but `WORK_DIR` isn't a real recipe directory — Section 6
  only symlinks in `steps/`/`utils/`, not `conf/`. Fails with
  `steps/make_mfcc.sh: no such file conf/mfcc.conf`. Confirmed this is
  another **pre-existing gap inherited unchanged from
  `kaggle_train.ipynb`** (never created there either), not WSL-specific —
  it just hadn't been hit before. None of this pipeline's other scripts
  (`compute_cmvn_stats.sh`, `train_mono.sh`, `align_si.sh`,
  `train_deltas.sh`, `train_lda_mllt.sh`, `train_sat.sh`,
  `decode_fmllr.sh`, `mkgraph.sh`) require a `conf/` file, so this was an
  isolated gap, not a pattern. Fixed in Section 6: writes
  `WORK_DIR/conf/mfcc.conf` with the same content Kaldi's own wsj s5
  recipe uses (`--use-energy=false` — the only non-default MFCC option
  this pipeline uses, matching Section 12's own "Kaldi's MFCC defaults
  already match this" description).
- **GMM training/decoding alignment beams are far too narrow for this
  corpus's utterance lengths, causing widespread alignment failure.**
  `steps/train_mono.sh`, `train_deltas.sh`, `train_lda_mllt.sh`,
  `train_sat.sh`, and `align_si.sh` all default to beam widths tuned for
  short read-speech sentences (`initial_beam=6`/`regular_beam=10` for
  monophone, `beam=10` for the triphone stages, `retry_beam=40`
  everywhere). This corpus's training utterances average **~105 seconds**
  and run up to **~330 seconds** — at the defaults, ~89% of monophone
  alignments failed outright (confirmed directly: 24 of 27 utterances
  failed in one job, even after Kaldi's automatic retry at the widened
  beam). This is a genuine property of this dataset (unusually long
  utterances relative to what these Kaldi recipe scripts assume), not a
  WSL or environment bug — the same failures would occur on any machine.

  Fixed by widening beams well past the defaults everywhere alignment
  happens: `ALIGN_BEAM = 40`, `ALIGN_RETRY_BEAM = 160` (Section 13),
  passed via `--initial-beam`/`--regular-beam`/`--beam`/`--retry-beam` to
  every training stage, plus `--beam 30 --lattice-beam 15` for
  `decode_fmllr.sh` (Section 14, same rationale, decoding's own beam
  units). Confirmed by direct testing this roughly halves the failure
  rate (~89% → ~42-52% at beam=40 on the same job) — **it does not
  eliminate failures entirely.** A residual portion fail regardless of
  beam width; spot-checking one such case showed a long, code-switched
  utterance (an embedded English phrase transcribed inside otherwise
  Bisaya text) where the PS27 G2P lexicon's Bisaya letter-to-phone rules
  don't approximate the actual English pronunciation closely enough for
  alignment to find a viable path — a lexicon-coverage limitation, not
  something beam width fixes.

  What to watch for: monophone's first alignment pass is the worst case
  (the model is still flat-start, with no real acoustic information yet),
  so the failure rate should visibly improve over the next few iterations
  as the model sharpens using whatever did align. If it *doesn't* keep
  dropping after the first couple of realignment iterations, that's the
  signal this corpus's longest/most code-switched utterances need to be
  split into shorter segments before training — a data-preparation change
  beyond what a beam parameter can fix, and out of scope for this
  migration pass.

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
3. **Verify Kaldi checkout, build tools + OpenBLAS + KenLM** — checks
   `~/kaldi` looks complete (no cloning), builds `tools/` (OpenFST) if
   needed, builds OpenBLAS from source via Kaldi's own
   `install_openblas.sh` if needed, resolves or builds `lmplz`.
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
gfortran sox perl cmake libboost-all-dev libeigen3-dev unzip`

**Python packages** (`pip`, installed by the notebook itself in Section 3):
`pandas`, `pyarrow`, `tqdm`

**Python packages you must install yourself before the notebook can even
open** (the notebook can't bootstrap the environment that runs it):
`jupyterlab` (or `notebook`) and `ipykernel`

**Kaldi build dependencies**: satisfied by the Ubuntu packages above
(`build-essential`, `automake`, `autoconf`, `libtool`, `subversion`, `git`,
`zlib1g-dev`, `gfortran`, `sox`, `perl`), plus OpenBLAS — built from source
by the notebook itself (Section 4) via Kaldi's own
`tools/extras/install_openblas.sh`, not an `apt` package (see
"Environment" above for why).

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

## Step-by-step execution guide (assumes zero prior knowledge)

This section walks through every click and every command needed to go
from "nothing open" to a running training pipeline, with no assumed
familiarity with WSL, Linux, virtual environments, or Jupyter. Follow it
top to bottom in order. Every command below is meant to be typed (or
copy-pasted) exactly as written, then run by pressing **Enter**.

### 0. Check WSL2 + Ubuntu are actually installed

Press the **Windows key**, type `PowerShell`, and open it. Run:

```powershell
wsl -l -v
```

You should see a line like `Ubuntu   Running   2` (or `Stopped` instead of
`Running` — that's fine too). If you instead get an error, or Ubuntu isn't
listed, WSL/Ubuntu isn't set up yet — that's a prerequisite for everything
below and outside the scope of this guide (search "install WSL2 Ubuntu"
for Microsoft's official steps, or ask for help getting that far first).
If this project's brief already told you Ubuntu is installed with Kaldi
at `~/kaldi`, you can skip straight to step 1.

### 1. Open an Ubuntu terminal

Still in that PowerShell window (or a fresh one), run:

```powershell
wsl
```

Your prompt will change to something ending in `$` — you are now inside
Ubuntu, not Windows. Every command from here on goes in this same window,
unless a step says otherwise. (If you ever close this window, just repeat
this step to get back in — everything you set up stays saved on disk.)

### 2. Confirm Kaldi is where the notebook expects it

```bash
ls -la ~/kaldi/src/Makefile ~/kaldi/tools/extras/install_kenlm_query_only.sh
```

Both paths should print back without an error. If either says "No such
file or directory," stop here and sort out the Kaldi checkout first — the
notebook is written to assume it's already there and complete, and won't
clone it for you.

### 3. Create a Python virtual environment (one-time setup)

A "virtual environment" is just an isolated folder of Python packages so
installing things for this project doesn't touch or break your system's
Python. You only do this once, ever, on this machine:

```bash
python3 -m venv ~/asr-venv
source ~/asr-venv/bin/activate
pip install jupyterlab ipykernel pandas pyarrow tqdm
```

That last command downloads and installs Jupyter and a few Python
libraries — it can take a couple of minutes. When it finishes, your
prompt will now start with `(asr-venv)`, meaning the virtual environment
is active.

### 4. Find your project folder's path, as seen from WSL

Your project (this folder, containing `wsl_train.ipynb`) lives on
Windows. From WSL, every Windows drive is reachable under `/mnt/`. Take
the Windows path you'd normally see in File Explorer's address bar, e.g.:

```
C:\Users\YourName\Documents\Sugbodoc\speech model
```

and rewrite it by: lowercasing the drive letter, putting `/mnt/` in front
of it, and flipping every `\` to `/`:

```
/mnt/c/Users/YourName/Documents/Sugbodoc/speech model
```

That's the path you'll use in the next step. (If you're not sure of your
exact Windows path, open this project folder in File Explorer, click
once in the empty area of the address bar to reveal the full path as
text, and copy it from there.)

### 5. Go to the project folder and launch Jupyter

Still in the same terminal (the one showing `(asr-venv)`):

```bash
cd "/mnt/c/Users/YourName/Documents/Sugbodoc/speech model"
jupyter lab wsl_train.ipynb
```

(Use your own path from step 4 instead of the example above — keep the
quotes if your path has spaces in it, like this one does.)

This prints a bunch of text ending in a URL that looks like
`http://localhost:8888/lab?token=...`. Jupyter should also open
automatically in your default Windows web browser. If it doesn't, copy
that whole URL and paste it into a browser yourself. **Leave this
terminal window open** — closing it shuts Jupyter down.

### 6. Confirm the notebook opened

You should now see `wsl_train.ipynb` open in the browser tab, showing a
sequence of text explanations and gray code boxes ("cells"). If it opened
to a file browser instead, double-click `wsl_train.ipynb` in the file
list on the left.

### 7. Run the notebook, one cell at a time

Click on the first gray code cell (under "## 2. Configuration"), then
press **Shift+Enter**. That runs the cell and moves you to the next one.
Keep pressing **Shift+Enter** to run each cell in order, top to bottom —
**do not skip ahead or run cells out of order**, since later cells depend
on earlier ones having already run.

Read the printed output under each cell before moving on — it tells you
what happened (paths it resolved, what it installed, what it skipped).

### 8. What to expect, stage by stage

- **Section 2 (Configuration)**: instant. Prints the paths it resolved —
  check `CORPUS_DIR` points at a real folder and doesn't print a warning.
- **Section 3 (Install Dependencies)**: runs `sudo apt-get`, which needs
  your Windows/Ubuntu account password. See step 9 below **before**
  running this cell.
- **Section 4–5 (Build Kaldi)**: the slow part — **30 to 90 minutes**,
  possibly more, the very first time (this includes an OpenBLAS build
  from source, a few extra minutes, downloaded from GitHub the first
  time it runs). The cell will print a wall of compiler output; that's
  normal, not an error. On every run after this one, these cells print
  `[skip]` and finish instantly, because the compiled result is already
  there.
- **Sections 6–14 (data through decoding)**: ranges from seconds to
  maybe 15–30 minutes depending on dataset size and CPU, mostly at the
  MFCC extraction and GMM training steps.
- **Section 14's last line** prints your **Word Error Rate (WER)** — the
  final result of the whole notebook.
- **Section 15**: copies the finished model back out to Windows, into
  the `output/` folder next to this notebook (see "Dataset configuration"
  above).

### 9. About the password prompt in Section 3

`sudo apt-get` cannot ask for your password from inside a Jupyter cell —
if you just run that cell cold, it will look frozen forever. Avoid that
by running the same install command once, by hand, in a **plain terminal**
first (this is the one time you'll be asked to type your Ubuntu account
password — it won't show characters as you type, that's normal, just
type it and press Enter):

```bash
sudo apt-get update
sudo apt-get install -y build-essential automake autoconf libtool subversion git zlib1g-dev gfortran sox perl cmake libboost-all-dev libeigen3-dev unzip
```

Do this *before* running Section 3's cell in the notebook. Once it's done
here, the notebook's own copy of this step will find everything already
installed and finish in a couple of seconds.

If Section 3's cell fails with something like `returned non-zero exit
status 1` and no clearer message, it's almost always the password issue
above, not a broken package list — this notebook's own package list has
already been checked against a fresh Ubuntu install. (One thing it
deliberately does *not* `apt`-install: a math library like
`libatlas-base-dev` — some Ubuntu releases dropped that package entirely.
Section 4 builds OpenBLAS from source instead; see "Environment" above.)

### 10. Let it run

Once you're past Section 5 (Kaldi finishes building), the rest of the
notebook can mostly be run straight through. It's safe to leave your
computer and come back later — nothing needs interaction beyond clicking
Shift+Enter on each cell.

### 11. If something goes wrong partway through

Don't panic and don't start over from scratch. Just re-run the notebook
from the top (**Run → Run All Cells**, or Shift+Enter through it again).
Every stage checks whether it already finished before doing any work, so
anything already completed will just print `[skip]` and move on
instantly — you only redo whatever failed or didn't finish.

If a specific cell shows a red error box, read the last few lines of the
printed output — Kaldi and this notebook's own checks are written to
explain what's missing (e.g. a specific package, or a broken path) rather
than fail silently.

### 12. When it's done

- Your trained model, decode graph, and Word Error Rate results are in
  the `output/tri3/` folder next to `wsl_train.ipynb` (plain Windows
  files — open that folder normally in File Explorer).
- The WER number printed at the end of Section 14 is your headline
  result — compare it against `conclusion.md`.

### 13. Coming back another day

Every time you want to work on this again:

```bash
wsl
source ~/asr-venv/bin/activate
cd "/mnt/c/Users/YourName/Documents/Sugbodoc/speech model"
jupyter lab wsl_train.ipynb
```

(steps 1, 3's `source` line, 4, and 5 — you do **not** need to repeat the
`pip install` from step 3 or the Kaldi build; both persist on disk.) When
you're done, close the browser tab and press **Ctrl+C** twice in the
terminal to stop Jupyter, or just close the terminal window.
