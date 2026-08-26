# tri3 (SAT HMM-GMM, PS27, 2-gram) -- deployable model

Curated subset of `train_kaldi.ipynb`'s trained `exp/tri3` output -- just
the files needed to decode new audio, not the training-only artifacts
(per-job alignments, FSTs, occupancy stats, training logs, per-speaker
training-set fMLLR transforms). Regenerate by re-running `train_kaldi.ipynb`
through Section 15; this folder is gitignored as a reproducible build
output, same as `data/` and `output/`.

| File | Purpose |
|---|---|
| `final.mdl` | Trained acoustic model (GMM-HMM, SAT). |
| `final.alimdl` | Alignment model used for the first-pass (pre-fMLLR) decode. |
| `final.mat` | LDA transform. |
| `full.mat` | Full-dimension LDA transform (pre-dimensionality-reduction). |
| `tree` | Phonetic decision tree (context-dependency). |
| `cmvn_opts` / `splice_opts` | Feature config the model was trained with -- must match at decode time. |
| `phones.txt` | Phone symbol table. |
| `graph/` | Prebuilt decode graph (`HCLG.fst` + symbol tables) for the 2-gram LM in `data/lang_2g`. Rebuild with `utils/mkgraph.sh` if the LM changes. |

## Decoding new audio

Needs a Kaldi checkout with `steps/`/`utils/` available. Build a Kaldi
data directory for the new audio (`wav.scp`, `text` if references are
known, `utt2spk`/`spk2utt`), extract MFCC + per-speaker CMVN the same way
`train_kaldi.ipynb` Section 12 does, then:

```bash
steps/decode_fmllr.sh --cmd run.pl --nj <N> \
  --beam 30 --lattice-beam 15 \
  --scoring-opts "--min-lmwt 1 --max-lmwt 25" \
  models/tri3/graph <new-data-dir> <decode-output-dir>
```

`--nj` must not exceed the new data's speaker count (`decode_fmllr.sh`
splits work per-speaker). See `CLAUDE.md`'s gotchas list for why the
`--beam`/`--scoring-opts` flags above aren't the Kaldi defaults.
