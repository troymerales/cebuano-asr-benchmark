# Bisaya ASR Benchmark: Kaldi HMM-GMM vs. ElevenLabs Scribe

A benchmark comparing a Kaldi HMM-GMM model trained from scratch against
ElevenLabs Scribe (a commercial ASR API) on the same Bisaya (Cebuano)
speech corpus.

## Background

The Kaldi model reproduces the best-performing Bisaya configuration from
Ing (2023) — a 2-gram, 3-state, speaker-adaptive-trained (SAT) HMM-GMM
model using the PS27 27-phoneme set. Every neural (DNN/TDNN) variant that
this work tested for Bisaya scored equal to or worse than this HMM-GMM
configuration, which is why there's no TDNN/DNN stage here. See
[Citation](#citation) below.

## Dataset

Bisaya (Cebuano) speech, stored as Parquet shards under
`data/bisaya_audio/` — one row per utterance, with audio bytes, a
transcript, and speaker/demographic metadata (gender, age band, dialect,
device, etc.). Not pre-split into train/test; the split happens at
training time (below).

## Systems evaluated

| | Kaldi HMM-GMM | ElevenLabs Scribe |
|---|---|---|
| Type | Trained from scratch on this corpus | Pretrained commercial API, evaluated zero-shot |
| Data seen | 80% of speakers (training split) | None of this corpus (never trained on it) |
| Evaluated on | Held-out 20% of speakers | Full corpus |

Because the two systems were exposed to the data differently, `compare.ipynb`
restricts the head-to-head comparison to the utterances **Kaldi never
trained on** — ElevenLabs' full-corpus result is also reported separately,
clearly labeled as outside that paired comparison.

## Repository structure

```
train_kaldi.ipynb          # train the Kaldi model (WSL2/Ubuntu)
evaluate_elevenlabs.ipynb  # call ElevenLabs, score its output
evaluate_kaldi.ipynb       # score the trained Kaldi model's output (Windows)
compare.ipynb              # normalize + compare both systems' results

data/bisaya_audio/         # corpus (Parquet shards, gitignored)
output/                    # generated results (gitignored)
  tri3/                    # full Kaldi model + decode output
  kaldi/results.csv        # Kaldi's raw per-utterance results
  elevenlabs/results.csv   # ElevenLabs' raw per-utterance results
models/tri3/                # curated, decode-ready Kaldi model (gitignored)
references/                 # local copy of source material, gitignored -- not redistributed (see Citation)
deploy/                     # interactive demo apps, not part of the benchmark -- see below
CLAUDE.md                   # detailed technical/environment notes
```

## Interactive demo (`deploy/`)

Separate from the notebooks above -- two Gradio apps for trying the
systems interactively rather than computing WER/CER, split by audience
and environment (see `deploy/README.md` for full setup):

| | `deploy/local/local_app.py` | `deploy/prod/prod_app.py` |
|---|---|---|
| Systems | Kaldi + ElevenLabs + Whisper (checklist, any combination) | Whisper only |
| Environment | **WSL2/Ubuntu**, built Kaldi checkout, `models/tri3/`, `ELEVENLABS_API_KEY` | Any lightweight cloud container (Hugging Face Spaces, Streamlit Community Cloud) or plain Python |
| Audience | Advanced users with the full local setup | Public-facing showcase |

`prod_app.py` drops Kaldi entirely -- it needs a compiled Kaldi checkout
under WSL/C++, which standard cloud containers can't build -- and is
self-contained so `deploy/prod/` can be pushed as its own deployment
unit with no dependency on the rest of this repo.

## Workflow

Run in this order:

1. **`train_kaldi.ipynb`** — trains the Kaldi model end-to-end (data prep,
   lexicon, language model, GMM training, decode) and exports the trained
   model to `output/tri3/` and `models/tri3/`.
2. **`evaluate_elevenlabs.ipynb`** — transcribes the full corpus via the
   ElevenLabs API and computes raw WER/CER. Independent of step 1.
3. **`evaluate_kaldi.ipynb`** — scores the Kaldi model's decode output
   from step 1 and computes raw WER/CER. Depends on step 1.
4. **`compare.ipynb`** — loads both raw results, applies text
   normalization, and produces the final comparison: headline WER/CER
   (raw and normalized), a raw-vs-normalized error breakdown, word/
   character confusion tables, and side-by-side charts. Depends on steps
   2 and 3.

Steps 2 and 3 can run in either order, or in parallel.

## Environment requirements

| Notebook | Environment | Why |
|---|---|---|
| `train_kaldi.ipynb` | **WSL2/Ubuntu** | Kaldi doesn't build on native Windows |
| `evaluate_elevenlabs.ipynb` | Plain Python (Windows or Linux) | No Kaldi dependency; just an HTTP API |
| `evaluate_kaldi.ipynb` | **Windows** (or any plain Python env) | Reads Kaldi's already-decoded text output — no Kaldi binaries needed |
| `compare.ipynb` | Plain Python (Windows or Linux) | Pure pandas/jiwer analysis |

Only `train_kaldi.ipynb` needs WSL and a Kaldi checkout. The other three
are plain Python notebooks (`pandas`, `pyarrow`, `jiwer`, `matplotlib`;
`evaluate_elevenlabs.ipynb` also needs `python-dotenv` and `elevenlabs`,
plus a git-ignored `.env` with `ELEVENLABS_API_KEY`).

## How the trained model gets from WSL to Windows

Kaldi only runs under WSL, but Windows can't dereference WSL-created
symlinks directly, and Kaldi's raw training output includes large,
training-only artifacts (per-job alignments, FSTs, logs) that evaluation
doesn't need. `train_kaldi.ipynb`'s last stage does both jobs from the
WSL side, before anything touches Windows:

1. Copies the full `exp/tri3` (model, decode graph, WER output) to
   `output/tri3/` on the Windows filesystem.
2. Curates a smaller `models/tri3/` — just the files needed to decode new
   audio (`final.mdl`, `final.alimdl`, `tree`, feature-transform configs,
   the decode graph), with symlinks dereferenced into real files.

`evaluate_kaldi.ipynb` then reads `output/tri3/decode_test/` from plain
Windows Python — no Kaldi installation needed there, since decoding
(inference) already happened in WSL.

## How metrics are calculated

- **WER** (Word Error Rate) and **CER** (Character Error Rate), both
  computed as `(substitutions + deletions + insertions) / (hits +
  substitutions + deletions)`, via [`jiwer`](https://github.com/jitsi/jiwer).
- `evaluate_elevenlabs.ipynb` and `evaluate_kaldi.ipynb` each compute and
  export **raw** metrics only (no text normalization).
- `compare.ipynb` is the single place normalization happens
  (`normalize_bisaya()`: lowercase, strip punctuation/hyphens, fold u/o
  together — a common Bisaya spelling variation) and where normalized
  WER/CER are computed, from each row's saved raw reference/prediction
  text. This keeps one canonical definition of "normalized" instead of
  duplicating it across notebooks.
- Both systems' `results.csv` share a `corpus_index` column (each row's
  position in a consistently-ordered load of the Parquet corpus) — the
  join key `compare.ipynb` uses to match the same utterances across both
  systems.

## Limitations and caveats

- **Small held-out test set.** The speaker-independent 80/20 split can
  leave as few as 3 speakers / ~19 utterances in the Kaldi test set —
  treat `compare.ipynb`'s output as a qualitative read, not a
  statistically powered comparison.
- **Rule-based lexicon.** The PS27 grapheme-to-phoneme mapping used for
  Kaldi's lexicon is a hand-written approximation, not a
  transcriber-produced dictionary.
- **Not a fully matched comparison.** ElevenLabs is a zero-shot
  pretrained model; Kaldi is trained specifically on this corpus. The
  paired comparison in `compare.ipynb` controls for *which* utterances
  are compared, not for this fundamental difference in how each system
  was built.
- Expect a WER gap against Ing (2023)'s own reported 5.41% figure for
  this configuration — this corpus is smaller and structured differently.

See `CLAUDE.md` for detailed environment/build notes (Kaldi-on-WSL
gotchas, exact stage-by-stage pipeline architecture).

## Citation

The Kaldi model configuration and PS27 phoneme set reproduced here are
from:

> Ing, J. A. (2023). *Filipino and Bisaya Speech Corpus and Baseline
> Acoustic Models for Healthcare Chatbot ASR*.
> https://www.researchgate.net/publication/374139254_Filipino_and_Bisaya_Speech_Corpus_and_Baseline_Acoustic_Models_for_Healthcare_Chatbot_ASR

The source text is not redistributed in this repository — `references/`
is a local, git-ignored copy for personal use only.
