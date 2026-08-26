# Bisaya ASR Benchmark: Kaldi HMM-GMM vs. ElevenLabs Scribe vs. Whisper

A benchmark comparing three Bisaya (Cebuano) ASR systems on the same
speech corpus: a Kaldi HMM-GMM model trained from scratch, ElevenLabs
Scribe (a commercial ASR API), and a Whisper small model fine-tuned on
this corpus.

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

| | Kaldi HMM-GMM | ElevenLabs Scribe | Whisper (fine-tuned) |
|---|---|---|---|
| Type | Trained from scratch on this corpus | Pretrained commercial API, evaluated zero-shot | `openai/whisper-small` fine-tuned on this corpus |
| Data seen | 80% of speakers (training split) | None of this corpus (never trained on it) | 80% of speakers (same split as Kaldi, seed 42) |
| Evaluated on | Held-out 20% of speakers | Full corpus | Held-out 20% of speakers |

Because the three systems were exposed to the data differently,
`compare.ipynb` restricts the head-to-head comparison to the utterances
**Kaldi (and Whisper) never trained on**. ElevenLabs' full-corpus result
is also reported separately, clearly labeled as outside that paired
comparison. Whisper's own full-corpus number is never reported at all —
unlike ElevenLabs, it was fine-tuned on 80% of this corpus, so a
full-corpus figure would mix train and test data rather than give a
comparable zero-shot reference point. Whisper's checkpoint selection
(which epoch's weights got kept) was also chosen based on its performance
on this held-out set during training, so it isn't a fully blind test set
the way ElevenLabs' full corpus is — see "Limitations and caveats" below.

## Repository structure

```
train_kaldi.ipynb          # train the Kaldi model (WSL2/Ubuntu)
evaluate_elevenlabs.ipynb  # call ElevenLabs, score its output
evaluate_kaldi.ipynb       # score the trained Kaldi model's output (Windows)
finetune_whisper.ipynb     # fine-tune Whisper + score it, on Kaggle (GPU) -- see below
compare.ipynb              # normalize + compare all three systems' results

data/bisaya_audio/         # corpus (Parquet shards, gitignored)
output/                    # generated results (gitignored)
  tri3/                    # full Kaldi model + decode output
  kaldi/results.csv        # Kaldi's raw per-utterance results
  elevenlabs/results.csv   # ElevenLabs' raw per-utterance results
  whisper/results.csv      # Whisper's raw per-utterance results (downloaded from Kaggle)
models/tri3/                # curated, decode-ready Kaldi model (gitignored)
references/                 # local copy of source material, gitignored -- not redistributed (see Citation)
deploy/                     # interactive demo apps, not part of the benchmark -- see below
CLAUDE.md                   # detailed technical/environment notes
```

`finetune_whisper.ipynb` runs on Kaggle (GPU), not locally -- it both
fine-tunes `openai/whisper-small` on this corpus's training split and, in
a section at the bottom, evaluates the fine-tuned checkpoint on the same
held-out test set Kaldi uses, exporting a `results.csv` you download from
Kaggle's Output tab and drop into `output/whisper/results.csv` locally.
`compare.ipynb` reads it from there like the other two systems' results.

## Interactive demo (`deploy/`)

Separate from the notebooks above -- two Streamlit apps for trying the
systems interactively rather than computing WER/CER, split by audience
and environment (see `deploy/README.md` for full setup). Built with
Streamlit rather than Gradio since Hugging Face Spaces now requires a
PRO account for Gradio Spaces -- Streamlit Community Cloud is still free.

| | `deploy/local/local_app.py` | `deploy/prod/prod_app.py` |
|---|---|---|
| Systems | Kaldi + ElevenLabs + Whisper (checklist, any combination) | Whisper only |
| Environment | **WSL2/Ubuntu**, built Kaldi checkout, `models/tri3/`, `ELEVENLABS_API_KEY` | Any lightweight cloud container (Streamlit Community Cloud) or plain Python |
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
4. **`finetune_whisper.ipynb`** (on Kaggle) — fine-tunes Whisper on the
   same speaker-independent split Kaldi uses, then evaluates it on the
   held-out test set and exports `results.csv`. Download that file from
   Kaggle's Output tab into `output/whisper/results.csv`. Independent of
   steps 1-3.
5. **`compare.ipynb`** — loads all three raw results, applies text
   normalization, and produces the final comparison: headline WER/CER
   (raw and normalized), a raw-vs-normalized error breakdown, word/
   character confusion tables, and side-by-side charts. Depends on steps
   2, 3, and 4.

Steps 2, 3, and 4 can run in any order, or in parallel.

## Environment requirements

| Notebook | Environment | Why |
|---|---|---|
| `train_kaldi.ipynb` | **WSL2/Ubuntu** | Kaldi doesn't build on native Windows |
| `evaluate_elevenlabs.ipynb` | Plain Python (Windows or Linux) | No Kaldi dependency; just an HTTP API |
| `evaluate_kaldi.ipynb` | **Windows** (or any plain Python env) | Reads Kaldi's already-decoded text output — no Kaldi binaries needed |
| `finetune_whisper.ipynb` | **Kaggle** (GPU) | Fine-tuning needs a GPU; not run locally |
| `compare.ipynb` | Plain Python (Windows or Linux) | Pure pandas/jiwer analysis |

Only `train_kaldi.ipynb` needs WSL and a Kaldi checkout, and
`finetune_whisper.ipynb` only runs on Kaggle. The two `evaluate_*.ipynb`
notebooks and `compare.ipynb` are plain Python (`pandas`, `pyarrow`,
`jiwer`, `matplotlib`; `evaluate_elevenlabs.ipynb` also needs
`python-dotenv` and `elevenlabs`, plus a git-ignored `.env` with
`ELEVENLABS_API_KEY`).

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
- `evaluate_elevenlabs.ipynb`, `evaluate_kaldi.ipynb`, and
  `finetune_whisper.ipynb`'s eval section each compute and export **raw**
  metrics only (no text normalization).
- `compare.ipynb` is the single place normalization happens
  (`normalize_bisaya()`: lowercase, strip punctuation/hyphens, fold u/o
  together — a common Bisaya spelling variation) and where normalized
  WER/CER are computed, from each row's saved raw reference/prediction
  text. This keeps one canonical definition of "normalized" instead of
  duplicating it across notebooks.
- All three systems' `results.csv` share a `corpus_index` column (each
  row's position in a consistently-ordered load of the Parquet corpus) —
  the join key `compare.ipynb` uses to match the same utterances across
  all three systems.

## Limitations and caveats

- **Small held-out test set.** The speaker-independent 80/20 split can
  leave as few as 3 speakers / ~19 utterances in the Kaldi test set —
  treat `compare.ipynb`'s output as a qualitative read, not a
  statistically powered comparison.
- **Rule-based lexicon.** The PS27 grapheme-to-phoneme mapping used for
  Kaldi's lexicon is a hand-written approximation, not a
  transcriber-produced dictionary.
- **Not a fully matched comparison.** ElevenLabs is a zero-shot
  pretrained model; Kaldi and Whisper are each trained specifically on
  this corpus. The paired comparison in `compare.ipynb` controls for
  *which* utterances are compared, not for this fundamental difference in
  how each system was built.
- **Whisper's held-out set isn't fully blind.** It wasn't trained on
  those utterances directly, but during fine-tuning the best checkpoint
  was selected (and training was stopped early) based on its performance
  on that same held-out set — a milder, indirect form of exposure beyond
  simple train/test separation.
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
