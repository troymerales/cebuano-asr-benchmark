# Reproduction Guide: Filipino and Bisaya ASR System using TDNN-HMM (Ing, 2023)

**Purpose of this document:** This is an implementation blueprint, not a summary of the thesis. It is written so that, given a *different* Bisaya or Filipino speech dataset, you can recreate the paper's ASR pipeline (HMM-GMM baseline → TDNN-HMM hybrid) on that new data. Background/theory is included only where it explains an implementation decision. The paper's reported results are included only as a reference point for judging a reproduction, not as a target that a different dataset should be expected to hit.

Source: Ing, J. A. (2023). *Filipino and Bisaya ASR System using TDNN-HMM towards application in a healthcare chatbot* (Master's thesis, De La Salle University).

Throughout this document: `Not specified in the paper` marks any parameter the thesis does not report. Do not substitute an assumed value for these without documenting that you made a choice.

---

## 1. Implementation Overview

Pipeline used in the paper:

`Raw Audio (WAV recordings)` → `Audio Preparation (noise screening + speed perturbation)` → `Transcript Preparation (word-level + phoneme-level transcription)` → `Dataset Splitting (speaker-independent 80/20)` → `Model Input (MFCC + CMVN [+ iVectors + volume perturbation for NN models])` → `Model (HMM-GMM monophone→triphone→enhancement, then TDNN-HMM/DNN-HMM)` → `Training/Fine-tuning (Kaldi GMM training recipe; Kaldi nnet3 TDNN recipe, 5 epochs)` → `Inference (Kaldi Viterbi/lattice decoding with n-gram LM)` → `Evaluation (WER; PER and confusion-matrix analysis)`

| Stage | Input | Processing | Output | Key parameters | Dependencies |
|---|---|---|---|---|---|
| Audio Preparation | Raw WAV recordings, per-response segments | Screen for unrecoverable noise (discard); light noise reduction on keepable files; speed perturbation | Cleaned WAV set + perturbed copies | Speed factor 1.1–1.25 (random per file); 16 kHz WAV | Recording pipeline / custom web recorder |
| Transcript Preparation | Raw spoken response | Word-level transcription (lowercase alphanumeric); phoneme-level transcription (PS27 or PS35) | Word transcript + phoneme transcript per utterance | Phoneme set choice (PS27/PS35); code-switch and affix rules | Human transcribers, phoneme set definition |
| Dataset Splitting | Full transcribed corpus | Speaker-independent 80/20 split; test speakers chosen once at random and held fixed across all model variants | Train set / Test set (no validation set reported) | ~80/20 ratio; FSC excluded from Filipino test set | Speaker metadata |
| Model Input | Train/test WAV + transcripts | MFCC extraction + CMVN; (NN models add iVectors + volume perturbation) | Per-frame feature vectors | 25 ms window, 10 ms frameshift, 13 cepstral coeffs (+Δ+ΔΔ = 39 dims) | Kaldi feature pipeline |
| Model | Feature vectors, phoneme transcripts | HMM-GMM (mono→tri→LDA+MLLT/VTLN/SAT); TDNN-HMM/DNN-HMM (GMM replaced by NN) | Trained acoustic model | HMM states (3/4/5); TDNN topology (symmetric/asymmetric/subsampled) | Kaldi `nnet3` recipe |
| Training/Fine-tuning | Acoustic model + features + LM | GMM re-estimation (Baum-Welch); NN trained via Kaldi nnet3 | Final acoustic model checkpoint | NN: 5 epochs, LR 0.01→0.001 | Kaldi, SRILM |
| Inference | Test audio + trained AM + LM | Feature extraction → decoding (Viterbi/lattice) with n-gram LM at tuned weight | Hypothesis transcript | LM weight (best found in 15–25% range) | Kaldi decoder |
| Evaluation | Hypothesis vs. reference transcripts | WER computation; word/phoneme confusion analysis; PER for children's speech | WER / PER, confusion tables | WER = (I+D+S)/N | Kaldi scoring scripts |

---

## 2. Dataset Specification

| Property | Value | Status |
|---|---|---|
| Primary source | DLSU healthcare chatbot project corpus (Luci-Atienza, 2021) | Used by paper |
| Supplementary sources | Filipino Speech Corpus (FSC, Guevara et al., 2002) subset — isolated words, adult female, 10 speakers; additional data collected by the author | Used by paper |
| Bisaya supplementary source | Section 1.5.1 states a subset of the "Cebuano Speech Corpus from the ISIP Project 6" (Ang et al., 2014) was also used to supplement the data, but Chapter 4/5 only report the 7-speaker/8.97-hour DLSU Bisaya corpus with no separate Cebuano-corpus statistics | Mentioned inconsistently — treat as `Not specified in the paper` how much (if any) of this corpus is in the final 8.97-hour Bisaya figure |
| Filipino speakers | 9 (DLSU corpus) + 10 (FSC) + 4 (collected) = 23 | Used by paper |
| Bisaya speakers | 7 | Used by paper |
| Filipino duration | 9.03 h (DLSU) + 2.78 h (FSC) + 4.49 h (collected) = 16.3 h | Used by paper |
| Bisaya duration | 8.97 h | Used by paper |
| Audio format | WAV | Used by paper — **not stated as a strict methodological requirement**, but Kaldi's standard recipes assume WAV/uncompressed PCM |
| Sampling rate | 16 kHz | Used by paper. **Reproduction:** if the new dataset differs, resample to 16 kHz (or pick one consistent rate and adjust the MFCC config's Nyquist-dependent parameters) |
| Channels | Not specified in the paper | — |
| Bit depth | Not specified in the paper | — |
| Transcript format | Plain text, two parallel transcriptions per utterance: word-level and phoneme-level | Used by paper — **required by methodology** since the phoneme-level transcript drives lexicon/pronunciation-dictionary construction in Kaldi |
| Language/dialect | Filipino (Tagalog-based) and Bisaya (Cebuano) | Dataset-specific — the paper's phoneme sets were designed for Filipino and only evaluated post hoc for Bisaya suitability |
| Speaker metadata | Speaker ID recorded (used for the speaker-independent split); gender is adult female for essentially all speakers (children's speech was inaccessible for most of the study; adult female voices ~200 Hz were used as a proxy for children's ~250–400 Hz voices) | Used by paper — speaker independence is required by the methodology; the adult-female-as-children-proxy choice is dataset-specific and not required for reproduction on a general dataset |
| Recording conditions | Custom recording website; consent form; scripted prompts (Table 4.1 wellness-assessment categories); instructions to record in a quiet environment | Used by paper |
| Domain / content | Healthcare chatbot: responses only (not full conversations) to a fixed conversational flow: general appearance, allergies, cough, fever, family history, vaccination, review of systems, daily activities, hygiene, play, sleep | Dataset-specific |
| Annotation format | Word-level: lowercase alphanumeric, no punctuation. Phoneme-level: PS27 (27 monophones) or PS35 (26 monophones + 9 diphones) | Required by methodology if reproducing the same phoneme-based lexicon approach |
| Filtering criteria | Audio discarded if it contains loud/unremovable noise (e.g., dog barks, passing cars); kept if noise is light and reducible | Used by paper |
| Code-switching | English words present; English speech itself was **not** used or collected. Only Filipino/Bisaya utterances (which may contain English loanwords) were used | Used by paper |
| Segmentation | Corpus already delivered pre-segmented into single spoken responses | Dataset-specific — a new raw dataset that is *not* pre-segmented will need a segmentation step not described in the paper (see Section 14) |

**Word/audio-file counts reported (Table 5.2, cross-checked against body text — the two do not fully agree, both reproduced here for transparency):**

| Corpus | Unique words | Total words | Audio files (Table 5.2) | Audio files (body text) |
|---|---:|---:|---:|---:|
| Bisaya | 888 | 48,816 | 21,548 | 21,458 |
| Filipino + Additional Data | 966 | 72,300 | 32,073 | 21,548 |
| FSC (Filipino) | 741 | 7,991 | 7,908 | 7,908 |

This is a known internal inconsistency in the source document — do not treat either column as more authoritative than the other; if you need exact file counts for your own dataset you will compute them directly rather than relying on this table.

---

## 3. Data Preparation

### Audio

| Operation | Input → Transformation → Output | Parameters |
|---|---|---|
| Format/rate | Raw recording → recorded directly as WAV at target rate → WAV, 16 kHz | Automatic at recording time via the custom recorder; for external audio, resample to 16 kHz |
| Noise screening | Raw segment → inspect for noise severity → keep (proceed to light noise reduction) or discard | Discard threshold: unrecoverable noise types are dog barks, passing cars (examples given, not an exhaustive rule). Reduction method/tool: `Not specified in the paper` |
| Mono/stereo | `Not specified in the paper` | — |
| Normalization (loudness) | `Not specified in the paper` | — |
| Silence trimming | `Not specified in the paper` (corpus arrives "already segmented into single responses"; no explicit VAD/trimming step described) | — |
| Segmentation | Already done upstream for the source corpora | Not itself part of this paper's pipeline for the primary corpora |
| Duration filtering | `Not specified in the paper` | — |
| Data augmentation (speed perturbation) | Clean WAV → apply a randomly chosen speed factor → additional perturbed WAV, used as extra training data | Speed factor randomly in **1.1–1.25**, applied per audio file; perturbed copy added to training data only (for both Filipino and Bisaya) |
| Data augmentation (volume perturbation) | Used only as an additional input to the TDNN models, not described as a general audio-prep step | `Not specified in the paper` how the volume perturbation was parameterized (this is standard in Kaldi's nnet3 recipe as a fixed random gain range, but the paper does not give the value used) |

### Transcripts

| Operation | Input → Transformation → Output | Parameters |
|---|---|---|
| Case | Raw transcript → lowercase | All alphanumeric characters lowercase |
| Punctuation | Raw transcript → strip all punctuation → punctuation-free text | No punctuation marks retained |
| Numbers | Spoken number → spelled out in words, **except** medical terms (e.g., "covid 19") which keep numeral form | Rule is domain-specific (healthcare terms) |
| Acronyms | Medical acronym (e.g., UTI) → transcribed as a single fused word | e.g., "uti" (one token), not "u t i" |
| Code-switching (dictionary words) | English word used mid-sentence that exists in a formal English or Filipino dictionary → transcribed as-is | No special marking |
| Code-switching (affixed English root) | Filipino/Bisaya affix + English root (e.g., "nagtotoothbrush") → split into two tokens when the affix is observed recurring in the corpus | The paper gives two different renderings of this same example in different chapters ("nagto" + "toothbrush" in Ch.1 vs. "nagto" + "nagtotoothbrush" in Ch.4) — this is an internal inconsistency; the intended rule is almost certainly *root word split from affix*, i.e. **prefix token + bare English root token** |
| Special characters/Unicode | `Not specified in the paper` | — |
| Tokenization | Whitespace-delimited words, each becoming a lexicon entry | — |
| Vocabulary construction | Vocabulary = set of unique word tokens across the transcripts (used to build the Kaldi lexicon) | Unique word counts given per corpus in Section 2 |
| Unknown words/tokens | Standard Kaldi `<UNK>` handling is implied by n-gram LM smoothing discussion in Ch.3, but no explicit OOV policy is stated for this study's data | `Not specified in the paper` |
| Phoneme-level transcription (PS27) | Word → sequence of 27 monophones | Phoneme inventory in Table 4.2 |
| Phoneme-level transcription (PS35) | Word → sequence of 26 monophones + 9 diphones, where diphones **supersede** the equivalent monophone pair whenever applicable (to avoid redundant transcriptions) | Diphones: /ha/, /he/, /hi/, /ho/, /hu/, /at/, /aw/, /ay/, /oy/ |
| IPA mapping | PS27/PS35 symbol → IPA equivalent | /sh/→/ʃ/, /th/→/θ/, /j/→/dʒ/, /ch/→/tʃ/, /ng/→/ŋ/ (Table 3.3) |

---

## 4. Dataset Construction and Splitting

- **Train/test split ratio:** approximately 80/20.
- **Validation set:** not reported — the paper only describes a train/test split. `Not specified in the paper` whether any held-out validation subset was used during NN training (e.g., for early stopping); the fixed 5-epoch schedule (Section 7) suggests none was used for stopping decisions.
- **Split method:** speaker-independent. The split is performed **by speaker**, not by utterance, specifically so that models are evaluated on voices unseen during training.
- **Speaker selection for test set:** test speakers were chosen **once, randomly**, per language (Filipino and Bisaya each had their own randomly chosen test speaker set), and this same test split was then held fixed and reused across **all** model variants and experiments in the study.
- **Random seed:** `Not specified in the paper`. The split cannot be exactly reproduced without it — treat the specific speakers selected as unrecoverable, and instead replicate the *procedure* (random speaker holdout, fixed across all experiments) on your own data.
- **Filtering before split:** for Filipino, the FSC subset is explicitly **excluded from the test set** — it is training-only data because of its distinct (isolated-word) vocabulary.
- **Data leakage:** the paper's design actively avoids leakage by holding out speakers rather than utterances. When reproducing, verify that no speaker present in test also appears in train (including through any augmented/perturbed copies of their audio).

---

## 5. Model Input / Representation

**Feature type:** MFCC (Mel Frequency Cepstral Coefficients), computed via Kaldi.

| Parameter | Value | Notes |
|---|---|---|
| Window size | 25 ms | Kaldi default, explicitly confirmed used |
| Frameshift | 10 ms | Kaldi default, explicitly confirmed used |
| Number of cepstral coefficients | 13 static | Plus 13 delta + 13 delta-delta = 39-dimensional feature vector per frame |
| Pre-emphasis | Applied (standard MFCC step, described in Ch.3 theory) | Coefficient value: `Not specified in the paper` |
| Windowing function | Hamming/Hanning-type tapering described in theory (Ch.3) as the general MFCC approach | Exact function used in this study's Kaldi config: `Not specified in the paper` (Kaldi default is Povey window unless configured otherwise — the paper does not confirm which was used) |
| Mel filterbank / frequency range | `Not specified in the paper` (number of filters, min/max frequency) | — |
| Normalization | CMVN (Cepstral Mean and Variance Normalization) applied after MFCC extraction | Standard per-speaker or per-utterance CMVN in Kaldi; which scope was used is `Not specified in the paper` |
| Additional features (NN models only) | iVectors | Dimensionality: `Not specified in the paper` for this study specifically (related work cited elsewhere in the thesis uses 100-dim iVectors, but this is not confirmed as the value this study used) |
| Additional augmentation fed to NN models | Volume perturbation | Parameters: `Not specified in the paper` |
| Feature extractor / toolkit | Kaldi's standard MFCC + CMVN pipeline (`compute-mfcc-feats`, `compute-cmvn-stats` equivalents) | — |

No pretrained feature extractor or learned front-end (e.g., wav2vec-style) is used anywhere in this study — all features are classical DSP-based (MFCC/CMVN/iVector), consistent with the Kaldi GMM/TDNN-HMM approach.

---

## 6. ASR Model

### Pretrained Components

**None.** This study does not use any pretrained ASR model, pretrained acoustic model, or pretrained language model. Every acoustic model (HMM-GMM and TDNN-HMM/DNN-HMM) and every n-gram language model is trained from scratch on the study's own corpus. The only "reuse" in the study is the cross-language experiment (Section 4.4.6/5.4.3), where a Filipino-trained acoustic model is evaluated directly on Bisaya speech and vice versa — this is an evaluation-time experiment, not a pretraining/fine-tuning strategy.

### Paper-Specific Implementation

**Toolkit:** Kaldi ASR toolkit (Povey et al., 2011) for all acoustic and decoding pipelines; SRILM toolkit for n-gram language models.

**Acoustic model family 1 — HMM-GMM (baseline):**
- Trained in the standard Kaldi progression: monophone → triphone → (optionally) LDA+MLLT and/or VTLN and/or SAT.
- Enhancement combinations tested: `LDA+MLLT`, `SAT`, `VTLN`, `VTLN+LDA+MLLT`, `VTLN+SAT`.
- HMM topology: 3-state, 4-state, and 5-state HMMs each tested (i.e., number of emitting states per phone HMM).
- VTLN warping factor: 0.8–1.2 (standard range cited from Povey et al., 2011); whether linear or non-linear VTLN was used for the actual experiments is not explicitly confirmed — both forms are described theoretically.

**Acoustic model family 2 — Hybrid NN-HMM:** the GMM emission model is replaced with a neural network; the HMM structure (states, transitions) is retained. Implemented using Kaldi's premade `nnet3` recipe. Four network configurations were compared:

| Model | Layers × nodes | Activation | Time strides / network context | Approx. parameters |
|---|---|---|---|---:|
| DNN baseline | Table 4.3 states 3 layers × 512 nodes; body text (§4.4.4) states 4 hidden layers × 512 nodes — **internal inconsistency in the paper** | ReLU | [-7, 7] (fixed, non-TDNN) | ~3.1 million |
| TDNN symmetric | 6 layers × 512 nodes | ReLU | [-2,2], [-1,1], [-1,1], [-3,3], [-3,3], [-6,6] (context [-16,16]) | ~4.9 million (body text says "about 5 million") |
| TDNN asymmetric | 4 layers × 512 nodes | ReLU | [-2,2], [-1,2], [-3,3], [-7,2] (context [-13,9]) | ~4 million |
| TDNN subsampled | 4 layers × 512 nodes | ReLU | [-2,2], {-1,2}, {-3,3}, {-7,2} — curly braces denote sub-sampled (only select frames within the range used, not the full context) (context [-13,9]) | ~3.3 million |

- Asymmetric strides intentionally use a larger left context and smaller right context to reduce latency for online decoding.
- Subsampling further reduces latency, training time, and parameter count by using only select frames rather than the full context window in deeper layers.
- All TDNN models additionally take iVectors and volume-perturbed features as input (see Section 5).
- The specific symmetric TDNN topology mirrors a preliminary architecture from the author's own earlier work (Ing, Pascual, & Dimzon, 2022), which reported 0.97% WER on the (different, children's) FCSC dataset — a data point, not part of this study's own comparison table.

**Lexicon/pronunciation model:** phoneme sequences from Section 3/4 are used to build the Kaldi lexicon (pronunciation dictionary), which maps each word to its PS27 or PS35 phoneme sequence — this lexicon underlies both the HMM-GMM and TDNN-HMM acoustic models.

**Language model:** n-gram, trained on the transcriptions themselves (not a general-domain corpus, since the target domain — healthcare Q&A responses — is narrow). Built with SRILM. Orders tested: 2-gram and 3-gram (Ch.4/Ch.5 report only these two; Ch.1's overview additionally mentions 4-gram, which is not reflected anywhere in the Chapter 5 results tables — treat 4-gram as **not actually evaluated** in the reported results, despite being mentioned as an intended experiment).

**Loss function:** `Not specified in the paper` for the NN training (Kaldi nnet3's default cross-entropy / sequence-training objectives are standard, but the paper does not confirm which was used or whether any sequence-discriminative training stage — e.g., LF-MMI — was applied on top of cross-entropy).

**Modifications by the researchers:** the core novel experimentation is architectural (symmetric vs. asymmetric vs. subsampled time strides) and is original exploration built directly on Kaldi's standard `nnet3` TDNN recipe rather than a modification of a pretrained model.

---

## 7. Training Configuration

| Parameter | Paper Configuration | Reproduction Notes |
|---|---|---|
| Optimizer | Not specified in the paper (Kaldi nnet3 default is natural-gradient SGD, but not confirmed for this study) | Confirm/choose explicitly if reimplementing outside Kaldi's default recipe |
| Learning rate | Initial 0.01, final 0.001 (NN models only; presumably an exponential decay schedule across epochs, as is standard in Kaldi nnet3, but the schedule shape itself is not confirmed) | — |
| Batch size | Not specified in the paper | — |
| Epochs | 5 (all NN models) | — |
| Scheduler | Not specified in the paper beyond initial/final LR | — |
| Warmup | Not specified in the paper | — |
| Weight decay | Not specified in the paper | — |
| Gradient accumulation | Not specified in the paper | — |
| Early stopping | Not specified in the paper (fixed 5-epoch schedule suggests none used) | — |
| Precision | Not specified in the paper | — |
| Random seed | Not specified in the paper | — |
| HMM-GMM training iterations/steps | Not specified in the paper (standard Kaldi mono/tri recipe defaults implied but not confirmed) | — |

**Other reported training details:**

- **Hardware:** i5-12400 CPU + NVIDIA GTX 1050 Ti GPU (for NN model training).
- **Framework/toolkit:** Kaldi ASR toolkit (`nnet3` recipe for NN models); SRILM for language models. No version numbers given for either.
- **Training data volume per model:** Filipino NN models trained on ~12.5 hours; Bisaya NN models trained on ~7.2 hours (these reflect the actual train-split sizes after the 80/20 split, not the full corpus).
- **Training time (measured, Filipino):** DNN 98.5 min; TDNN symmetric 135.2 min; TDNN asymmetric 128.0 min; TDNN subsampled 88.8 min.
- **Training time (measured, Bisaya):** DNN 51.0 min; TDNN symmetric 103.2 min; TDNN asymmetric 92.5 min; TDNN subsampled 82.3 min.
- **Checkpointing:** Not specified in the paper.
- **Data augmentation used in training:** speed perturbation (1.1–1.25×, applied to raw audio pre-feature-extraction) and volume perturbation (fed specifically into the NN acoustic models). No noise augmentation, SpecAugment, or VTLP is used in this study (these are discussed in Ch.2 as related work, not as part of this study's own method).
- **Gradient clipping:** Not specified in the paper.

---

## 8. Inference

`Audio → MFCC+CMVN (+ iVectors for NN models) → Acoustic Model (HMM-GMM or TDNN-HMM) → Lattice generation with n-gram LM → Best-path decoding → Hypothesis transcript`

| Aspect | Value |
|---|---|
| Input format | Same MFCC(+CMVN, +iVector for NN) feature pipeline as training, applied to test audio |
| Decoding method | Kaldi's standard lattice-based decoding (implicitly Viterbi-derived best path search over the decoding graph); beam search parameters (beam width, lattice beam, max-active) are `Not specified in the paper` |
| Beam size | Not specified in the paper |
| Language model usage | n-gram LM (2-gram or 3-gram, depending on best result for that language) integrated at decode time with a tunable LM weight | 
| LM weight | Swept from 1% to 25%; best-performing weight for all models in the study falls between roughly 15% and 25% (WER plateaus in this range) |
| Post-processing | Not specified in the paper (no stated punctuation restoration, casing, or number-formatting step after decoding — consistent with the fully lowercase, spelled-out-number transcript convention used for scoring) |
| Text normalization before scoring | The hypothesis and reference are expected to already match the training transcript convention (lowercase alphanumeric, no punctuation) — no extra normalization step is described |
| Inference time (measured, Filipino, ~1.47s avg. response) | DNN 2.6s; TDNN symmetric 3.8s; TDNN asymmetric 3.0s; TDNN subsampled 2.9s |
| Inference time (measured, Bisaya, ~1.43s avg. response) | DNN 2.5s; TDNN symmetric 3.3s; TDNN asymmetric 2.7s; TDNN subsampled 2.8s |

Note: the paper states these inference times use Kaldi's stock decoding script and were not optimized for latency.

---

## 9. Evaluation

**Primary metric:** Word Error Rate (WER), computed as:

WER = (I + D + S) / N

where I = insertions, D = deletions, S = substitutions (relative to the reference word sequence), and N = total number of reference words.

**Secondary analyses:**
- **Word-level confusion analysis:** most frequent substitution/insertion/deletion pairs, computed per best model, to identify systematic error patterns (enclitic/particle word drops, substring confusions, homophones).
- **Phoneme-level confusion analysis:** simplified phoneme confusion matrices per phoneme set (PS27/PS35), used to identify which phonemes/phoneme classes are most often confused, and to compare PS27 vs. PS35 suitability for Bisaya.
- **Phoneme Error Rate (PER):** used specifically for the children's-speech evaluation, in place of WER, because the training vocabulary has little to no overlap with the children's conversational healthcare-interview vocabulary (WER would be dominated by out-of-vocabulary effects rather than acoustic-model quality).

**Evaluation procedure:**
1. Decode the held-out speaker-independent test set with each trained model at its best LM weight.
2. Compute WER against the word-level reference transcript.
3. For the top model(s) per phoneme set/language, additionally compute word- and phoneme-level confusion tables.
4. For the children's-speech experiment, decode actual child healthcare-interview recordings and score with PER against the phoneme-level reference instead of WER.

**Comparison/baseline models within the paper itself:** HMM-GMM (monophone/triphone/enhancement variants) serves as the internal baseline against which the TDNN-HMM/DNN-HMM hybrid models are compared, for each language.

No external open-source ASR baseline (e.g., a pretrained multilingual model) is used for comparison — all comparisons are internal, among the models trained in this study.

---

## 10. Paper Results as Baseline

| Configuration | Dataset | WER | Notes |
|---|---|---:|---|
| Filipino HMM-GMM SAT (3-gram, 3-state, PS27) | DLSU + FSC + collected Filipino corpus (16.3 h, 23 speakers) | 3.96% | Best HMM-GMM baseline for Filipino |
| Filipino TDNN-HMM asymmetric (3-gram, 5-state, PS27) | Same | **3.48%** | Best overall Filipino model in the study |
| Bisaya HMM-GMM SAT (2-gram, 3-state, PS27) | Bisaya corpus (8.97 h, 7 speakers) | **5.41%** | Best overall Bisaya model in the study |
| Bisaya DNN-HMM baseline (2-gram, 5-state, PS35) | Same | 5.50% | Best NN-based Bisaya model — notably, the plain DNN outperformed all TDNN variants for Bisaya, unlike for Filipino |
| Filipino TDNN models, no additional data (original corpus only) | DLSU Filipino corpus only (9.03 h) | ~12–14% (model-dependent) | Reference point showing the effect of the additional 7.27 h (FSC + collected) of data |
| Filipino/Bisaya best models on actual children's healthcare speech | Separate children's-speech test set | PER 50.90%/52.77% (Filipino), 30.92%/31.60% (Bisaya) | Not directly comparable to the WER figures above — different metric, different (harder, mismatched-vocabulary) test set |
| Cross-language acoustic models (Filipino AM → Bisaya speech, and vice versa) | Opposite-language test set | 9.05%–15.46% (model-dependent) | Degraded but usable performance; supports viability of cross-lingual acoustic model reuse for phonetically similar languages |

> These values serve as reference points for evaluating a reproduction of the methodology. They should not be expected to match exactly when using a different dataset. A different dataset will differ in vocabulary size, domain narrowness, recording quality, speaker count, and total duration — all of which strongly affect WER in this kind of small-vocabulary, domain-specific corpus (e.g., note how the ~7 h Bisaya corpus without extra data performs far worse than the ~16 h Filipino corpus with it; see Section 5.4.1 in the source thesis). If your new dataset is not a narrow-domain, small-vocabulary healthcare Q&A corpus, direct comparison to these numbers is not meaningful — they will most likely be optimistic relative to a more open-vocabulary or conversational task.

---

## 11. Reproduction Guide for a New Dataset

### Step 1 — Prepare the Dataset
Required inputs:
- Audio recordings (ideally already segmented into single utterances/responses; if not, you must add a segmentation step the paper does not describe).
- Word-level transcripts for every utterance.
- Speaker ID for every utterance (mandatory — the split depends on it).

Expected format: WAV audio (any consistent sampling rate — resample to a single fixed rate); plain-text transcript per utterance, associated with a speaker ID.

### Step 2 — Standardize Audio
Perform:
- Resample all audio to a single consistent sampling rate (paper used 16 kHz; if your source data is already at a fixed rate, that rate can be kept, but be consistent across all utterances and note that this is a deviation from the paper if you don't use 16 kHz).
- Screen out utterances with unrecoverable noise; apply light noise reduction to the rest (the paper does not name a specific reduction algorithm — you must select and document one).
- Optionally apply speed perturbation (paper: random factor 1.1–1.25 per file) to expand the training set.

Expected output: A clean, uniformly-formatted WAV corpus, at consistent sample rate/channel count, with an expanded (speed-perturbed) training pool if desired.

### Step 3 — Standardize Transcripts
Perform:
- Lowercase all text; remove punctuation.
- Decide and document your own convention for numerals (paper: spell out except domain-specific terms kept numeric) — this rule is domain-specific and must be re-derived for your domain, not copied blindly.
- Decide how to handle code-switched words and affixed loanwords, following the paper's general principle: recurring affix+loanword combinations are split into a native-affix token and a bare loanword token.
- If reproducing the phoneme-level modeling approach: build a phoneme transcription for each word, either using PS27, PS35, or a phoneme set appropriate to your target language (PS27/PS35 were designed for Filipino/Bisaya specifically and cannot be assumed to transfer to an unrelated language).
- Build the vocabulary/lexicon from the resulting word and phoneme transcripts.

Expected output: Cleaned word-level transcripts, phoneme-level transcripts, and a lexicon (word → phoneme sequence) usable by Kaldi.

### Step 4 — Create Train/Validation/Test Sets
Follow:
- Split by speaker, not by utterance, to keep the test set speaker-independent.
- Use roughly an 80/20 train/test ratio (paper does not describe a validation split — you may add one for your own model-selection needs, but note this is your own addition, not part of the original methodology).
- If any subset of your data has a very different vocabulary or register from the rest (as FSC did for Filipino), consider excluding it from the test set specifically, as the paper did, to avoid the test set being unrepresentative of the target domain.

Important considerations:
- Fix the random seed for your split and record it — the paper's own split is not reproducible because no seed was reported.
- Verify zero speaker overlap between train and test, including across any augmented (speed/volume-perturbed) copies.

### Step 5 — Prepare Model Input
Use:
- MFCC features: 25 ms window, 10 ms frameshift, 13 static coefficients + Δ + ΔΔ (39-dim total).
- CMVN normalization on top of MFCC.
- For NN (TDNN/DNN) models: add iVectors and volume-perturbed features as additional inputs (exact iVector dimensionality and volume-perturbation range are not specified in the paper — choose Kaldi's standard defaults and document the choice, e.g. 100-dim iVectors is a common Kaldi recipe default).

Configuration: Kaldi's standard `compute-mfcc-feats` / CMVN / iVector-extraction pipeline; no pretrained feature extractor is used.

### Step 6 — Configure the ASR Model
Use: Kaldi ASR toolkit throughout — HMM-GMM training recipe, then `nnet3` for the TDNN/DNN stage.

Pretrained components: none — every component is trained from scratch on your data.

Paper-specific configuration:
- HMM-GMM: train monophone → triphone → apply chosen enhancement combination(s) (LDA+MLLT, SAT, VTLN, VTLN+LDA+MLLT, VTLN+SAT); try 3/4/5-state HMM topologies.
- TDNN-HMM: replace the GMM with a TDNN using one of the three topologies in Section 6 (symmetric/asymmetric/subsampled), or the DNN baseline topology, as your starting point; adjust node counts/layers only if your dataset size clearly differs enough from the paper's (~7–16 hours) to justify it, and document any such change as a deviation.
- Build n-gram LM(s) from your own domain transcripts using SRILM (or a modern equivalent); test at least 2-gram and 3-gram; if your domain is broader than the paper's narrow healthcare Q&A domain, consider whether a purely in-domain LM trained on your own transcripts is still appropriate, since the paper's approach specifically avoided general-domain LMs due to domain specificity.

### Step 7 — Fine-tune/Train
Use: Kaldi `nnet3` training recipe.

Training configuration: 5 epochs; initial LR 0.01, final LR 0.001 (linear/exponential decay schedule across epochs is standard in Kaldi but not confirmed exactly by the paper). All other hyperparameters (batch size, optimizer, weight decay, gradient clipping, precision, seed) are not specified in the paper — you must choose Kaldi `nnet3` recipe defaults or your own values and document them explicitly, since they cannot be copied from the source.

### Step 8 — Run Inference
Use: Kaldi lattice decoding with your trained acoustic model and n-gram LM; sweep the LM weight (paper swept 1%–25%, with best results consistently in the 15–25% range) to find the best value for your data — do not assume the paper's optimal weight transfers, since LM weight optimum is data- and LM-size-dependent.

### Step 9 — Evaluate
Calculate:
- WER on your held-out, speaker-independent test set, per model/configuration.
- Word- and phoneme-level confusion analysis on your best model(s), to identify systematic error categories (same-phoneme-group confusions, substring/homophone substitutions, particle-word insertions/deletions were the categories found in the original study — check whether these transfer to your language/domain or whether new categories emerge).
- If your dataset includes a mismatched-domain or mismatched-speaker-population test set (e.g., children's speech when trained on adults, as in the original study), use PER instead of WER for that specific evaluation, since severe vocabulary mismatch inflates WER in a way that obscures acoustic-model quality.

### Step 10 — Compare Against Baseline
Compare your new results against Section 10's table, but explicitly account for: total training hours, vocabulary size/domain narrowness, number of speakers, recording quality/environment, and whether your target language's phoneme inventory or morphology (e.g., presence/absence of ergative-absolutive structure, code-switching patterns) resembles Filipino/Bisaya. A large gap in any of these factors makes direct WER comparison unreliable, even if the underlying method is faithfully reproduced.

---

## 12. What Changes When Using a Different Dataset?

### Fixed (should remain essentially unchanged)
- The overall pipeline shape: audio prep → transcript prep → speaker-independent split → MFCC+CMVN(+iVector) features → HMM-GMM baseline → TDNN-HMM hybrid → n-gram-LM decoding → WER/PER evaluation.
- MFCC configuration (25 ms window / 10 ms frameshift / 13 static + Δ + ΔΔ coefficients) — this is a general-purpose ASR feature convention, not specific to Filipino/Bisaya.
- The general HMM-GMM training progression (monophone → triphone → enhancement) and the TDNN-HMM replacement strategy.
- The definition of WER and the rationale for using PER when vocabulary mismatch is severe.

### Dataset-dependent (may need adjustment)
- Sampling rate, channel count, and any resampling/normalization needed to reach a consistent format.
- Noise-screening/reduction approach and thresholds (paper's rule — discard if noise is "too loud," like dog barks/cars — is qualitative, not a hard threshold).
- Train/test split ratio and whether a validation set is warranted.
- Amount of training data available, which directly affects whether TDNN models will outperform a plain DNN (in this study, more data clearly helped Filipino's TDNN models pull ahead of DNN, while Bisaya's smaller corpus meant the plain DNN baseline actually won).
- LM order and LM weight sweep range/optimum.

### Model-dependent (determined by the chosen architecture/toolkit)
- Number of TDNN layers, nodes per layer, and time-stride configuration — these were chosen for a small (~7–16 hour), narrow-vocabulary corpus; a larger or more diverse dataset may support (or require) a different capacity.
- iVector dimensionality and any Kaldi recipe defaults not specified in the paper.
- Whether to include volume perturbation, and at what strength.

### Implementation-dependent (left unspecified by the paper — must be decided during reproduction)
- Optimizer, batch size, weight decay, gradient clipping, precision, random seed, checkpointing strategy, early-stopping policy for NN training.
- Exact noise-reduction algorithm/tool.
- CMVN scope (per-utterance vs. per-speaker).
- Beam widths and other decode-time search parameters.
- OOV/`<UNK>` handling policy.
- Windowing function used in MFCC extraction (Kaldi default vs. paper's actual configuration).

| Component | Original Paper | New Dataset (example) | Action |
|---|---|---|---|
| Sampling rate | 16 kHz | e.g. 48 kHz or 8 kHz | Resample to one consistent rate |
| Phoneme set | PS27/PS35 (Filipino/Bisaya-specific) | A different language | Design or adopt a phoneme set appropriate to the new language; do not reuse PS27/PS35 unless the language is phonologically very close to Filipino/Bisaya |
| Speakers | 23 (Filipino) / 7 (Bisaya), speaker-independent split | Varies | Recreate the speaker-independent split with your own fixed seed |
| Dataset size | 16.3 h (Filipino) / 8.97 h (Bisaya) | Varies | If much smaller, expect the plain DNN or HMM-GMM+SAT to be competitive with or beat TDNN (as happened with Bisaya); if much larger, consider deeper/larger TDNN or even end-to-end approaches, which the paper explicitly avoided due to data scarcity |
| Vocabulary | Narrow, healthcare Q&A domain (<1,000 unique words) | Possibly open-domain / larger vocabulary | Rebuild the LM and lexicon from scratch on the new domain; a domain-specific n-gram trained only on the new transcripts (as the paper did) may not generalize if the new domain is broad — consider a larger/general-domain LM instead |

---

## 13. Reproduction Checklist

### Dataset
- [ ] Audio collected
- [ ] Transcripts available (word-level, and phoneme-level if replicating the HMM/TDNN-HMM lexicon approach)
- [ ] Audio format standardized (consistent sample rate, channel count)
- [ ] Audio quality checked; unrecoverable-noise files discarded, light-noise files cleaned
- [ ] Speed perturbation (and/or other augmentation) applied and documented
- [ ] Transcript normalization completed (lowercase, no punctuation, number-spelling rule decided, code-switch/affix rule decided)
- [ ] Phoneme set chosen/designed and phoneme transcripts produced (if applicable)
- [ ] Invalid/unusable samples removed
- [ ] Speaker IDs recorded for every utterance

### Dataset Construction
- [ ] Train/test split created, speaker-independent, with a documented random seed
- [ ] (Optional) validation split created, since the paper does not define one
- [ ] Speaker leakage checked across train/test, including augmented copies
- [ ] Dataset statistics recorded (speakers, hours, unique words, total words, audio-file counts) per split

### Model
- [ ] Kaldi (or equivalent HMM-GMM/TDNN-HMM-capable toolkit) set up
- [ ] Lexicon/pronunciation dictionary built from phoneme transcripts
- [ ] HMM-GMM baseline trained (monophone → triphone) and enhancement variants (LDA+MLLT/VTLN/SAT combinations) configured
- [ ] TDNN/DNN topology selected (symmetric / asymmetric / subsampled / plain DNN) and time-stride configuration set
- [ ] iVector extraction and volume perturbation configured for NN models
- [ ] n-gram LM(s) built from in-domain transcripts (2-gram and 3-gram at minimum)

### Training
- [ ] HMM states (3/4/5) swept, if replicating that experiment
- [ ] NN training configuration set (5 epochs, LR 0.01→0.001, or your own documented deviation)
- [ ] All unspecified hyperparameters (optimizer, batch size, seed, etc.) explicitly chosen and recorded
- [ ] Checkpoints saved
- [ ] Best model selected per configuration

### Evaluation
- [ ] Test inference performed with LM weight swept (paper's range: 1%–25%)
- [ ] WER calculated for each model/configuration
- [ ] PER calculated for any mismatched-domain/mismatched-population evaluation (e.g., children's speech)
- [ ] Word-level confusion analysis performed on best models
- [ ] Phoneme-level confusion analysis performed on best models
- [ ] Results compared against Section 10's baseline table, with dataset differences explicitly accounted for

---

## 14. Missing / Ambiguous Implementation Details

- **Random seed for the speaker-independent split.** Not specified in the paper. Matters because it determines exactly which speakers are held out, which affects WER. Cannot be inferred. Decision needed: choose and record your own seed; do not expect to reproduce the paper's exact split.

- **Validation set existence and use.** Not specified in the paper — only train/test is described. Matters because NN training decisions (e.g., epoch count) may normally be validation-driven, but the paper uses a fixed 5-epoch schedule with no stated validation-based early stopping. Can be reasonably inferred that no validation set was used for stopping. Decision needed: decide whether to add a validation split of your own for model selection, understanding this is an addition beyond the original method.

- **Baseline DNN layer count.** Table 4.3 says 3 layers; body text (§4.4.4) says 4 hidden layers, both citing ~3.1 million parameters. Matters because it is the point of comparison for all TDNN variants. Cannot be fully resolved from the text alone. Decision needed: pick one (4 layers is more consistent with the "vanilla DNN with network context [-7,7] and 4 hidden layers" phrasing) and document the choice; note the discrepancy if publishing a reproduction.

- **iVector dimensionality.** Not specified in the paper for this study's own models (100-dim iVectors appear only in cited related work). Matters for NN input dimensionality. Decision needed: use a standard Kaldi recipe default (commonly 100-dim) and document it as your own choice.

- **CMVN scope (per-speaker vs. per-utterance).** Not specified. Matters for how normalization statistics are pooled, especially with few utterances per speaker. Decision needed: choose one and document it; per-speaker is more standard in Kaldi recipes when enough per-speaker data exists.

- **Decoding beam widths and other search parameters.** Not specified. Matters for decoding speed/accuracy trade-off and reproducibility of exact WER. Decision needed: use Kaldi recipe defaults, document them, and note that small WER differences may stem from these unlisted search parameters.

- **Exact noise-reduction algorithm.** Not specified beyond "light noise reduction." Matters because it affects acoustic feature quality on the retained (imperfect) recordings. Decision needed: choose and document a specific tool/algorithm (e.g., spectral gating).

- **N-gram order actually available vs. tested.** Chapter 1 mentions 2-, 3-, and 4-gram experiments; Chapter 4/5 report results only for 2-gram and 3-gram. Matters because a reproduction attempting to also test 4-gram will have no baseline result to compare against. Can be inferred that 4-gram was either dropped or not reported. Decision needed: treat 4-gram as an open, unreported experiment if you choose to run it.

- **VTLN linear vs. non-linear form used in experiments.** Both forms are described theoretically (Ch.3), but the specific experimental results (Ch.5) do not state which form was actually applied. Matters for exact reproducibility of the VTLN-enhanced models' numbers. Decision needed: choose one (linear VTLN is more standard in Kaldi's stock recipes) and document it.

- **Cebuano/ISIP Project 6 corpus contribution to the Bisaya dataset.** Section 1.5.1 mentions this corpus was used to supplement Bisaya data, but Chapter 4/5's Bisaya corpus statistics (7 speakers, 8.97 hours) make no separate mention of it. Matters because it affects whether the reported 8.97-hour Bisaya figure already includes this supplementary data or not. Cannot be resolved from the text. Decision needed: when reproducing, treat your own supplementary data sourcing as independent of this ambiguity, and do not assume any specific proportion of "supplementary vs. primary" data in the paper's Bisaya corpus.

- **Optimizer, weight decay, gradient clipping, precision, batch size for NN training.** None of these are specified. Matters for exact reproducibility of training dynamics and possibly final WER. Cannot be inferred beyond "standard Kaldi nnet3 recipe defaults were probably used." Decision needed: adopt Kaldi `nnet3`'s recipe defaults explicitly and document them as your own choice, not the paper's.

- **Word/audio-file count discrepancies (Table 5.2 vs. body text).** As noted in Section 2, the reported audio-file counts for Bisaya and Filipino+Additional Data differ between the table and the surrounding prose. Matters only if you are trying to cross-validate the original dataset's exact statistics; does not affect the reproducibility of the *method* itself. No decision needed beyond awareness.
