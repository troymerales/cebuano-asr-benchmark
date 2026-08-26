# Bisaya ASR Benchmark: Kaldi HMM-GMM vs. ElevenLabs Scribe vs. Whisper

A benchmark comparing three Bisaya (Cebuano) ASR systems on the same
speech corpus: a Kaldi HMM-GMM model trained from scratch, ElevenLabs
Scribe (a commercial ASR API, evaluated zero-shot), and a Whisper small
model fine-tuned on this corpus (on Kaggle). The five notebooks under
`notebooks/` don't run from one shared environment or in a single "run
all" pass -- see "Running the pipeline" below for what to run where.

**[Live demo →](https://cebuano-asr-benchmark-u4pxbbe9xhuq3gdhnup2tj.streamlit.app/)**
-- a minimal Streamlit app serving just the fine-tuned Whisper checkpoint,
deployed to Streamlit Community Cloud (see `deploy/README.md`). It's a
quick way to try a recording, not the benchmark itself -- the actual
training, evaluation, and three-way comparison live in `notebooks/`.

## Repository structure

```
README.md             # this file
CLAUDE.md             # deep technical/environment reference (build gotchas, exact architecture)

notebooks/             # the benchmark itself -- train, evaluate, compare
  train_kaldi.ipynb      # train the Kaldi model from scratch (WSL2/Ubuntu)
  evaluate_kaldi.ipynb    # score Kaldi's decode output (plain Python)
  evaluate_elevenlabs.ipynb  # call the ElevenLabs API, score it (plain Python)
  finetune_whisper.ipynb  # fine-tune + evaluate Whisper (runs on Kaggle, GPU)
  compare.ipynb           # normalize + compare all three systems' results

deploy/                # NOT part of the benchmark -- interactive demo apps
  local/                  # all three engines, for advanced users with the full local setup
  prod/                   # Whisper only, self-contained, for cloud hosting
  README.md               # full setup/deploy instructions

data/bisaya_audio/     # corpus (Parquet shards) -- gitignored, not in this repo
output/                # generated results -- gitignored, reproduced by notebooks/
  tri3/                   # train_kaldi.ipynb's full Kaldi model + decode output
  kaldi/results.csv       # evaluate_kaldi.ipynb's raw per-utterance results
  elevenlabs/results.csv  # evaluate_elevenlabs.ipynb's raw per-utterance results
  whisper/results.csv     # finetune_whisper.ipynb's raw per-utterance results (downloaded from Kaggle)
models/tri3/           # curated, decode-ready Kaldi model -- gitignored, used by deploy/local/
references/            # local copy of source material -- gitignored, not redistributed (see Citation)
```

The split between `notebooks/` and `deploy/` is the main thing to
understand: **`notebooks/` is the benchmark** -- training and evaluating
each system, then comparing their WER/CER. **`deploy/` is a separate,
standalone pair of apps** for trying the systems interactively (upload
audio, get a transcript) -- it doesn't compute WER/CER and isn't read by
anything under `notebooks/`. See `deploy/README.md` for that side of the
repo.

`data/`, `output/`, and `models/` are all gitignored -- they're either
the corpus itself (not redistributed) or build artifacts the notebooks
regenerate, not something checked into version control.

## Running the pipeline

The five notebooks under `notebooks/` don't share one environment, so
there's no single "run all" entry point -- each is run on its own, in
this order:

| Notebook | Environment | Depends on |
|---|---|---|
| `train_kaldi.ipynb` | WSL2/Ubuntu (Kaldi doesn't build on native Windows) | corpus only |
| `evaluate_kaldi.ipynb` | Plain Python | `train_kaldi.ipynb`'s decode output |
| `evaluate_elevenlabs.ipynb` | Plain Python + `ELEVENLABS_API_KEY` | corpus only (real API cost) |
| `finetune_whisper.ipynb` | Kaggle (GPU) | corpus only, runs remotely |
| `compare.ipynb` | Plain Python | all three `results.csv` exports above |

Each notebook's own top cells explain its setup and exact run
instructions in more detail; `CLAUDE.md` has the deeper technical
reference (exact stage-by-stage architecture, environment gotchas).

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
comparison. Whisper's own full-corpus number is never reported at all --
unlike ElevenLabs, it was fine-tuned on 80% of this corpus, so a
full-corpus figure would mix train and test data. See "Limitations and
caveats" below for a further nuance on how blind Whisper's held-out set
actually is.

The Kaldi model reproduces the best-performing Bisaya configuration from
Ing (2023) -- a 2-gram, 3-state, speaker-adaptive-trained (SAT) HMM-GMM
model using the PS27 27-phoneme set. Every neural (DNN/TDNN) variant that
thesis tested for Bisaya scored equal to or worse than this HMM-GMM
configuration, which is why there's no neural stage in `train_kaldi.ipynb`.
See [Citation](#citation) below.

## Metrics, briefly

WER and CER are both `(substitutions + deletions + insertions) / (hits +
substitutions + deletions)`, via [`jiwer`](https://github.com/jitsi/jiwer).
Every eval notebook exports **raw** (non-normalized) metrics only;
`compare.ipynb` is the single place text normalization happens
(`normalize_bisaya()`: lowercase, strip punctuation/hyphens, fold u/o
together) and where normalized WER/CER get computed. All three systems'
`results.csv` share a `corpus_index` join key -- see `CLAUDE.md` for how
that's derived and why it has to be. Full detail on all of this is in
`CLAUDE.md` and each notebook's own cells, not repeated here.

## Limitations and caveats

- **Small held-out test set.** The speaker-independent 80/20 split can
  leave as few as 3 speakers / ~19 utterances in the Kaldi test set --
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
  on that same held-out set -- a milder, indirect form of exposure beyond
  simple train/test separation.
- Expect a WER gap against Ing (2023)'s own reported 5.41% figure for
  this configuration -- this corpus is smaller and structured differently.

See `CLAUDE.md` for detailed environment/build notes (Kaldi-on-WSL and
Kaggle gotchas, exact stage-by-stage pipeline architecture).

## Citation

The Kaldi model configuration and PS27 phoneme set reproduced here are
from:

> Ing, J. A. (2023). *Filipino and Bisaya Speech Corpus and Baseline
> Acoustic Models for Healthcare Chatbot ASR*.
> https://www.researchgate.net/publication/374139254_Filipino_and_Bisaya_Speech_Corpus_and_Baseline_Acoustic_Models_for_Healthcare_Chatbot_ASR

The source text is not redistributed in this repository -- `references/`
is a local, git-ignored copy for personal use only.
