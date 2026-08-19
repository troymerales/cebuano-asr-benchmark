Filipino ASR studies are primarily focused on the traditional HMM-GMM approach. Studies on Bisaya ASR are also scarce if any. Numerous studies have
employed neural network methodologies and achieved favorable outcomes. Most
of these studies revolve around end-to-end systems which require massive amounts
of data. The reason Philippine languages rarely see any neural network approaches
is mainly due to the need for more speech data. Although, one way to mitigate
this is to employ a hybrid TDNN-HMM model which still needs more data than an
HMM model but less than an end-to-end model. With this being said, this study
was able to collect additional Filipino speech data on top of already available data
and analyze it, develop a baseline HMM-GMM and explore model enhancement
techniques, and develop a TDNN-HMM-based ASR system.
This study collected 4 additional Filipino speakers’ worth of data totaling 4.49
hours. The data is already segmented into single responses, preprocessed to reduce
noise, and transcribed at both word level and phoneme level. This dataset is used
as training data for the Filipino HMM and NN models. As mentioned in the
analysis of the effects of these additional data, the collection of additional Bisaya
speech data may see a significant increase in performance in Bisaya NN models
as the Filipino NN models have.
The study also analyzed the phoneme distribution of the speech data of both
Filipino and Bisaya speech. For both Filipino and Bisaya, PS27 is the same
as PS35 except for the diphones being distributed to already existing phonemes.
The phoneme distribution of Filipino and Bisaya is relatively similar to each other
with some subtle differences. Phonemes used exclusively for English words and
79
brands are also identified through this. These phonemes are also one of the least
frequently used. However, it may be essential when transcribing conversational
speech since English code-switching is fairly common in both Filipino and Bisaya.
Although arguably, phonemes such as /f/, /v/, /th/, and /z/ are sometimes
pronounced as /p/, /b/, /t/, and /s/ depending on the speaker’s preference.
The study presented multiple HMM-GMM models for both Filipino and Bisaya.
There were various experiments made on the phoneme set, n grams, HMM states,
language model weights, and model enhancement techniques such as VTLN,
LDA+MLLT, and SAT. The best HMM-GMM models are the 3-gram 3-state
SAT using PS27 for Filipino with a 3.96% WER and the 2-gram 3-state SAT
using PS27 for Bisaya with a 5.41% WER. Overall, the 3-gram language model
performed the best for Filipino while the 2-gram language model performed the
best for Bisaya. The number of HMM states seems to have varying effects on the
performance with no clear indication of improvement. For model enhancement
technique, The SAT is the best performing out of all for both Filipino and Bisaya.
On the other hand, both VTLN and LDA+MLLT had little to no significant effects on the performance. The study also delves deeper into the word-level analysis
which shows 3 categories with which the models are struggling. First, phonemes
within the same phoneme group are often substituted with one another. Second,
the substring problem wherein a word that is a substring to another longer word
is substituted with each other. This is also similar to the problem of (Ing et al.,
2022) wherein compound words are sometimes decoded as two separate words.
The last problem is homophones wherein the word is completely pronounced the
same but is a different word. It also shows that the model, in some cases, inserts
or deletes enclitic or particle words. Further looking into the phoneme level analysis confirms the substitutions and identifies the problematic phonemes within
the same phoneme group. The results also point to PS27 being slightly better
since the phoneme analysis shows that models that use PS35 sometimes introduce redundancy in the transcriptions.
The study also presented multiple hybrid NN-HMM models for both Filipino
and Bisaya. The best NN models are the 3-gram 5-state TDNN asymmetrical model using PS27 for Filipino with a 3.48% WER and the 2-gram 5-state
DNN-HMM model using PS35 for Bisaya with a 5.50% WER. The Filipino model
improved by about 0.5% WER but the Bisaya model saw no change in performance. Thus, the Bisaya model’s word level analysis and phoneme level analysis
are almost the same as its HMM-GMM counterpart. Since the study compared
the performance of the models trained with different amounts of data, the trend
showed that adding more Bisaya training data would yield an improvement similar
to Filipino models. Out of the 3 problem categories mentioned before, the models improved significantly on the words with phonemes within the same phoneme
80
group. The substring and homophone problem also improved but it is limited.
Since the experiment focused on the improvement of the acoustic model, it is
expected that the latter categories see little improvement; most of the instances
could be decoded correctly with a better language model. Thus, future works
could explore a more appropriate approach which is to employ a larger language
model with examples of these substrings and homophones. Future works could
also revolve around the modification of the topology of the neural network approaches and other neural network architectures such as RNN and LSTM.
The study also experimented with using the acoustic model for the crosslanguage model. The Filipino acoustic model is used in Bisaya speech and vice
versa. The results show that although the models performed on a subpar level, the
performance is still reasonable in terms of WER. Future research could explore
utilizing cross-language models on other Philippine languages or dialects with a
limited amount of data. Although not optimal, this could be a great alternative.
Lastly, the study also evaluated the best models for actual children’s speech
in healthcare. For both Filipino and Bisaya models, the phoneme error rate was
poor. It seems that training exclusively on female adult speech is not sufficient
when evaluating children’s speech. There are multiple factors leading to this such
as the nature of speech, frequency of voice, quality of the recording, and verbal
disfluencies. Future works could explore transfer learning approaches wherein
models trained on adult speech such as the models in this study are fine-tuned
further with children’s speech. Another possible experiment that could be done is
by training on formant modified speech instead of only speed-perturbed speech.
This could modify the training data to match the formant qualities of children’s
speech better. To address the poor recording quality of the data, training on data
with noise or noise augmentation could assist in creating a noise-robust model.
