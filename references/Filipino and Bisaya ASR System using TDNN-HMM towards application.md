**De La Salle University** 

#### **Animo Repository** 

Software Technology Master's Theses 

Software Technology 

2023 

#### **Filipino and Bisaya ASR System using TDNN-HMM towards application in a healthcare chatbot** 

John Andrew Ing 

Follow this and additional works at: https://animorepository.dlsu.edu.ph/etdm_softtech 

###### **Recommended Citation** 

Ing, J. (2023). Filipino and Bisaya ASR System using TDNN-HMM towards application in a healthcare chatbot. Retrieved from https://animorepository.dlsu.edu.ph/etdm_softtech/9 

This Master's Thesis is brought to you by the Software Technology at Animo Repository. It has been accepted for inclusion in Software Technology Master's Theses by its authorized administrator. 



<!-- Start of picture text -->
Fr or Uns Lifeat<br>f | “ |<br>‘7 A ‘ it<br><!-- End of picture text -->

### Filipino and Bisaya ASR System Using TDNN-HMM Towards Application in a Healthcare Chatbot 

A Thesis 

Presented to 

the Faculty of the College of Computer Studies De La Salle University Manila 

In Partial Fulfillment 

of the Requirements for the Degree of Master of Science in Computer Science 

by 

ING, John Andrew 

Ronald PASCUAL Adviser 

August 10, 2023 

###### **Abstract** 

Although there have been previous studies on Filipino ASR, it is primarily focused on the Hidden Markov Model (HMM) with the Gaussian Mixture Model (GMM) approach. Studies on Bisaya ASR are much more limited in terms of resources such as speech corpus and previous works. There is a lack of neural network or end-to-end system studies because of this since neural networks require massive amounts of data to train. An alternative to this would be the hybrid model which makes use of both neural networks and HMM. This neural network architecture would still need data but not as much as an end-to-end ASR system. To address these opportunities, this study makes use of De La Salle University’s healthcare chatbot project speech corpus for the Filipino and Bisaya languages. Furthermore, this study collected, preprocessed, as well as transcribed additional Filipino speech data. With these data, the study also presented an HMM-GMM ASR system similar to previous studies as a baseline. This study also experimented with phoneme sets, _n_ -grams, language model weights, HMM states, and model enhancement techniques. The study found that the best models for both Filipino and Bisaya used SAT with a 3.96% WER AND 5.41% WER respectively. The study also developed a deep neural network (DNN) HMM baseline model and time delay neural network (TDNN) HMM models with symmetric, asymmetric, and subsampled time strides. For Filipino, the best model is the asymmetric TDNN-HMM model with a 3.48% WER. For Bisaya, the best model is the baseline DNN-HMM model with a 5.50% WER. Furthermore, the study also explored numerous experiments which are: 1) the effects of additional data with respect to performance, 2) the performance of the models on actual conversational children’s speech, and 3) the performance of using cross-language acoustic models. 

**Keywords:** Automated Speech Recognition, Filipino Language, Bisaya Language, Healthcare 

## **Contents** 

|**1**<br>**Res**|**earch **|**Description**<br>**1**|
|---|---|---|
|1.1|Overv|iew of the Current State of Technology . . . . . . . . . . . .<br>1|
|1.2|Resea|rch Objectives . . . . . . . . . . . . . . . . . . . . . . . . . .<br>3|
||1.2.1|General Objectives . . . . . . . . . . . . . . . . . . . . . .<br>3|
||1.2.2|Specifc Objectives . . . . . . . . . . . . . . . . . . . . . .<br>3|
|1.3|Scope|and Limitations of the Research<br>. . . . . . . . . . . . . . .<br>4|
|1.4|Signif|cance of the Research<br>. . . . . . . . . . . . . . . . . . . . .<br>5|
|1.5|Resea|rch Methodology . . . . . . . . . . . . . . . . . . . . . . . .<br>6|
||1.5.1|Data Collection and Preparation<br>. . . . . . . . . . . . . .<br>6|
||1.5.2|Data Preparation . . . . . . . . . . . . . . . . . . . . . . .<br>6|
||1.5.3|Transcription . . . . . . . . . . . . . . . . . . . . . . . . .<br>6|
||1.5.4|Data Analysis . . . . . . . . . . . . . . . . . . . . . . . . .<br>7|
||1.5.5|Automatic Speech Recognition . . . . . . . . . . . . . . . .<br>7|
|**2**<br>**Rev**|**iew of**|**Related Literature**<br>**9**|
|2.1|Autom|ated Speech Recognition<br>. . . . . . . . . . . . . . . . . . .<br>9|
||2.1.1|Signal Processing/Feature Extraction Methods . . . . . . .<br>10|
||2.1.2|Acoustic Models<br>. . . . . . . . . . . . . . . . . . . . . . .<br>11|



ii 

||2.1.3<br>Language Models . . . . . . . . . . . . . . . . . . . . . . .<br>13|
|---|---|
|2.2|Philippine Languages ASR . . . . . . . . . . . . . . . . . . . . . .<br>13|
|2.3|Low Resource ASR . . . . . . . . . . . . . . . . . . . . . . . . . .<br>14|
|2.4|Children ASR . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>16|
|2.5|Time Delay Neural Network . . . . . . . . . . . . . . . . . . . . .<br>18|
|**3**<br>**The**|**oretical Framework**<br>**21**|
|3.1|Filipino and Bisaya . . . . . . . . . . . . . . . . . . . . . . . . . .<br>21|
|3.2|Phonemes and Transcriptions<br>. . . . . . . . . . . . . . . . . . . .<br>22|
|3.3|Feature Extraction and Model Enhancement Techniques<br>. . . . .<br>25|
||3.3.1<br>Mel Frequency Cepstral Coefcients . . . . . . . . . . . . .<br>25|
||3.3.2<br>Cepstral Mean and Variance Normalization . . . . . . . . .<br>26|
||3.3.3<br>Vocal Tract Length Normalization . . . . . . . . . . . . . .<br>26|
||3.3.4<br>Linear Discriminant Analysis<br>. . . . . . . . . . . . . . . .<br>27|
||3.3.5<br>Speaker Adaptive Training . . . . . . . . . . . . . . . . . .<br>27|
|3.4|Language Model . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>28|
|3.5|Hidden Markov Model . . . . . . . . . . . . . . . . . . . . . . . .<br>29|
|3.6|Time Delay Neural Network . . . . . . . . . . . . . . . . . . . . .<br>30|
|**4**<br>**Res**|**earch Methodology**<br>**33**|
|4.1|Speech Corpus<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>33|
|4.2|Data Collection and Data Preparation<br>. . . . . . . . . . . . . . .<br>34|
||4.2.1<br>Audio Recording<br>. . . . . . . . . . . . . . . . . . . . . . .<br>35|
||4.2.2<br>Preprocessing . . . . . . . . . . . . . . . . . . . . . . . . .<br>35|
||4.2.3<br>Speech Transcription . . . . . . . . . . . . . . . . . . . . .<br>35|



iii 

|4.3|Data|Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>36|
|---|---|---|
|4.4|ASR|Models and Experiments . . . . . . . . . . . . . . . . . . . .<br>37|
||4.4.1|Phoneme Set and HMM States<br>. . . . . . . . . . . . . . .<br>37|
||4.4.2|Language Model<br>. . . . . . . . . . . . . . . . . . . . . . .<br>38|
||4.4.3|Model Enhancement Experiments . . . . . . . . . . . . . .<br>38|
||4.4.4|Neural Network Approaches . . . . . . . . . . . . . . . . .<br>38|
||4.4.5|Efects of Additional Data . . . . . . . . . . . . . . . . . .<br>40|
||4.4.6|Cross-Language Acoustic Model Experiment . . . . . . . .<br>40|
|4.5|Evalu|ation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>40|
|**5**<br>**Res**|**ults a**|**nd Discussion**<br>**42**|
|5.1|Addit|ional Speech Data<br>. . . . . . . . . . . . . . . . . . . . . . .<br>42|
|5.2|Data|Analyses . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>43|
|5.3|ASR|Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>49|
||5.3.1|HMM-GMM Filipino ASR . . . . . . . . . . . . . . . . . .<br>50|
||5.3.2|HMM-GMM Bisaya ASR . . . . . . . . . . . . . . . . . . .<br>57|
||5.3.3|Filipino Neural Network Approaches<br>. . . . . . . . . . . .<br>61|
||5.3.4|Bisaya Neural Network Approaches . . . . . . . . . . . . .<br>67|
||5.3.5|Summary of Best Models . . . . . . . . . . . . . . . . . . .<br>70|
|5.4|Expe|riments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .<br>73|
||5.4.1|Efects of Additional data on ASR performance<br>. . . . . .<br>73|
||5.4.2|Evaluation of Models on Children’s Speech . . . . . . . . .<br>76|
||5.4.3|Cross-Language Acoustic Model . . . . . . . . . . . . . . .<br>76|
||5.4.4|Language Model Weights . . . . . . . . . . . . . . . . . . .<br>77|



iv 

|**6**|**Conclusions and Recommendations**|**79**|
|---|---|---|
|**A **|**Research Ethics Documents**|**82**|
|**B **|**Personal Vitae**|**94**|
|**Re**|**ferences**|**95**|



v 

## **List of Figures** 

|2.1|Architecture of an ASR system<br>. . . . . . . . . . . . . . . . . . .|10|
|---|---|---|
|3.1|A detailed diagram of the sample sentences in Filipino and Bisaya<br>as compared to English . . . . . . . . . . . . . . . . . . . . . . . .|22|
|3.2|An overview of a TDNN model wherein there are n layers and each<br>layer has a symmetrical time stride ∆_n_ . . . . . . . . . . . . . . .|31|
|5.1|Filipino Distribution of Phonemes for PS27 . . . . . . . . . . . . .|44|
|5.2|Bisaya Distribution of Phonemes for PS27<br>. . . . . . . . . . . . .|45|
|5.3|Bisaya Distribution of Phonemes for PS35<br>. . . . . . . . . . . . .|45|
|5.4|Bisaya Distribution of Phonemes for PS35<br>. . . . . . . . . . . . .|46|
|5.5|Sound waves of the word _oo_ with phoneme transcription<br>. . . . .|53|
|5.6|Sound waves of the words _ko alam_ with phoneme transcription . .|54|
|5.7|Line Graph of the relationship between the amount of data and its<br>efects on Filipino NN models’ WER<br>. . . . . . . . . . . . . . . .|75|
|5.8|Line Graph of the relationship between the amount of data and its<br>efects on Bisaya NN models’ WER . . . . . . . . . . . . . . . . .|75|
|5.9|Line graph of the WER over the LM weight for Filipino models<br>.|78|
|5.10|Line graph of the WER over the LM weight for Bisaya models . .|78|



vi 

## **List of Tables** 

|2.1|A summary of ASR studies. . . . . . . . . . . . . . . . . . . . . .|10|
|---|---|---|
|2.2|A summary of Philippine Language ASR studies.<br>. . . . . . . . .|15|
|2.3|A summary of transfer learning studies. . . . . . . . . . . . . . . .|16|
|2.4|A summary of data augmentation studies.<br>. . . . . . . . . . . . .|16|
|2.5|A summary of Children ASR studies. . . . . . . . . . . . . . . . .|18|
|2.6|A summary of Time Delay Neural Network studies. . . . . . . . .|20|
|3.1|Simplifed International Phonetic Alphabet . . . . . . . . . . . . .|23|
|3.2|Phonemes for PS27 and PS35 . . . . . . . . . . . . . . . . . . . .|24|
|3.3|Mapping of PS27/PS35 Phonemes to its IPA Equivalent<br>. . . . .|24|
|4.1|General physical wellness assessment<br>. . . . . . . . . . . . . . . .|34|
|4.2|Filipino Phonemes for PS27 and PS35<br>. . . . . . . . . . . . . . .|37|
|4.3|An overview of the neural network approaches . . . . . . . . . . .|39|
|5.1|A summary of the speech corpora used in this study . . . . . . . .|42|
|5.2|A summary of the number of words and audio fles of the speech<br>corpora<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|43|
|5.3|Most frequently occurring words in Filipino<br>. . . . . . . . . . . .|46|
|5.4|Most frequently occurring words in Bisaya . . . . . . . . . . . . .|47|



vii 

|5.5|Most frequently occurring 2-grams in Filipino<br>. . . . . . . . . . .|48|
|---|---|---|
|5.6|Most frequently occurring 2-grams in Bisaya . . . . . . . . . . . .|48|
|5.7|Most frequently occurring 3-grams in Filipino<br>. . . . . . . . . . .|49|
|5.8|Most frequently occurring 3-grams in Bisaya . . . . . . . . . . . .|49|
|5.9|Overview of WER Results for Filipino HMM-GMM models using<br>PS27 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|50|
|5.10|Overview of WER Results for Filipino HMM-GMM models using<br>PS35 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|51|
|5.11|Most frequent substitutions of the best Filipino models for PS27<br>and PS35<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|52|
|5.12|Most frequent deletions and insertions of the best Filipino models<br>for PS27 and PS35 . . . . . . . . . . . . . . . . . . . . . . . . . .|55|
|5.13|Most frequent phoneme errors of the best Filipino models for PS27|56|
|5.14|Most frequent phoneme errors of the best Filipino models for PS35|56|
|5.15|Overview of WER Results for Bisaya HMM-GMM models using PS27|57|
|5.16|Overview of WER Results for Bisaya HMM-GMM models using PS35|58|
|5.17|Most frequent substitutions of the best Bisaya models for PS27 and<br>PS35 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|59|
|5.18|Most frequent deletions and insertions of the best Bisaya models<br>for PS27 and PS35 . . . . . . . . . . . . . . . . . . . . . . . . . .|59|
|5.19|Most frequent phoneme errors of the best Bisaya models for PS27|60|
|5.20|Most frequent phoneme errors of the best Bisaya models for PS35|61|
|5.21|Overview of WER Results for Filipino neural network models using<br>PS27 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|62|
|5.22|Overview of WER Results for Filipino neural network models using<br>PS35 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|62|



viii 

|5.23 Most frequent substitutions of the best Filipino neural network<br>models for PS27 and PS35 . . . . . . . . . . . . . . . . . . . . . .|63|
|---|---|
|5.24 Most frequent deletions and insertions of the best Filipino neural<br>network models for PS27 and PS35 . . . . . . . . . . . . . . . . .|63|
|5.25 Most frequent phoneme errors of the best Filipino neural network<br>models for PS27 . . . . . . . . . . . . . . . . . . . . . . . . . . . .|64|
|5.26 Most frequent phoneme errors of the best Filipino neural network<br>models for PS35 . . . . . . . . . . . . . . . . . . . . . . . . . . . .|65|
|5.27 Summary of average training time and average inference time per<br>response for Filipino neural network models<br>. . . . . . . . . . . .|66|
|5.28 Comparison of Filipino NN models’ efciency performance<br>. . . .|66|
|5.29 Overview of WER Results for Bisaya neural network models using<br>PS27 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|67|
|5.30 Overview of WER Results for Bisaya neural network models using<br>PS35 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|68|
|5.31 Most frequent substitutions of the best Bisaya neural network mod-<br>els for PS27 and PS35<br>. . . . . . . . . . . . . . . . . . . . . . . .|68|
|5.32 Most frequent deletions and insertions of the best Bisaya neural<br>network models for PS27 and PS35 . . . . . . . . . . . . . . . . .|69|
|5.33 Summary of average training time and average inference time per<br>response for Bisaya neural network models . . . . . . . . . . . . .|70|
|5.34 Comparison of Bisaya NN models’ efciency performance . . . . .|70|
|5.35 Summary of the Best Filipino and Bisaya models<br>. . . . . . . . .|71|
|5.36 Most frequent phonemes in Filipino and the PER of the best models|72|
|5.37 Least frequent phonemes and problematic phonemes in Filipino and<br>the PER of the best models<br>. . . . . . . . . . . . . . . . . . . . .|72|
|5.38 Most frequent phonemes in Bisaya and the PER of the best models|72|
|5.39 Least frequent phonemes and problematic phonemes in Bisaya and<br>the PER of the best models<br>. . . . . . . . . . . . . . . . . . . . .|73|



ix 

- 5.40 Comparison of Results of Filipino neural network models with and without additional data . . . . . . . . . . . . . . . . . . . . . . . . 74 

- 5.41 Results of the best Filipino and Bisaya models on children’s speech 76 5.42 Results for models evaluated on cross-language . . . . . . . . . . . 77 

x 

## **Chapter 1** 

## **Research Description** 

This chapter presents an overview of the current state of technology in the domain of automated speech recognition. This chapter also discusses the field of Filipino automated speech recognition. Furthermore, it discusses the research objectives, the scope and limitations of the research, and the significance of the study. 

### **1.1 Overview of the Current State of Technology** 

Automated speech recognition (ASR) systems are used to convert audio into phonemes or words. They are most commonly known as speech-to-text systems or transcription systems. These systems have previously been effectively used in more developed languages such as English and Mandarin. With Google’s English ASR being as low as a 9% word error rate (WER), the task of converting English audio to text is practically solved. 

Early attempts at automated speech recognition usually utilized the Hidden Markov Model (HMM) and Gaussian Mixture Model (GMM) acoustic models (Rabiner, 1989; Juang, Levinson, & Sondhi, 1986). Due to its great performance in speech, the HMM-GMM model is one of the most used models in the field of ASR both then and even now due to its innate ability to model time-series data such as speech (Swietojanski, Ghoshal, & Renals, 2013; Tan et al., 2021). 

However, with the rise in popularity of neural networks in the field of machine learning, studies on an ASR system utilizing neural network approaches such as HMM-Artificial Neural Network (ANN), HMM-Deep Neural Network (DNN), and Recurrent Neural Network (RNN) have been explored and have had great 

1 

success (Chen & Cheng, 2014; Amodei et al., 2016; Yeung & Alwan, 2018). It even opened up opportunities to frame the ASR task into an image classification problem by using the audio’s spectrogram and feeding it into a Convolutional Neural Network (CNN), a network known for its application on images (Salido et al., 2017). However, some of the limitations of neural networks are the huge amount of data as well as the computing power required to be able to train them to reach a low WER. Thus, there are studies directed toward transfer learning. Kunze et al. (2017) proposed a technique wherein the first several layers of a pretrained neural network were frozen and the rest was trained on the target data. Another interesting approach was by Tong, Wang, and Ma (2017) wherein they used techniques such as acoustic adaptation and multi-task learning. 

The Philippines has over 120 actively spoken languages. The top two languages are Tagalog, the basis of Filipino, and Cebuano or Bisaya. The field of Filipino ASR research has been stimulated through the work of Guevara et al. (2002) who provided a Filipino Speech Corpus (FSC). The FSC has been used by various studies in different domains because it contains read speech as well as spontaneous speech in Filipino (Chua, Chua, de Padua, Tan, & Cheng, 2011; Bautista & Kim, 2014; Fadri, 2017). However, Ang, Miyanaga, Guevara, Cajote, and Bayona (2014) could not utilize the FSC because of one specific problem they identified, code-switching. In any practical conversation in Filipino or even Bisaya, speakers usually code-switch from one language to another. This motivated the study to create a speech corpus with code-switching present. Similarly, a study by (Lim, Xu, Lin, Chen, & Pascual, 2022) created a speech corpus of Filipino news with English code-switching. Studies on Bisaya ASR are much more limited in terms of resources such as speech corpus and previous works. However, some studies propose techniques to mitigate the effects of scarce data through grapheme-tophoneme (Aquino, Tsang, Lucas, & de Leon, 2019) and reusing an acoustic model from a phonologically similar language (Prasad, van Esch, Ritchie, & Mortensen, 2019). 

ASR systems for children have also been a point of interest in the field since 1) there is a lack of large-scale children’s speech corpora, 2) children are prone to reading miscues and disfluencies (Pascual & Guevara, 2012) as well as a limited proficiency in vocabulary and grammar, and 3) children’s speech is typically higher in pitch because of physical differences in their speech organs. These challenges make it so that ASR systems that are trained on adult data perform worse on children’s speech. Multiple transfer learning methods have mainly addressed these hurdles to children’s ASR. The study of (Tong et al., 2017) proposed two transfer learning methods under deep neural networks: acoustic adaptation and multi-task learning. Both show children’s ASR can benefit from transfer learning by reducing the data needed. A rather different approach is explored by (Sheng, Yang, & Qian, 

2 

2019) in which they effectively used generative adversarial networks to generate augmented data for children ASR. There are also methods such as Vocal Tract Length Normalization (VTLN), which considers the physical difference between adult vocal tract length and children’s vocal tract length (Eide & Gish, 1996). 

In the context of Philippine languages in children’s ASR, one of the notable contributions to the field is by Pascual and Guevara (2012). They developed the Filipino Children’s Speech Corpus (FCSC). Their goal was to analyze the reading miscues and disfluencies of Filipino-speaking children to be able to develop a reading miscue detector which will then be used to develop an automated reading tutor system. Recent studies have capitalized on this corpus such as Briones, Cai, Te, and Pascual (2020) which developed a word-level ASR system for continuous speech in Filipino children. Another study by Dimzon and Pascual (2020) uses the CFSC to develop an automatic phoneme recognizer for children’s Filipino read speech. Both Briones et al. (2020) and Dimzon and Pascual (2020) used HMM and experimented with its parameters. Although, these studies are mainly focused on read speech instead of conversational speech. Considering the relatively small speech corpus, a fully end-to-end neural network model may find it hard to converge during training due to the small number of samples. Thus, a great compromise is the DNN-HMM model or more specifically the TDNN-HMM. Several studies such as Georgescu, Cucu, and Burileanu (2019), Peddinti, Povey, and Khudanpur (2015), and Liu, Zhang, Xu, and Chen (2019) have used the TDNN-HMM architecture with success. 

### **1.2 Research Objectives** 

##### **1.2.1 General Objectives** 

To develop a Filipino and Bisaya automatic speech recognition system module aimed toward application in a healthcare chatbot 

##### **1.2.2 Specific Objectives** 

1. To investigate previous methods in Filipino and Bisaya ASR. 

2. To collect additional Filipino female adult speech data and analyze the characteristics of the speech data. 

3 

3. To develop a baseline HMM-GMM-based ASR system and explore model enhancement techniques. 

4. To develop a Filipino and Bisaya TDNN-HMM-based ASR system and to determine the effectiveness of the system on conversational healthcare domain speech. 

### **1.3 Scope and Limitations of the Research** 

The speech corpus used in this study is from De La Salle University’s healthcare chatbot project intended for children’s use (Luci-Atienza, 2021). Due to the children’s speech being only available during the later stages of this study, children’s speech audio is replaced with adult female voice actresses since it is the closest to children’s speech in terms of voice frequency. Although this study is not focused on building an ASR for children, it is still evaluated on the recently available speech corpus. Onto the characteristics of the speech data, an overview of the conversation flow is in the following order: general appearance, allergies, cough, fever, family history, vaccination, review of systems, daily activities, hygiene, play, and sleep. Only the responses are recorded in the speech corpus. It is also already segmented into single responses, preprocessed to remove noise, and transcribed both at the word and phoneme levels. The speech corpus totals 9 Filipino speakers and 7 Bisaya speakers with 9.03 hours and 8.97 hours respectively. The study also made use of 10 speakers from the Filipino Speech Corpus (Guevara et al., 2002) with a total duration of 2.78 hours. On top of this speech corpus, this study collected an additional 4 speakers for Filipino with a total duration of 4.49 hours. Since the study experimented with a neural network approach, more data would be beneficial for the model to learn and generalize speaker-specific features. The additional adult female speech data follows the same format of conversation flow, segmentation, preprocessing, and transcription. The additional data was used to gauge and compare the performance of the models with more data. Although the speech corpus contains English speech data, this study does not utilize this English speech nor collect additional English speech data. 

The development of the baseline HMM-GMM-based ASR model used the Mel Frequency Cepstrum Coefficient (MFCC) as its feature extraction due to its ability to represent speech features as perceived by humans. Then, the Cepstral Mean and Variance Normalization (CMVN) is used to normalize the speech. It is then trained on monophones and then triphones. The language model is an n-gram language model trained on the transcriptions themselves. Along with these, the study also experimented with the number of HMM states and n-grams. This acoustic model setup is similar to earlier works on Filipino ASR; thus, serves as 

4 

a valid baseline for this study. On top of the baseline model, the authors also experimented with model enhancement techniques such as Vocal Tract Length Normalization (VTLN), Linear Discriminant Analysis + Maximum Likelihood Linear Transform (LDA + MLLT), and Speaker Adaptive Training (SAT). 

The development of the TDNN-HMM-based ASR model also used MFCC and CMVN. On top of this, it also used iVectors. The same experiments were applied to the HMM states as well as the n-gram language model. The difference is that the GMM module is replaced with a TDNN module. Aside from the mentioned feature extraction, the TDNN module is also fed with I-vectors which are features that help with speaker adaption. This study also experimented with symmetrical, asymmetrical, and subsampled time strides for the architecture of the TDNN. All of the models mentioned are developed using the Kaldi ASR toolkit (Povey et al., 2011). 

### **1.4 Significance of the Research** 

The aim of this study is to develop a hybrid TDNN-HMM ASR system for both Filipino and Bisaya. This study will be useful for the following: 

- **Filipino ASR and Bisaya ASR fields** : This research will benefit the Filipino and Bisaya ASR fields by providing a neural network approach. This study also contributes an ASR model that may be replicated, compared, or extended 

- **Healthcare chatbot** : This research will benefit Filipino-speaking and Bisayaspeaking people by contributing towards a healthcare chatbot that may help Filipino & Bisaya speakers maintain their health through advice or referral 

- **ASR** : The results of this study will also be of benefit to the ASR field as a whole by contributing an ASR model for Filipino and Bisaya ASR which are considered to be low-resource fields as well as the handling of conversational speech and code-switching 

5 

### **1.5 Research Methodology** 

##### **1.5.1 Data Collection and Preparation** 

The additional data collected matches the format of the already existing speech data. Female adult voice actresses were employed to gather the speech data. It is stored in a WAV file format with a 16 kHz sampling rate. The voice actresses were given an instruction manual that introduced the general objectives of the study. Then, it directs the user visually on how to record the audio. To supplement the speech data, a subset of the Filipino Speech Corpus (FSC) (Guevara et al., 2002) and Cebuano Speech Corpus from the ISIP Project 6 (Ang et al., 2014) is utilized. The study also made use of speed perturbation as data augmentation. 

##### **1.5.2 Data Preparation** 

The audio files are either preprocessed to remove light noises such as static noise or light background noises, or discarded if it contains louder noise that is difficult to remove such as dog barks and passing cars. 

##### **1.5.3 Transcription** 

The speech corpus is transcribed both at the phoneme level and word level. For word-level transcriptions, the transcriptions are lowercase alphanumeric characters. The only time numeric characters are utilized is when the word is a medical term such as /covid 19/. In any other cases, the numbers is spelled out. Medical terms such as UTI, which stands for urinary tract infection, are transcribed as one word /uti/. There are also instances wherein a Filipino or Bisaya prefix and suffix are used with an English root word. An example would be the word natotoothbrush which means brushing one’s teeth. This word is transcribed as two separate words /nagto/ and /toothbrush/. 

For phoneme-level transcriptions, there are two phoneme sets used: 1) Phoneme Set 27 (PS27) which contains 27 monophones, and 2) Phoneme Set 35 which contains 26 monophones and 9 diphones. The only rule in transcribing at the phoneme level is that the diphones in PS35 supersede the monophones to avoid inconsistencies and redundancies in the transcriptions. 

6 

##### **1.5.4 Data Analysis** 

Given there are two languages in the speech corpus, this study compared the two languages in terms of the phoneme distribution. Although Filipino and Bisaya may be phonetically similar, this does not necessarily mean that the distribution of phonemes is also similar. This gave insight into the comparison of the performance of the models on each phoneme and the actual phoneme distribution. This study also looked at the most common 1-gram, 2-gram, and 3-gram to see the most common phrases and how they affected the models. 

##### **1.5.5 Automatic Speech Recognition** 

The Kaldi ASR toolkit (Povey et al., 2015) is used for all speech recognition models. The MFCC is utilized for feature extraction with a 10 ms frameshift and 25 ms window size. The CMVN is used to normalize the speech features. The SRI Language Modeling (SRILM) toolkit is used on the transcriptions to generate the n-gram models utilized by the ASR. This study experimented with 2-gram, 3-gram, and 4-gram language models. The experiment also included exploring 3-, 4-, and 5-state HMMs. 

###### **Model Enhancement Experiments** 

As mentioned, the authors experimented with model enhancement techniques. The following combinations of model enhancement techniques are used: LDA+MLLT, SAT, VTLN, VTLN+LDA+MLLT, and VTLN+SAT. 

###### **TDNN** 

As for the proposed architecture of the TDNN, it is implemented using Kaldi’s premade nnet3 recipe. It is a TDNN with six layers with ReLU activation. Its time strides are symmetrical; the number of left contexts is the same as the right contexts. This study experimented with asymmetrical time strides as well as different values of time strides. Specifically, a smaller right context to reduce the latency of TDNN when used in online decoding. Along with this, the study also experimented with sub-sampling in deeper layers wherein only a select few frames are used instead of the entire context. This further reduces the latency as well as reduces the training time required for the model. A baseline DNN equivalent is used to gauge the performance of the TDNN architecture. 

7 

###### **Acoustic Model Training Experiments** 

Since this study makes use of the same phoneme set for both Filipino and Bisaya, the authors experimented with using a Filipino acoustic model to test Bisaya speech and vice versa. This shows the viability of having a mixed acoustic model. 

###### **Evaluation** 

To evaluate the performances of the models, the standard word error rate (WER) is used. To analyze the models further, word confusion and phoneme confusion analysis are done to be able to see in which cases the models struggle. 

###### **Experiments** 

In this study, the authors experimented with the effects of the amount of data in relation to the performance by training on 25%, 50%, 75%, and 100% of the data. This is to give insight into how much training data would be needed for the models to converge. 

Since the prior project’s main objective was to create a chatbot for children, the author experimented with evaluating the best models for children’s speech. The children’s speech data is actual healthcare interviews between a nurse and a child. This is evaluated using phoneme error rate (PER) instead of WER since the training data’s vocabulary has little to no overlap with the vocabulary of the testing data 

In this study, the authors also experimented with cross-language acoustic models wherein Filipino acoustic models are evaluated on Bisaya speech and vice versa. This showed the viability of training in one language or dialect and using it in another phonetically similar language. 

Lastly, the author experimented with the weights of the language model from 1% to 25%. This displayed the factor of the language model in the performance of the ASR system as a whole. 

8 

## **Chapter 2** 

## **Review of Related Literature** 

This chapter presents a review of the previous works done in the field of ASR. The first section discusses what ASR is and the different parts of an ASR model. The second and third sections discuss previous works’ methods, results, and opportunities in the field of Filipino ASR and children’s ASR. Lastly, the fourth section discusses the types and designs of various datasets in ASR. 

### **2.1 Automated Speech Recognition** 

Automated Speech Recognition (ASR) is the task of converting raw human speech/audio into useful information such as text. This speech-to-text module can enable various systems such as personal digital assistants, voice search, speech-to-speech translation, and conversational bots. These are possible with the help of signal processing/feature extraction methods to convert raw audio to useful machinereadable information and features, acoustic models to interpret mentioned features to make a decision, and language models to aid in generating text that has semantic meaning rather than just meaningless utterances. A typical architecture of an ASR system is shown in Figure 2.1. Table 2.1 provides an overview of all the previous works that will be discussed in this section. 

9 



<!-- Start of picture text -->
audio signalg SignalFeaturei ProcessingExtractioni  & features Acoustic Model AM score Hypthesis Search result<br>Language Model LM score<br><!-- End of picture text -->

Since raw speech signals are continuous, signal processing generates a discrete sample. This discrete sample will further be processed using feature extraction methods to generate acoustic features. 

A signal processing technique that is often used by many studies is the Fourier transform which reveals notable features such as the frequency domain (Kunze et al., 2017; Salido et al., 2017). One of the notable feature extraction methods that integrate a type of Fourier Transform in its algorithm is the Mel Frequency Cepstrum Coefficient (MFCC). Multiple studies have used it because it can produce robust features that account for noise (Dimzon & Pascual, 2020; Briones et al., 2020; Yeung & Alwan, 2018; Liao et al., 2019; Bautista & Kim, 2014). This may reveal some useful information that would normally be difficult to extract by humans, especially with information that is high-dimensional such as audio. 

##### **2.1.2 Acoustic Models** 

Acoustic models use the previously mentioned acoustic vector features to establish statistical representations between these features and phonemes, letters, or words. One of the most prominent acoustic models that have shown success for different previous works is the use of Hidden Markov Models (HMM). This is due to HMM being a great mathematical tool for a wide range of applications, especially when applied properly on a pattern recognition problem (Rabiner, 1989). In conjunction with HMM, Gaussian Mixture Models (GMM) are used to establish a relationship between the HMM states and the acoustic features (Juang et al., 1986). A study by Swietojanski et al. (2013) showcased the use of HMM-GMM as a baseline for their study on combining hybrid and HMM-GMM systems on English TED talks corpus. Perceptual linear prediction (PLP) was used as well as multi-level adaptive networks (MLAN) as the feature extraction method. Speaker adaptive training (SAT) was also utilized to discriminatively train the models using the boosted maximum mutual information (BMMI). A publicly available English TED talk corpus was used. With this, the best performing model is MLAN+SAT+BMMI with a word error rate of 17.3%. 

Another more recent study by Nacem et al. (2020) uses a variation of the GMM called subspace GMM to recognize continuous Urdu speech. Aside from the ASR system, one other contribution of the study was a dataset of high-quality Urdu speech. As the acoustic feature, MFCC was used. The model was able to yield a minimum of 9% WER which has its merits considering Urdu is a low-resource language. 

Tan et al. (2021) also use HMM-GMM in conjunction with their proposed 

11 

CNN-transformer-based joint CTC-attention system to recognize accented English speech. Since there is limited data from Librispeech and accented English datasets, the study utilized data augmentation techniques such as noise simulation, SpecAugment (Park et al., 2019), speed perturbation, and text-to-speech. With MFCC as their feature extraction, the model was able to yield a minimum of 2.92% WER. 

Although HMM-GMM has been and is being used extensively for ASR, as well as with the rise in popularity of neural networks (NN), the number of research on hybrid ASR systems that use HMM and NN in conjunction with each other as well as purely NN-based ASR systems has also risen. One of the notable works in this field is by Amodei et al. (2016). The study built an end-to-end ASR system for English and Mandarin using Recurrent Neural Networks (RNN). To achieve this, the study also collected English and Mandarin speech corpora. Because the RNN-based approach is generic, the ASR system performed well for both English and Chinese in different circumstances, namely, noisy, clean, accented, and read speech. The ASR system consistently had a WER lower than human evaluators across all circumstances for Chinese speech. However, for English speakers, the RNN only matches when the speech is clean. In all other circumstances, human evaluators outperformed the ASR system. 

A team of researchers, Kunze et al. (2017), saw an opportunity to bypass some limitations of the work of Amodei et al. (2016). Specifically, transfer learning was utilized to be able to train ASR models with limited computing resources. A German speech corpus was used to test the approach of freezing _k_ layers of Wav2Letter and then training the rest of the layers on the German corpus. To evaluate the model, WER was used along with training time and GPU memory usage. Transfer learning was able to outperform a model that was trained from scratch with the same amount of time and with less GPU memory required. 

More recent studies have used Connectionist Temporal Classification (CTC) (Graves et al., 2006) as a way to label unsegmented sequences. Studies by Nakatani (2019) and Li et al. (2019) use CTC and have seen respective successes in both fields. Nakatani (2019) used it as a way to improve transformer-based ASR. The model was trained on a corpus of spontaneous Japanese speech and yielded a WER of 4.5%. Li et al. (2019) use it towards an ASR model that can handle code-switching. The model was trained on a corpus of utterances from Microsoft’s Cortana in Chinese which yielded a WER of 11.11% for monolingual speech and a WER of 55.38% for code-switching. 

A wide array of acoustic models tackle ASR with different approaches each with its advantages and disadvantages. These studies would be integral to this paper since the domain of this study is very specific; specific domains require 

12 

specific models. 

##### **2.1.3 Language Models** 

Language models aid in generating text that has semantic meaning. This is also especially useful in domain-specific problems where the task is known. For more general problems, n-grams can be sufficient for a language model wherein the model gives the probability of the combination of n number of words. Tong et al. (2017) utilize a bigram language model since not only is it domain-specific, but also the target languages were English and Mandarin. There are also more advanced language models that deal with this problem such as in the study of Tan et al. (2021) which used Recurrent Neural Network (RNN) in implementing the language model 

For domain-specific language models, Ang et al. (2011) use the CMU-Cambridge Statistical Language Modeling Toolkit (CMU SLM Toolkit) to generate a language model that is suitable for Filipino news. Since then, more recent studies such as the paper of (Lee et al., 2021) propose an adaptable multi-domain language model that is based on their adapter module paired with BERT and RNN. This opens opportunities for training a language model that is suitable for not only a Filipino or Bisaya language model but also one that is specifically for healthcare. Table 2.1 provides a summary of the studies that were discussed. 

### **2.2 Philippine Languages ASR** 

Numerous Filipino languages are being actively used by a variety of communities. However, the most used is Filipino which is also the national language of the Philippines. Thus, a lot of ASR research in the Philippines has been directed towards this language in particular. One of the most used corpora is the Filipino Speech Corpus (FSC) (Guevara et al., 2002). The creation of this corpus has inspired many researchers to explore this field. 

Bautista and Kim (2014) used FSC to develop an HMM-based ASR system for the Filipino language using the mentioned FSC. The lack of intelligent systems in Filipino motivated them to build an ASR model for Filipino speakers. The experiments include using different values for parameters and the model was able to reach an 11.3% WER. Another study that used FSC is Fadri (2017) which is an intelligent system in Filipino called PASABI, a speech-to-text messaging application that used RNN which yielded a 3.95 Character Error Rate (CER) 

13 

###### which indicates a fairly high misspelling rate. 

As mentioned, FSC is one of the most used corpora; however, it does not account for code-switching and loan words wherein speakers use other languages in the middle of conversations. This is especially common for Filipino speakers to switch between languages such as English or even Bisaya. This motivated Ang et al. (2014) to not only create a corpus of spontaneous speech with code-switching in English as well as isolated utterances but also created an HMM-based ASR system for this. The model garnered an 18.7% WER. 

Salido et al. (2017) wanted to recognize isolated digits in Filipinos; however, the approach is unique. Instead of treating it as an ASR task, image classification techniques were applied to the spectrogram. Usually, after a Fourier transform, the acoustic features are fed into an acoustic model; however, a pre-trained AlexNet Convolutional Neural Network (CNN) is used which is normally used for image classification. The study was successfully able to generate the Filipino isolated digit corpus and develop an accurate ASR system with a WER of 1.4%. Although this evaluation may be high, it is only on a vocabulary size of 10 and is a clean and isolated speech. 

One of the main challenges in the Philippine language ASR is low resources. Prasad et al. (2019) offered a way to build an ASR system for low-resource languages without any audio training data. Multiple corpora in different low-resource languages were generated. One of those languages is Cebuano. The study experimented with training a Filipino acoustic model of CTC-Segmentation and Minimum Bayes Risk (SMBR) and evaluating it on Cebuano data. This proved to be effective as the model yielded an 18.1% WER as well as improvements in other languages. This shows that phonetically similar languages can be used to develop a low-resource language. 

Liao et al. (2019) developed a Bikol and Kapampangan ASR system using an HMM-based model. The data that the model was trained on was a Bikol and Kapampangan isolated phrases that were collected by the study. The model achieved a 4.9% WER. The model was also evaluated by language experts by simply counting the number of word errors that the model makes. A summary of all the Philippine Language ASR works can be seen in Table 2.2 

### **2.3 Low Resource ASR** 

There have been two main methods of handling low-resource ASR. First is the use of transfer learning wherein the model is trained on a similar high-resource 

14 

Table 2.2: A summary of Philippine Language ASR studies. 

|**Author**|**Dataset**|**Methodology**|**Results**|
|---|---|---|---|
|Bautista<br>and<br>Kim (2014)|FSC|HMM-GMM ASR|WER 11.3%|
|Ang et al. (2014)|Filipino sponta-<br>neous speech &<br>isolated<br>utter-<br>ances|LDA, VTLN, HMM-<br>GMM|WER 18.7%|
|Fadri (2017)|FSC|RNN|CER 3.95|
|Salido<br>et<br>al.<br>(2017)|isolated Filipino<br>digits|Short-time<br>Fourier<br>Transform,<br>AlexNet<br>CNN image classifca-<br>tion|WER 1.4%|
|Prasad<br>et<br>al.<br>(2019)|Cebuano<br>&<br>other languages|CTC-SMBR,<br>Ce-<br>buano data→Filipino<br>AM|WER 18.1%|
|Liao et al. (2019)|Bikol<br>and<br>Ka-<br>pampangan<br>Speech|HMM-GMM|WER 4.9%|



language and then it is trained on the target low-resource language (Kermanshahi, Akbari, & Nasersharif, 2021). Studies such as Kunze et al. (2017) make use of this by applying a freezing parameter wherein the model is trained on a highresource language and then the first _n_ layers of the neural network are frozen while retraining it on a low-resource language. Tong et al. (2017) also demonstrates transfer learning; but instead of different languages, it is adult speech and children’s speech. The paper has two methods of transfer learning. The first is acoustic adaptation wherein the model is first trained on a large adult speech corpus. It is then retrained with children’s speech. The second is multi-task learning wherein adult speech and children’s speech are combined to train the model. A summary of the discussed studies is seen in Table 2.3 

15 

Table 2.3: A summary of transfer learning studies. 

|**Author**|**High Resource**|**Low Resource**|
|---|---|---|
|Kunze et al. (2017)|English|German|
|Tong et al. (2017)|Adult (English)|Children (English)|
|Kermanshahi<br>et<br>al.<br>(2021)|English|Persian|



The second one is to augment speech data. One of the methods is noise augmentation (Hannun et al., 2014; Seltzer, Yu, & Wang, 2013) wherein noise is added to the clean speech data. This makes the model more robust to noise. Another method is audio perturbation. One example is the vocal tract length perturbation (VTLP) (Jaitly & Hinton, 2013) wherein the signal is subjected to a random warping coefficient in the frequency axis. Generally, this warping coefficient is between 0.8 to 1.2. Another example is speed perturbation (Ko, Peddinti, Povey, & Khudanpur, 2015) wherein instead of warping in the frequency axis, the signal is warped in the time axis; this results in a change in the duration of the signal. Lastly, another method that could be used is the use of text-tospeech (TTS) (Du & Yu, 2020) wherein a model is given a text input, and it outputs synthesized speech. A summary of data augmentation studies is seen in Table 2.4 

Table 2.4: A summary of data augmentation studies. 

|Seltzer et al. (2013)|Noise Augmentation|
|---|---|
|Hannun et al. (2014)|Noise Augmentation|
|Jaitly and Hinton (2013)|Vocal Tract Length Pertur-<br>bation|
|Ko et al. (2015)|Speed Perturbation|
|Du and Yu (2020)|Text-to-Speech|



### **2.4 Children ASR** 

Children’s ASR has been split from the field of adult ASR since adult ASR models have a considerable performance drop when used on children. One factor is that children have a physical difference from adults which is the vocal tract. Usually, 

16 

children’s voices are much higher because of this and this is one of the features that is being used in adult ASR systems. Another reason is reading miscues, grammar errors, or vocabulary errors. ASR systems that use language models may find it difficult to take these into account. Thus, normalization techniques such as Vocal Tract Length Normalization (VTLN) and Subglottal Resonance Normalization (SRN) are used to take these into account. 

Yeung and Alwan (2018) explore both VTLN and SRN on the difficulties of ASR for kindergarten-aged children. The problem that children’s ASR is the variance between kindergarten-aged children and elementary-aged children is enough for some ASR systems to perform considerably worse. To combat this, a matched versus mismatched experiment was implemented on the OGI kids’ speech data in English. Wherein the training data would be matched or mismatched with the testing data. A hybrid HMM-DNN system was implemented which found that the mismatched performed better than matched when trained on 1st graders and tested on kindergarten-aged children. This may indicate that older-aged children may be better training data for kindergarten-aged children because of the mentioned reading miscue or vocabulary problem. 

With regard to resources, Tong et al. (2017) propose a transfer learning to combat the scarcity of data in children’s ASR. The study experimented with acoustic adaptation and multi-task learning with a DNN model on English and Mandarin corpora in both adults and children. Acoustic Adaptation takes a trained adult ASR system and uses parameter adaptation with children’s speech data. Multitask learning, on the other hand, trains the model from scratch with both adult and children’s speech data. The study found that multi-task learning outperforms acoustic adaptation; but, both approaches prove to increase performance in children’s ASR. 

On the Filipino side of children’s ASR, Briones et al. (2020) develop an ASR system for Filipino-speaking children. The study used an equivalent of the FSC but for children, Children’s FSC (CFSC) (Pascual & Guevara, 2012). An HMMbased ASR system was utilized which yielded a 42.10% WER. Dimzon and Pascual (2020) have the same motivations as Briones et al. (2020). This study utilized an HMM-based model as well as VTLN to normalize the vocal tract length. Although VTLN can improve performance in children’s speech, in this case, the study only saw a 2% decrease in WER. With this as well as fine-tuning the models, it yielded a 30.52% WER. 

Children’s ASR in conjunction with Philippine Language ASR has mainly explored the use of HMM-GMM models and mostly on the Filipino language. Also, most of the studies are focused on CFSC which is solely based on read speech. These can be seen in Table 2.2 and Table 2.5 This presents an interesting 

17 

opportunity to tackle the problem of conversational speech in both Filipino and Bisaya for a specific domain, healthcare, using a hybrid model HMM-DNN that may be able to increase the performance of the ASR system. 

Table 2.5: A summary of Children ASR studies. 

|**Author**|**Dataset**|**Methodology**|**Results**|
|---|---|---|---|
|Tong<br>et<br>al.<br>(2017)|English & Man-<br>darin Corpora|Acoustic<br>adaptation<br>& Multi-task learning|Both outperform<br>baseline|
|Yeung and Al-<br>wan (2018)|English<br>OGI<br>Kids’<br>Speech<br>Corpus|VLTN, SRN, HMM-<br>DNN, matched vs mis-<br>matched|Mismatched<br>outperforms<br>matched %|
|Dimzon<br>and<br>Pascual (2020)|CFSC|VTLN, HMM-GMM|WER 30.53%|
|Briones<br>et<br>al.<br>(2020)|CFSC|HMM-GMM|WER 42.1%|



### **2.5 Time Delay Neural Network** 

With the mentioned acoustic models, there are HMM-GMM-based ASR systems and end-to-end systems based purely on neural network approaches. Additionally, there is an approach called a hybrid model wherein the HMM is still used; however, the GMM module is replaced with a neural network (NN). The hybrid model is a discriminative model due to its NN module as compared to the GMM which is a generative model that only approximates. Since this study experimented with TDNN, the focus of this section will also be on related works on TDNN for both end-to-end and hybrid systems. 

Georgescu et al. (2019) explored the architectures TDNN, convolutional TDNN (CNN-TDNN), long-short-term memory TDNN (LSTM-TDNN), and LSTM-TDNN with attention. The standard MFCC was used as the feature extraction along with 100-dimensional i-vectors. The language model is a bigram language model trained on over 355 million words. The acoustic models were trained on the read speech corpus (RSC) and the spontaneous speech corpus (SSC) both of which were in Romanian. The RSC contains about 100 hours of speech while the SSC contains about 134 hours of speech. The best-performing acoustic models were 

18 

the TDNN with 2.79% WER and the CNN-TDNN with 16% WER for the RSC and SSC respectively. The WER for TDNN in the SSC is a respectable 16.63%. 

Peddinti et al. (2015) also explored the architecture of TDNN. However, the time strides or the contexts are the emphases of the study. An asymmetrical time stride means the left and the right contexts are unequal. A larger left context and a smaller right context were used to make the acoustic model suitable for online decoding. Sub-sampling is when only a select few frames of context are used instead of the whole context. This was also used to further reduce the latency, reduce the training time needed, and reduce the size of the model. As a baseline, the vanilla DNN was used to be able to compare it with the TDNN’s performance. The same feature extraction MFCC was used along with 100-dimensional i-vectors. The language model is a trigram language model trained on over 14 million words. The acoustic models were trained on the Switchboard corpus which is a conversational speech corpus with 300 hours of speech. The best-performing model was the TDNN with time strides [-2,2], _{_ -1,2 _}_ , _{_ -3,4 _}_ , _{_ -7,2 _}_ with a % WER. This is compared to the vanilla DNN with a network context of [-7,7] with a 15.1% WER. 

Kipyatkova (2017) experimented with both TDNN and a DNN on a Russian speech corpus. The same feature extraction MFCC was used along with 100dimensional i-vectors. The language model is a trigram language model trained on online Russian newspapers with over 350 million words. The acoustic models were trained on a Russian speech corpus of more than 30 hours of audio data. The best-performing model was achieved by a TDNN with 5 layers and a network context of [-8,8] with 19.04%. Liu et al. (2019) explored the architectures TDNN, TDNN with Recurrent Neural Network (RNN), Time Delay Recurrent Neural Network (TDRNN), and deep1-TDRNN. The same MFCC and 100-dimensional i-vectors were used. The language model is a trigram trained on 14 million words. The speech corpus is also the Switchboard with 300 hours. The best-performing models are the TDRNN with an 11.3% WER. Although, the pure TDNN is not far behind with a 12.1% WER. 

The study of Fathima, Patel, Mahima, and Iyengar (2018) presents the TDNNHMM architecture’s performance on a low-resource language as compared to a DNN-HMM model or an HMM-GMM model. The speech corpora used are composed of three Indian languages which are Tamil, Telugu, and Gujarati. The training data contains about 40 hours of speech data per language. The language model used is a trigram trained on the transcript of the corpora itself which contains about 150,000 words. With time strides [-1,2], _{_ -3,3 _}_ , _{_ -3,3 _}_ , _{_ -3,3 _}_ , _{_ - 6,0 _}_ , The TDNN consistently outperformed both the HMM-GMM models and 

19 

the DNN-HMM models. Another study by Diwan et al. (2021) also presents the TDNN-HMM architecture and compares it with HMM-GMM as well as a fully end-to-end transformer-based ASR system. The study makes use of low-resource Indian languages namely Hindi, Marathi, Odia, Tamil, Telugu, Gujarati, and Bengali. The corpora contain about 70 to 80 hours of speech data per language. The results, in this case, are unclear whether TDNN or an end-to-end system is better since both have roughly the same performances. A summary of all the mentioned previous works is seen in Table 2.6. 

Table 2.6: A summary of Time Delay Neural Network studies. 

|**Author**|**Dataset**|**Architecture**|**Results**<br>**(WER)**|
|---|---|---|---|
|Georgescu<br>et<br>al.<br>(2019)|RSC (100 hours) and<br>SSC (134 hours)|CNN-TDNN|16.63%|
|Peddinti et al. (2015)|Switchboard<br>corpus<br>(300 hours)|TDNN|14%|
|Kipyatkova (2017)|Russian Speech Cor-<br>pus (30 hours)|TDNN|19.04%|
|Liu et al. (2019)|Switchboard<br>corpus<br>(300 hours)|TDRNN|11.3%|
|Fathima et al. (2018)|Indian<br>Languages<br>(120 hours)|TDNN|12.7%|
|(Diwan et al., 2021)|Indian<br>Languages<br>( 600 hours)|TDNN|29.03%|



The TDNN is a powerful tool for acoustic models. Although none of the mentioned studies focused on the Philippine languages, the results show a competitive WER for conversational speech. Current progress on Filipino speech corpora may not yet be sufficient to train the complex models mentioned above. However, comparing the performance of a pure TDNN to these complex models, the pure TDNN still offers a competitive WER. 

20 

## **Chapter 3** 

## **Theoretical Framework** 

This chapter discusses the theoretical framework of the study. The first section discusses the Filipino and Bisaya languages as well as the phonemes used in this study. The next section discusses the feature extraction algorithms and the model enhancement techniques used. The last section discusses the acoustic models used. Specifically, the HMM-GMM model and the TDNN-HMM model. 

### **3.1 Filipino and Bisaya** 

More than 120 languages are being actively used in the Philippines. All of these are considered to be part of the Austronesian family of languages. In the 1987 constitution of the Philippines, the Tagalog language is designated as the national language of the Philippines. Thus, this Tagalog is also referred to as Filipino. Moreover, this is the most used language in the Philippines wherein the speakers are mainly from the Luzon region. The second most used language in the Philippines is Bisaya wherein Cebuano is the main dialect. As opposed to Filipino, Bisaya is mainly used by speakers from the Visayas region. The Spanish language substantially influences both languages. As a result, many of the words are of Spanish origin. Both languages are ergative-absolutive. This means that they treat the subject of an intransitive verb like the object of a transitive verb. An example of this property is the Filipino sentence “Umiinom **ako** ng maraming tubig” or the Bisaya sentence “Moinom **kog** daghang tubig” both meaning “I drink a lot of water” in English. A more detailed diagram is seen in Figure 3.1 These sentences also demonstrate that both are verb-initial languages wherein the verbs “umiinom” (drinking) and “moinom” (drink) usually come first in a sentence rather than the subject. Both languages also make use of prefixes, suffixes, 

21 



<!-- Start of picture text -->
Verb Subject Preposition Adjective Object<br>_____ i<br>* - *s a<br>a ee Mie ne<br>— ne,<br><!-- End of picture text -->

the performance of the models. All monophones used in the phoneme sets are a subset of the IPA. Minor symbol changes were only made to make the transcription process easier and more readable. These changes are seen in Table 3.3. These phoneme sets would suffice in transcribing Filipino speech in this study. These phoneme sets would also suffice since the phonemes used for the Bisaya language are similar if not the same as Tagalog (Malaay, Simora, Cabatic, Oco, & Roxas, 2017). There have also been instances where the use of a Tagalog acoustic model is used to test Bisaya speech data since both are part of the same language family and phonetically similar (Prasad et al., 2019). 

Some notable phonemes are /f/, /v/, /s/, /z/, and /th/ which are exclusively used when the speaker code switches to English words. Some examples are the words “fever”, “reliever”, “pedzinc” and “menthol” respectively. The phonemes /sh/ and /ch/, although not usually spelled out in Filipino or Bisaya words, are usually pronounced in words with ”sy/siy” and “ts” respectively. An example of these is the words “siya” (him/her) and “petsa” (date) which are transcribed as /sh a/ and /p e t ch a/ respectively. 

Table 3.1: Simplified International Phonetic Alphabet 

|**Phone Class**|**Phones**|
|---|---|
|Stop|/p/, /b/, /t/, /d/, /k/, /g/, /ú/,<br>/ã/, /c/, /é/, /q/, /å/, /P/|
|Nasal|/m/, /M/, /n/, /6/, /ñ/, /N/, /ð/|
|Fricative|/F/, /B/, /f/, /v/, /T/, /D/, /s/,<br>/z/, /S/, /Z/, /ù/, /ü/, /ç/, /J/,<br>/x/, /G/, /X/, /K/, /è/, /Q/, /h/,<br>/H/|
|Africate|/Ð/, /ì/|
|Trill|/à/, /r/, /ö/|
|Tap or Flap|/v#/, /R/, /ó/|
|Approximant|/V/, /ô/, /õ/, /j/, /î/, /l/, /í/,<br>/L/, /Ï/|
|Vowel|/i/, /ı/, /e/, /E/, /æ/, /a/, /@/,<br>/A/, /6/, /O/, /2/, /o/, /U/, /u/,<br>/y/, /Y/, /ø/, /œ/, /5/, /3/, /Æ/,<br>/9/, /8/, /0/, /1/, /7/, /W/|



23 

Table 3.2: Phonemes for PS27 and PS35 

|**Phone Class**|**Phones**|
|---|---|
|Stop|/p/, /b/, /t/, /d/, /k/, /g/|
|Fricative|/f/, /v/, /s/, /z/, /sh/, /th/,<br>_/h/_<sup>1</sup>|
|Africate|/j/, /ch/|
|Nasal|/m/, /n/, /ng/|
|Lateral Liquid|/l/|
|Retrofex Liquid|/r/|
|Glide|/w/, /y/|
|Vowel|/a/, /e/, /i/, /o/, /u/|
|**Diphones**<sup>2</sup>|**/ha/, /he/, /hi/, /ho/, /hu/,**<br>**/at/, /aw/, /ay/, /oy/**|



> 1 The phone /h/ is used exclusively for PS27 

> 2 All diphones are used exclusively for PS35 

Table 3.3: Mapping of PS27/PS35 Phonemes to its IPA Equivalent 

|**PS27/PS35**|**IPA**|**Equiva-**|
|---|---|---|
|**Phoneme**|**lent**||
|/sh/|/S/||
|/th/|/T/||
|/j/|/Ð/||
|/ch/|/ì/||
|/ng/|/N/||



24 

### **3.3 Feature Extraction and Model Enhancement Techniques** 

##### **3.3.1 Mel Frequency Cepstral Coefficients** 

The Mel Frequency Cepstrum Coefficient (MFCC) is a feature extraction technique that has been widely used in the ASR field Hasan, Jamil, Rahman, et al. (2004) due to its ability to convert continuous speech waveforms into frequency and energy bands that are similar to what a human would hear or interpret them as. However, the MFCC is sensitive to noise. First, it goes through a pre-emphasis module which increases the energy in the high frequencies. This ensures that the magnitude of both low and high frequencies is normalized. This is especially important for the recognition of high-frequency low-energy phonemes such as unvoiced fricatives. Next, windowing is applied to the waveform wherein it is spliced using a sliding window. This is usually done with a 25ms window with a 10ms frameshift. When splicing the waveforms, the drop-off in amplitude may cause noise in the high frequencies. To address this problem, algorithms such as the Hamming and Hanning windows are introduced to taper off the amplitudes at the beginning and the end. Once this is done, a Discrete Fourier Transform (DFT) is applied to convert the waveform from the time domain to the frequency domain. This is seen in Equation 3.1 wherein _x_ (0) to _x_ ( _N_ ) are the original signals and are being converted to the frequency domain _X_ (0) to _X_ ( _N_ ) by multiplying _−i_ <u>2</u> _<u>πnk</u>_ the original signal _x_ ( _n_ ) by the term _e N_ . Since humans perceive magnitude and frequency at a logarithmic scale instead of a linear scale, the Mel scale and triangular filter banks are applied. These can be seen in Equation 3.2 wherein _f_ is the frequency. Lastly, the spectrum of the spectrum or, in short, the cepstrum is acquired through the Discrete Cosine Transform (DCT). Since most of the important features are in the first several coefficients, the higher-order coefficients are discarded. Typically, 13 cepstral coefficients are used. Lastly, the dynamic MFCC features are computed. These are also known as the delta coefficients and the delta-delta coefficients. The 13 delta coefficients or the first-order derivatives contain information about the speech rate. The 13 delta-delta coefficients or the second-order derivatives contain information about the acceleration of speech. Thus, this makes up the 39 MFCC coefficients per window frame. 



25 



##### **3.3.2 Cepstral Mean and Variance Normalization** 

The Cepstral Mean and Variance Normalization (CMVN) is a feature normalization technique. It simply does a normalization using the mean divided by the variance as seen in Equation 3.3. Wherein _xt_ ( _i_ ) is the _i_ th index in the feature vector at time _t_ and _xt_ ˆ ( _i_ ) represents its normalized values. The symbol _µ_ represents the mean and _σ_ is its standard deviation which is computed as Equation 3.4 and Equation 3.5 respectively. Since MFCC performs particularly worse when used in noisy environments, the CMVN is used to counteract this (Viikki & Laurila, 1998). 







##### **3.3.3 Vocal Tract Length Normalization** 

Vocal Tract Length Normalization (VTLN) is also a feature normalization technique much like CMVN. It aims to which aims to compensate for the effects of physical differences in vocal tract length. Since children from various age ranges may be in different stages of development in terms of their speech organs, the VTLN may mitigate the effects of these differences in speech organs. Moreover, the use of adult speech for an ASR for children may massively hurt the performance of the model without VTLN. A simple linear VTLN as seen in Equation 3.6 wherein _k_ is the warping factor and _s_ denotes the speaker (Cohen, Kamm, & Andreou, 1995). For each speaker s, there is a warping factor k that is multiplied by frequency f to get the normalized frequency f’. A non-linear option for VTLN is also available as seen in Equation 3.7 wherein it allows more stretching at high frequencies than at low (Eide & Gish, 1996). Typically, the warping factor is set 

26 

to 0.8 to 1.2 (Povey et al., 2011). With regards to Filipino-speaking children, the VTLN has only slight improvements in the performances of models. 





##### **3.3.4 Linear Discriminant Analysis** 

Linear Discriminant Analysis (LDA) is a dimensionality reduction method that aims to maximize the separation among the categories in the data (Saon, Padmanabhan, Gopinath, & Chen, 2000). This is done by getting the _d_ -dimensional mean vectors _µd_ and covariance vectors _σ_<sup>2</sup> _d_<sup>.Fromthis,Equation3.8canbede-</sup> rived wherein _Sw_ is the within-class scatter and _Sb_ is the between-class scatter. It aims to ideally reduce _Sb_ and increase _Sw_ . Next, the generalized eigenvalue is solved from the matrix _Sw_<sup>_TSb_wherein</sup><sup>_T_isthetransposeofthematrix.Next,the</sup> _k_ eigenvectors with the largest eigenvalues are chosen. A larger eigenvalue means it is more informative. From these _k_ eigenvectors, a _d × k_ -dimensional eigenvector matrix _W_ . Lastly, the samples are transformed onto a new subspace based on the chosen eigenvalues. Equation 3.10 explains the transformation wherein _X_ is the _d × k_ -dimensional matrix representing the original _n_ samples and _Y_ is the final transformed matrix in the new subspace. 







##### **3.3.5 Speaker Adaptive Training** 

The Speaker Adaptive Training (SAT) method aims to create a speaker-independent model. Anastasakos, McDonough, Schwartz, and Makhoul (1996) as Equation 

27 

3.11 wherein it is considered that there are _S_ speakers and each speaker _s_ has a sequence of observations _O_<sup>_s_</sup> = ( _o_<sup>_s_</sup> 1<sup>_, os_</sup> 2<sup>_, . . . , os_</sup> _T_<sup>_r_)where</sup><sup>_Ts_isthelengthofobserva-</sup> tions for that speaker. The compact HMM _λc_ , which has fewer overlaps between speakers, is mapped by the transformation _Gs_ for each speaker _s_ . The term _G_ is modeled through the use of the Maximum Likelihood Linear Regression method which produces a linear transform that maximizes the likelihood of the adaption data. Both the _λc_ and _Gs_ are optimized to maximize the likelihood of the training data. The emphasis of SAT is put on _G_ since this term provides the variability to discriminate between speaker characteristics and recording conditions. Thus, this allows the acoustic models to be speaker-independent. 



### **3.4 Language Model** 

The language model is widely used in different domains. In ASR, n-grams are typically sufficient. It is based on _p_ ( _w|c_ ) wherein _w_ is the word and _c_ is the context. To calculate the probability of seeing a specific _n_ -gram, we take the number of occurrences of the specific _n_ -gram and divide it by the number of occurrences of the specific ( _n −_ 1)-gram. For example, the probability of a specific bigram can be calculated as in Equation 3.12. 



Calculation of the probability gives a value between 0 to 1 pertaining to the probability of the specific occurrence of the n-gram. To compute the probability of a sentence using an n-gram, the probabilities are simply chained and multiplied together. For example, _p( <s>my favorite dessert is ice cream </s>)_ where _<_ s _>_ and _<_ /s _>_ are the start and end of the sentence respectively. This is computed as _p_ 1( _my|<s>_ ) _· p_ 2( _favorite|my_ ) _· . . . · pm_ ( _</s>|x_ ) where _m_ is the number of _n_ -grams in the sentence. For longer sentences, these probabilities tend to be very small. To prevent an underflow, calculation in log probabilities is used. For the previous example, the computation becomes _log_ ( _p_ ) = _log_ ( _p_ 1) + _log_ ( _p_ 2) + _. . ._ + _log_ ( _pm_ ). To get back the probability we just get the exponential _e_<sup>_log_(</sup><sup>_p_)</sup> . Another problem arises when unseen instances are presented to the model. Thus, techniques to generalize a language model trained on a specific domain are applied. One way to combat zero probabilities is by replacing unknown words with _<_ UNK _>_ . Another technique is smoothing wherein we simply add a value to the count of unigrams to artificially increase the probability. 

28 

Lastly, the backoff and interpolation make use of unigram to n-gram. The backoff technique simply just “backs off” to the ( _n −_ 1)-gram if the specific n-gram is not sufficient. Interpolation is to sum over all the weight unigram to _n_ -gram. 

### **3.5 Hidden Markov Model** 

In early applications of speech recognition, the Hidden Markov Model (HMM) has been widely used (Swietojanski et al., 2013; Tan et al., 2021) due to its effectiveness in modeling a sequence of events and observations. Since speech recognition deals with a series of features and observations, the HMM is suitable for ASR systems. The HMM is based on the Markov Chain which models the probability of going from one state to another. The HMM has an additional observation per state. The three main algorithms that the HMM utilizes are the forward-backward algorithm, the Viterbi algorithm, and the Baum-Welch algorithm. The forwardbackward algorithm is the likelihood computation. Given an HMM _λ_ = ( _A, B_ ) and an observation sequence _O_ , determine the likelihood _P_ ( _O|λ_ ). The transition probability matrix is defined as _A_ = _a_ 11 _, a_ 12 _, . . . , ann_ wherein _aij_ represents the probability of moving form state _i_ to _j_ . The emission probabilities are defined as _B_ = _bi_ ( _ot_ ) wherein it expresses the probability of _ot_ being generated from state _i_ . The naive way of computing the likelihood of a sequence of observations is to brute force every single possibility which will take _O_ ( _N_<sup>_T_</sup> ) where _N_ is the hidden states and _T_ is the number of observations. Instead, the forward and backward algorithm makes use of dynamic programming that reuses previously computed probabilities to optimize the computations. These optimizations cut the time complexity down to _O_ ( _N_<sup>2</sup> _T_ ). The computations are found in Equations 3.13 and 3.14 where _αt_ ( _j_ ) represents the probability of being in state _j_ after seeing the first _t_ observations and _βt_ ( _j_ ) represents the probability of being in state _j_ before seeing the last _t_ observations (Rabiner, 1989). 





The Viterbi algorithm is the decoding algorithm. Given an HMM _λ_ = ( _A, B_ ) and an observation sequence _O_ = _o_ 1 _, o_ 2 _, . . . , oT_ , find the most probable sequence of states _Q_ = _q_ 1 _, q_ 2 _, ..., qT_ . The Viterbi algorithm is similar to the forward algorithm, 

29 

but instead of summing, the maximum is taken as seen in Equation 3.15 where _vt_ ( _j_ ) is the maximum probability of state _j_ occurring at time _t_ (Rabiner, 1989). 



Lastly, the Baum-Welch algorithm is the learning algorithm. It is an iterative process of the Expectation-Maximization principle. Given an observation sequence _O_ = _o_ 1 _, o_ 2 _, . . . , oT_ , and set of possible states _Q_ = _q_ 1 _, q_ 2 _, ..., qT_ , learn the HMM _λ_ parameters _A_ and _B_ . The Baum-Welch makes use of the forwardbackward algorithm. Along with this, it also makes use of _ξt_ ( _i, j_ ) where it is the probability of being in state _i_ in time _t_ , and state _j_ in time _t_ + 1 as well as _γt_ ( _i_ ) where it is the probability of being in state _i_ in time _t_ . To simplify these functions, the sum of _ξt_ ( _i, j_ ) from _t_ = 1 to _T −_ 1 is the expected number of transitions from state _i_ to state _j_ , and the sum of _γt_ ( _i_ ) from _t_ = 1 to _T −_ 1 is the expected number of transitions from state _i_ . To compute for the estimated model _λ_ = ( _A, B, π_ ), the estimated initial state distribution _πi_ is set to _γ_ 1( _i_ ), _aij_ is set to the expected number of transitions from _i_ to _j_ over the expected number of transitions from _i_ , and _bj_ ( _vk_ ) expected number of times in state _j_ and observing symbol _vk_ over the expected number of times in state _j_ . Now that the estimated model is complete, the process will repeat and generate a new model. This iterates several times or until a convergence condition is met (Rabiner, 1989). 

### **3.6 Time Delay Neural Network** 

As opposed to the generative model GMM, the Time Delay Neural Network (TDNN) is a discriminative model that serves the same purpose as the GMM when used in a hybrid HMM-TDNN system. The TDNN also takes into account temporal context using a hierarchical architecture. This is done by a 1-dimensional convolution to include left and right contexts also known as a time stride. This is done for each layer. This makes it so that the first few layers take in less temporal context and the deeper layers take into account wider temporal context and learn high-level features. A general TDNN is shown in Figure 3.2 wherein there are _n_ layers and each layer has a symmetrical time stride ∆ _n_ . Symmetrical time strides mean that the left and right contexts are of equal length. An asymmetrical time stride is where the left and right contexts are unequal. One advantage of an asymmetrical time stride architecture is that when the right context is relatively small and the left context is relatively large, this makes it suitable for online decoding without sacrificing performance (Peddinti et al., 2015). This is because it still considers a large enough context to recognize the features as well as needs less 

30 



<!-- Start of picture text -->
Feature 1st 2nd<br>Vectors cee Mutou<br>Layer Layer Layer ulpu<br>*<br>2* Ye) ft) (4)<br>Piyys *-H<br>*-<br>*<br>=<br>/ OY) OO ©0<br>::<br>* .<br>[J] O Oo ©<br>[JQ :.<br>LIQ -*<br>Lj.<br>*<br>*<br>*<br>*<br>*<br><!-- End of picture text -->

et al., 2011). As opposed to the 25 ms window frame of MFCC, the i-vectors are usually larger than 1 second. 





32 

## **Chapter 4** 

## **Research Methodology** 

This chapter presents the methodology of this study. The first section discusses the existing speech corpus and its characteristics. The second section discusses the data collection and data preparation processes such as audio recording, segmentation and preprocessing, and speech transcription. The third section discusses the exploratory data analysis. The fourth section discusses the ASR models and the experiments that were done. Lastly, the fifth section discusses the evaluation methods to gauge the performance of the models. 

### **4.1 Speech Corpus** 

The speech corpus that is used, as mentioned, is from the DLSU healthcare chatbot project (Luci-Atienza, 2021). Due to the availability of children’s speech and its ethical considerations, female voice actresses’ speech was used to train the models instead of children’s speech. Since the frequency of children’s voices is, on average, between 250-400 Hz, a suitable alternative for this is the adult female voice which is usually around 200 Hz. This is instead of the male adult voice of 150 Hz (Pedersen, Agersted, & Jønsson, 2015). The speech corpus is composed of 9 speakers with 9.03 hours of segmented speech for Filipino and 7 speakers with 8.97 hours for Bisaya. The speech recordings are stored in a WAV file format with a 16 kHz sampling rate. The recordings are responses to the questions regarding general physical wellness assessment in Table 4.1. 

Along with the mentioned speech corpus, the study used a subset of the Filipino Speech Corpus (FSC) (Guevara et al., 2002) for solely training Filipino models. The subset used is composed of only the isolated words. Similarly to the 

33 

mentioned DLSU healthcare speech corpus, only adult females were included. The subset of the speech corpus used is composed of 10 speakers totaling 2.78 hours of audio. In addition to this, the study collected 4 additional Filipino speakers with 4.49 hours of audio. Although there is little overlap in vocabulary with the chatbot speech corpus, this could help the models train on a more diverse dataset and perform better on the phoneme level. 

Table 4.1: General physical wellness assessment 

|**Category**|**Information**|
|---|---|
|**Chief Complaint**|Fever, Cough, Colds, Pain, Nau-<br>sea|
|**Review of Past Medical His-**<br>**tory**|Past Surgeries, Hospitalizations,<br>Familial History|
|**Medications**||
|**Instrumental**<br>**Activities**<br>**of**<br>**Daily Living Scale**|Feeding,<br>Grooming,<br>Toileting,<br>Dressing,<br>General<br>Hygiene,<br>Transferring, Playtime, Sleep|
|**Review of Systems**|General Appearance,<br>Allergies,<br>Skin, Neuro, Ears, Eyes, Nose,<br>Mouth and Throat, Heart, and<br>Lungs,<br>Gastrointestinal,<br>Geni-<br>tourinary, Multiple Sclerosis, En-<br>docrine|



### **4.2 Data Collection and Data Preparation** 

The data collection process supplements the speech data already collected. Filipino female adult speech was collected since, as mentioned, it is the closest to children’s speech in terms of frequency. The contents of the transcript of the additional data are the same as in Table 4.1. The following sub-sections also discuss the audio recording process, segmentation and preprocessing, and speech transcription. These processes are very similar to the ones used in the healthcare chatbot project. The transcript is also the same as the healthcare chatbot speech corpus. 

34 

##### **4.2.1 Audio Recording** 

The audio recording is facilitated through a custom website made for audio recording. The participant is given a consent form to sign before they are allowed to access the website. Once the participant has signed the consent form, a link is given to the participant. The website’s homepage introduces the overview of the project and the general objectives of the study. The website also contains a tutorial on how to navigate and use the audio recorder. The tutorial also reminds the participants of best practices such as recording in an environment free of background noises such as cars passing, animal noises, and other people talking. Each participant was given a unique key to access the audio recording page on the website. The recording page is composed of the controls and the prompt information. The controls include the start and stop recording, playback controls, and upload audio. The prompt information includes the prompt for what the participant has to record as well as the progress counter which tells them how many prompts are left. The audio recorder automatically converts the audio into a WAV file with a 16 kHz sampling rate. All the audio files are uploaded to a cloud database. 

##### **4.2.2 Preprocessing** 

Each audio file was either preprocessed or screened out of the final corpus. Minor noises were reduced or removed via light noise reduction but noises such as dog barks and passing cars may be harder to remove; thus, the recordings are discarded since they may reduce the performance of the speech recognition models. Speed perturbation was used for data augmentation. A speed factor of 1.1 to 1.25 is randomly applied to each audio file. The speed-perturbed file serves as additional training data for both Bisaya and Filipino acoustic models. 

##### **4.2.3 Speech Transcription** 

The speech corpus was transcribed at both the phoneme level and the word level. For word-level transcription, the transcriptions are lowercase alphanumeric characters. This means that the transcriptions are solely composed of both letters and numbers; no special characters such as punctuation marks are transcribed. However, the only time a number is transcribed in its numerical form is when it is a medical term such as /covid 19/. In any other instance, numbers are spelled out in letters. Also, medical-related acronyms are transcribed as a single word and not as individually separate letters. For example, UTI, which stands for urinary tract infection, is transcribed as one word /uti/. English code-switching 

35 

instances, where each word appears in formal English or Filipino dictionary, were transcribed as is. It is however commonly observed that children speakers informally combine English words with Filipino prefixes and suffixes. One example is the word /nagtotoothbrush/, where the English root word is /toothbrush/, and where adding the prefix /nagto/ transforms the English noun into a verb in the present continuous tense. In these instances, and especially when a Filipino prefix or suffix was observed to occur more than once in the speech corpus, the Filipino prefixes or suffixes were transcribed separately from the English word. For example, the word /nagtotoothbrush/ is transcribed as two separate words /nagto/ and /nagtotoothbrush/. 

For phoneme-level transcription, there are two phoneme sets used in transcribing the audio recordings: 1) Phoneme Set 27 (PS27) which contains 27 monophones, and 2) Phoneme Set 35 (PS35) which contains 26 monophones and 9 diphones. Table 4.2 shows the 27 monophones and the 9 diphones that were considered for the two Filipino phoneme sets PS27 and PS35. The phoneme level transcription process using PS27 is straightforward because the phoneme set has no overlaps or redundancies. In the transcription process using PS35 however, the diphones supersede the equivalent monophone pairs. The Filipino word /lagnat/ (fever) and the Bisaya word /hilanat/ (fever) for example are transcribed using PS35 as /l a g n at/ and /h i l a n at/ respectively, while the same word is transcribed as /l a g n a t/ and /h i l a n at/ using PS27. Note however that the same word can be transcribed as /l a g n a t/ and /h i l a n a t/ using PS35, thus introducing a redundancy that transcribers need to avoid. It is also worth noting that PS35 is similar to the phoneme sets used in the papers of (Pascual & Guevara, 2012; Briones et al., 2020; Pascual & Guevara, 2017; Dimzon & Pascual, 2020). The only notable difference is the removal of the phoneme /q/, a glottal stop, due to its low phoneme recognition rate (Briones et al., 2020). Although the Bisaya language has similar phonemes to Filipino, these phoneme sets may not be suitable for the Bisaya language. However, using these baseline phoneme sets, this study explored the best phoneme set for the Bisaya language through phoneme data analysis and phoneme matrix analysis. 

### **4.3 Data Analysis** 

Given there are two languages in the speech corpus, this study compared the two languages in terms of the frequency of each phoneme. Although Filipino and Bisaya may be phonetically similar, this does not necessarily mean that the distribution of phonemes is also similar. This may give insight into the comparison of the performance of the models on each phoneme and the actual phoneme 

36 

Table 4.2: Filipino Phonemes for PS27 and PS35 

|**Phone Class**|**Phones**|
|---|---|
|Stop|/p/, /b/, /t/, /d/, /k/, /g/|
|Fricative|/f/, /v/, /s/, /z/, /sh/, /th/,<br>_/h/_<sup>1</sup>|
|Africate|/j/, /ch/|
|Nasal|/m/, /n/, /ng/|
|Lateral Liquid|/l/|
|Retrofex Liquid|/r/|
|Glide|/w/, /y/|
|Vowel|/a/, /e/, /i/, /o/, /u/|
|**Diphones**<sup>2</sup>|**/ha/, /he/, /hi/, /ho/, /hu/,**<br>**/at/, /aw/, /ay/, /oy/**|



- 1 The phone /h/ is used exclusively for PS27 

- 2 All diphones are used exclusively for PS35 

distribution. 

### **4.4 ASR Models and Experiments** 

The Kaldi ASR toolkit was used for all the speech recognition models (Povey et al., 2011). Baseline HMM-GMM models were developed as a benchmark for further experiments. Although simple, these models have performed decent and may sometimes be sufficient for certain domains. The MFCC (Hasan et al., 2004) was utilized for feature extraction since it is one of the most robust features in ASR. Kaldi’s default 10ms frameshift and 25ms window size was implemented. To normalize the features CMVN was used. The corpus is split into about 8020 for training and testing. It is split according to speakers so that the models are tested on unseen speaker voices or voice qualities. These test speakers are chosen randomly once for Filipino and Bisaya and it is uniform for all models. For Filipino, FSC is excluded from the test set. 

##### **4.4.1 Phoneme Set and HMM States** 

The authors developed ASR models for both PS27 and PS35. This explored which phoneme set is suitable for each language. This study also experimented with 3-, 

37 

4-, and 5-state HMMs with monophone and triphone training. 

##### **4.4.2 Language Model** 

The _n_ -gram models were trained on the transcriptions themselves since publicly available general domain n-grams may not be suitable for a specific domain such as healthcare. This study experimented with 2-gram and 3-gram. The authors also experimented with adjusting the weight of the language model from 1% to 25%. This is sufficient to observe the effect of the language models as well as to not overpower the acoustic model when decoding. 

##### **4.4.3 Model Enhancement Experiments** 

The authors experimented with model enhancement techniques such as vocal tract length normalization (VTLN), Linear Discriminant Analysis (LDA) with Maximum Likelihood Linear Transform (MLLT), and Speaker Adaptive Training (SAT) on the baseline HMM-GMM models. The following combinations of model enhancement techniques were used: LDA+MLLT, SAT, VTLN, VTLN+LDA+MLLT, and VTLN+SAT. 

##### **4.4.4 Neural Network Approaches** 

After training multiple HMM-GMM models with various configurations, the best HMM-GMM model is then selected and a neural network is trained on the same acoustic features as the HMM-GMM model. After the neural network is trained, the GMM component of the HMM-GMM is replaced with the neural network. Instead of the generative nature of the GMM wherein it models the probability distribution of the phonemes, the neural network has a discriminative nature wherein it takes in acoustic features and generates the probabilities of each phoneme. This study used a time delay neural network (TDNN) architecture for the neural network component. The TDNN’s ability to model time series data makes it effective for speech recognition tasks. The preliminary experiment showed a 0.97% WER on the FCSC using a TDNN-HMM architecture (Ing, Pascual, & Dimzon, 2022). This TDNN model is from Kaldi’s premade nnet3 recipe. It is a TDNN with six layers with ReLU activation with 512 nodes per layer. This totals about 5 million parameters. The time strides are all symmetrical; the number of left contexts and right contexts is the same. The input layer splices together 

38 

2-time strides. For the next two layers, the time stride is one. The next two layers have time strides of three. The last layer has a time stride of six. This is designed to gradually widen the context the deeper it goes into the TDNN. This can be written in shorthand as the configuration [-2,2], [-1,1], [-1,1], [-3,3], [-3,3], [-6, 6]. This study also used this architecture. Furthermore, since the previous study only presents symmetrical time strides, this study also experimented with asymmetrical time strides as well as different values of time strides. As mentioned, a larger left context and a smaller right context reduce the latency of the TDNN when utilized in online decoding. Thus, the configuration [-2,2], [-1,2], [-3,3], [- 7,2] was used. This configuration has 4 layers with 512 nodes per layer and ReLU activation. This totals about 4 million parameters. Along with asymmetrical time strides, this study also experimented with sub-sampling in the deeper layers wherein instead of using the context from _t−n_ to _t_ + _n_ , it is spliced into a select few frames in the range of _t−n_ to _t_ + _n_ . Thus, the configuration [-2,2], _{_ -1,2 _}_ , _{_ -3,3 _}_ , _{_ - 7,2 _}_ was used. Similar to asymmetrical, this has 4 layers with 512 nodes per layer with ReLU activation. This configuration has about 3.3 million parameters. This is done to prevent redundant overlaps between the input context as it goes deeper. All TDNN models use iVectors and volume perturbation as additional features. To also gauge the TDNN architecture, a baseline DNN with network context [-7,7] was used with 4 hidden layers and 512 nodes per layer. This configuration has about 3.1 million parameters. All neural network models are trained for 5 epochs with an initial learning rate of 0.01 and a final learning rate of 0.001. Table 4.3 presents an overview of the configurations of all the neural network approaches discussed. 

Table 4.3: An overview of the neural network approaches 

||**Network**<br>**Context**|**Time**<br>**Strides**|**Layers**<br>**and**<br>**Nodes**|**Model**<br>**Pa-**<br>**rameters**|
|---|---|---|---|---|
|**DNN**<br>**baseline**|[-7, 7]|N/A|3 layers<br>512 nodes|_∼_3.1 million|
|**TDNN**<br>**symmet-**<br>**ric**|[-16,16]|[-2,2],<br>[-1,1],<br>[-1,1],<br>[-3,3],<br>[-3,3], [-6, 6]|6 layers<br>512 nodes|_∼_4.9 million|
|**TDNN**<br>**asym-**<br>**metric**|[-13,9]|[-2,2],<br>[-1,2],<br>[-3,3], [-7,2]|4 layers<br>512 nodes|_∼_4 million|
|**TDNN**<br>**subsam-**<br>**pled**|[-13,9]|[-2,2], _{_-1,2_}_,<br>_{_-3,3_}_,_{_-7,2_}_|4 layers<br>512 nodes|_∼_3.3 million|



39 

##### **4.4.5 Effects of Additional Data** 

Another experiment this study conducted is the size of the dataset that the TDNN is trained on. Specifically, this study gauged the effect of the additional data collected on the performance of the neural network approaches. This is to gauge whether the additional data collected is beneficial or whether the original dataset is already optimal for training the TDNN models. To further inspect the relationship between the amount of data and the performance, the study experimented with training on 25%, 50%, 75%, and 100% of the data. This trend gave an insight into how much data is needed to train a model to convergence. 

##### **4.4.6 Cross-Language Acoustic Model Experiment** 

Since this study makes use of the same phoneme set for both Filipino and Bisaya, this theoretically allows for a Filipino acoustic model to be utilized on Bisaya speech and vice versa. Thus, this study experimented with training acoustic models in Filipino and using them on Bisaya speech. This showed the viability of having a mixed acoustic model. 

### **4.5 Evaluation** 

To evaluate the performances of the models, the standard word error rate (WER) was used. Equation 4.1 defines how WER was computed where I is the number of insertions, D is the number of deletions, S is the number of substitutions, and N is the number of total words. To illustrate this, the ground truth sentence is “hindi ko alam, ” meaning “I do not know” in English. An insertion would be “hindi ko na alam”, a deletion would be “hindi alam”, and a substitution would be “hindi mo alam”. 



Other than the WER, this study looks into the phoneme confusion matrices of PS27 and PS35 for all of the models to be able to make a detailed analysis of the performance of the models. This is to inspect each phoneme and which phoneme it is often confused for. Thus, this is not only to observe which phonemes are the most difficult to recognize but also to see which phoneme set is suitable for the use case. In this case, this is to analyze if either PS27 or PS35 is suitable for use 

40 

in the Bisaya language. The confusion matrices were also used to further analyze the Filipino acoustic model tested on Bisaya speech and vice versa. Lastly, since the original project’s aim was for children’s speech, the models were evaluated on children’s healthcare speech. To evaluate the models on children’s speech, phoneme error rate (PER) is used since the aim is to evaluate the acoustic model, and the WER is expected to be high due to out-of-vocabulary words. 

41 

## **Chapter 5** 

## **Results and Discussion** 

This chapter presents the results and discusses the analyses of the study. The first section discusses the additional speech data collected and preprocessed. The second section presents the data analysis made on both the Filipino and Bisaya speech data. The third section discusses the ASR models and the overview of their results, word-level analysis, and phoneme-level analysis. Lastly, the fourth section discusses the various experiments done to gain a deeper insight into the best models. 

### **5.1 Additional Speech Data** 

The study collected 4 additional speakers and audio files totaling 4.49 hours of segmented speech. Summing up the healthcare chatbot project’s 9 speakers and FSC’s 10 speakers, the total number of Filipino speakers is 23. The total duration for Filipino audio files is 16.3 hours. A summary of the used speech corpora is seen in Table 5.1. 

Table 5.1: A summary of the speech corpora used in this study 

|**Corpus**|**Speakers**|**Duration (Hours)**|
|---|---|---|
|Bisaya|7|8.97|
|Filipino|9|9.03|
|+ FSC|10|2.78|
|+ Collected Data|4|4.49|



Table 5.2 is a summary of the number of words and audio files for the speech 

42 

corpora. Bisaya has a total of 888 unique words, a total of 48816 total words, and a total of 21458 audio files. The Filipino corpus is split into the original female adult speech corpus with the additional data and the FSC. This is because FSC has a completely different vocabulary and is only used for training while the additional data’s vocabulary is mostly the same as the original speech corpus. For Filipino and Additional Data, there is a total of 966 unique words, 72300 total words, and 21548 audio files. For FSC, there are 741 unique words, 7991 total words, and 7908 audio files. 

Table 5.2: A summary of the number of words and audio files of the speech corpora 

|**Language**|**Unique**<br>**Words**|**Total**<br>**Words**|**Total Audio**<br>**Files**|
|---|---|---|---|
|Bisaya|888|48816|21548|
|Filipino<br>+|966|72300|32073|
|Additional||||
|Data||||
|+ FSC|741|7991|7908|



### **5.2 Data Analyses** 

This study, as mentioned, used PS27 and PS35 for both Filipino and Bisaya. This enables the study to compare the two languages’ phoneme distribution. Figures 5.1 and 5.2 present the phoneme distribution for PS27 for both Filipino and Bisaya respectively. The distribution is also color-coded to group phonemes by their categories. The Filipino phoneme distribution leans heavily towards the usage of vowels. Specifically, the vowels /a/, /i/, and /o/ are frequently used. The next most commonly used phonemes are the nasal phonemes /n/, /m/, and /ng/. This is followed by stops, fricatives, and lastly, glides. For Bisaya phoneme distribution, vowels are also prominent. In this case, it can be observed that Bisaya more frequently used the phoneme /u/ than the phoneme /o/. The reverse is true for Filipino. The next most commonly used phoneme is specifically the phoneme /k/ which is a stop phoneme. This is followed by the liquid phoneme /l/. The next notable phoneme is the glide phoneme /w/ which sees more usage in Bisaya rather than in Filipino. It is also worth noting that phonemes /sh/, /f/, /v/, /ch/, /j/, /th/, and /z/is the least used phonemes since these are either used in English words or a particular group of Filipino and Bisaya words. Specifically, phonemes /f/, /v/, /th/, and /z/ are exclusively used for English words. Furthermore, the use of these phonemes is further lessened since some speakers tend to replace these phonemes with /p/, /b/, /t/, and /s/ respectively. Phonemes /sh/, /ch/, and /j/ 

43 



<!-- Start of picture text -->
HE vowel<br>GE nasal<br>20 fricative<br>affricate<br>Ge liquid<br>EE stop<br>15 Mi glide<br>iu<br>o<br>8<br>Ee<br>u<br># 10<br>5<br>0<br>aniomlkstungpdhgebwreryshf vehj th z<br>Phoanemes<br><!-- End of picture text -->



<!-- Start of picture text -->
EE vowel<br>ME nasal<br>20 fricative<br>affricate<br>Mae liquid<br>MH stop<br>» Mmm glide<br>an<br>oO<br>ai]<br>Cc<br>ov<br>@=)fa 10<br>5<br>0 akiulnowtmbsghydp- erngfshv j- thchz<br>Phonemes<br><!-- End of picture text -->



<!-- Start of picture text -->
20.0 GE vowel<br>GB nasal<br>fricative<br>175 affricate<br>Ws liquid<br>Mmm stop<br>15.0 Ml glide<br>Mm diphone<br>12.5<br>voa<br>gc<br>10.0<br>&<br>75<br>5.0<br>25<br>0.0<br>an iomt ks ungp dt ge bhi r at aw w ay y hash f v chho j oy huheth z<br>Phonemes<br><!-- End of picture text -->



<!-- Start of picture text -->
20.0 GH vowel<br>GE nasal<br>fricative<br>175 affricate<br>Ms liquid<br>15.0 GamMH stopglide<br>Mmm diphone<br>12.5<br>vo<br>a<br>8ra8 10.0<br>&<br>75<br>5.0<br>25<br>0.0<br>akuietnombswt gdp ei r awng hi y ha ay at f sh v j hu oy th ch z hohe<br>Phonemes<br><!-- End of picture text -->

group of words are present here. Enclitic words such as _ko_ (me/mine), _na_ (already), _wa_ (no/none), and _sa_ (referring to a place). Similar general answers are also present such as _wa ko kahibalo_ or _wa ko kaybaw_ (I do not know) as well as _nakalimot na ko_ (I already forgot). 

Table 5.4: Most frequently occurring words in Bisaya 

|**Word**|**Count (out of** _∼_**49000)**|
|---|---|
|ko|7085|
|wala|3447|
|na|3059|
|kahibalo|2278|
|wa|2275|
|nakalimot|1993|
|sa|1241|
|kaybaw|994|
|kibaw|885|
|dili|745|



Tables 5.5 and 5.6 show the most frequent bigrams for both Filipino and Bisaya respectively. Filipino bigrams are primarily fragments of statements that convey uncertainty as it is one of the most general responses in the transcript. Some examples are the statements _hindi ko alam_ (I do not know), _nakalimutan ko na_ (I forgot), and _hindi ko matandaan_ (I cannot remember). The rest are statements of duration or time such as _nung isang araw_ (a day ago), _nung isang linggo_ (a week ago), and _minsan po_ (sometimes). The same can be said for Bisaya. The phrase _wala ko kahibalo_ (I do not know) is often seen in the transcript but with different variations. The word _wala_ (not/none) is synonymous with _wa_ . The word _kahibalo_ (know) is synonymous with the words _kaybaw_ , _kibaw_ , and _kahibaw_ . The bigram _nakalimot na_ (I forgot) is also present. The rest are also statements of duration or time such as _miaging buwan_ (last month) and _miaging simana_ (last week). 

47 

Table 5.5: Most frequently occurring 2-grams in Filipino 

|**2-gram**|**Count (out of** _∼_**40000)**|
|---|---|
|hindi ko|4037|
|ko alam|3249|
|ko na|2094|
|nakalimutan ko|2079|
|nung isang|875|
|hindi po|636|
|isang araw|557|
|isang linggo|500|
|minsan po|479|
|ko matandaan|443|



Table 5.6: Most frequently occurring 2-grams in Bisaya 

|**2-gram**|**Count (out of** _∼_**27000)**|
|---|---|
|ko kahibalo|2276|
|wala ko|2270|
|wa ko|2266|
|na ko|2133|
|nakalimot na|1985|
|ko kaybaw|992|
|ko kibaw|885|
|ko kahibaw|341|
|miaging buwan|171|
|miaging simana|170|



Tables 5.7 and 5.8 show to most frequent trigrams for both Filipino and Bisaya respectively. As expected, the phrases talked about for bigrams are present as the most frequent trigrams. However, there are additional phrases for trigrams such as _apat na araw_ (four days), _anim na araw_ (six days), and _sanggol pa lang_ (just a baby). The same can be said for Bisaya wherein the variations of _wala ko kahibalo_ (I do not know) are seen. Additional phrases are present such as _adunay kauban na_ (both/accompanying), _usa ka simana_ (last week), and _lapas na sa_ (beyond). It is worth noting that the trigrams for Bisaya get sparse quickly after the statements of uncertainty while Filipino trigrams, in comparison, are still relatively dense. This could be one of the reasons Bisaya models perform worse when using trigrams and Filipino models perform better when using trigrams. The performances of the ASR are discussed in the following sections. 

48 

Table 5.7: Most frequently occurring 3-grams in Filipino 

|**3-gram**|**Count (out of** _∼_**19000)**|
|---|---|
|hindi ko alam|3234|
|nakalimutan ko na|2061|
|hindi ko matandaan|437|
|nung isang araw|315|
|nung isang linggo|301|
|apat na araw|176|
|nung isang buwan|174|
|anim na araw|163|
|hindi naman po|150|
|sanggol pa lang|139|



Table 5.8: Most frequently occurring 3-grams in Bisaya 

|**3-gram**|**Count (out of** _∼_**14000)**|
|---|---|
|wala ko kahibalo|2196|
|nakalimot na ko|1976|
|wa ko kaybaw|964|
|wa ko kibaw|870|
|wa ko kahibaw|322|
|adunay kauban na|96|
|usa ka simana|87|
|lapas na sa|84|
|wa ko kahibalo|76|
|nakalimut na ko|64|



### **5.3 ASR Models** 

This section discusses the performances of both HMM-GMM and hybrid HMMNN approaches and experiments outlined in the previous chapter. As mentioned, all ASR models use a 1%-25% weighted language model to decode audio into plain text. All model WERs displayed in this section use the best weight for the language model. Each subsection is composed of an introductory paragraph, an overview of results, a word-level analysis of the two best models for PS27 and PS35, and a phoneme-level analysis of the mentioned models. 

49 

##### **5.3.1 HMM-GMM Filipino ASR** 

This section presents the results and discussions obtained from our investigation into the performance of Filipino HMM-GMM-based ASR systems. To gain a deeper understanding of how the models are performing, word-level and phonemelevel analyses are also discussed. 

###### **Overview of Results** 

Tables 5.9 and 5.10 display the WER of all Filipino 3-,4-, and 5-state HMM-GMM models with 2-gram and 3-gram language models for PS27 and PS35 respectively. As expected monophone training performs the worst overall with 10.50% WER being the best. This is because it does not take into account surrounding context phonemes. Triphone training sees a significant performance improvement compared to monophone training with a 5.13% WER. However, LDA+MLLT sees no significant change in performance with the best having a 5.06% WER. Lastly, SAT proves to be the best model enhancement technique out of the previously mentioned with a 3.96% WER. The effectiveness of LVTLN is seen when applied to tri and LDA+MLLT. However, it sees no significant change when applied to SAT. The 3-gram language model has a slight increase in performance over the 2-gram for all models. The utilization of either PS27 or PS35 does not exhibit a significant increase in performance since both offer similar results with PS27 marginally performing better. For PS27, the best-performing model is the 3-gram 3-state SAT model with a 3.96% WER. Similarly for PS35, it is the 3-gram 4-state SAT model with a 3.97% WER. 

Table 5.9: Overview of WER Results for Filipino HMM-GMM models using PS27 

|**FIL PS27**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**mono**|12.05%|12.98%|13.56%|**10.50%**|11.16%|11.80%|
|**tri**|6.29%|6.10%|5.81%|5.56%|5.34%|**5.13%**|
|**LDA+MLLT**|6.95%|6.31%|6.13%|6.15%|5.53%|**5.51%**|
|**SAT**|4.45%|4.32%|4.81%|**3.96%**|4.00%|4.40%|
|**LVTLN + tri**|5.97%|5.27%|5.62%|5.32%|**4.76%**|5.03%|
|**LVTLN**<br>**+**<br>**LDA**<br>**+**<br>**MLLT**|6.32%|5.60%|5.51%|5.50%|5.22%|**5.04%**|
|**LVTLN**<br>**+**<br>**SAT**|4.15%|4.16%|4.16%|4.00%|4.02%|**4.00%**|



50 

Table 5.10: Overview of WER Results for Filipino HMM-GMM models using <u>PS35</u> 

|**FIL PS35**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**mono**|12.32%|12.85%|13.26%|**10.80%**|11.03%|11.43%|
|**tri**|6.09%|5.97%|6.11%|**5.27%**|5.30%|5.42%|
|**LDA+MLLT**|6.88%|5.80%|6.07%|5.97%|**5.06%**|5.28%|
|**SAT**|4.59%|4.25%|4.71%|4.13%|**3.97%**|4.42%|
|**LVTLN + tri**|6.74%|6.66%|5.89%|6.08%|5.80%|**5.35%**|
|**LVTLN**<br>**+**<br>**LDA**<br>**+**<br>**MLLT**|7.63%|6.72%|5.76%|6.77%|5.91%|**5.12%**|
|**LVTLN**<br>**+**<br>**SAT**|4.56%|4.58%|4.37%|**4.16%**|4.26%|**4.16%**|



###### **Word-Level Analysis** 

To gain a deeper understanding of how the models are performing and which areas the models are struggling in, word-level analysis is done on the best-performing models for both PS27 and PS35. The best model for PS27, as mentioned above, is the 3-gram 3-state SAT model. The best model for PS35 is the 3-gram 3-state SAT model. Looking into the word-level performance of both, Table 5.11 presents the most frequent substitutions. 

Starting with the substitutions, the word _oo_ (yes) is most often replaced with the word _ko_ (me/mine). Since vowels are typically larger in terms of amplitude and quasi-periodic, the sound wave for _oo_ displays such characteristics in the sound waveform in Figure 5.5. It is worth noting there is no silence between the two phonemes and there are also instances wherein the word _oo_ is shortened to just one phoneme /o/ instead of /o o/. This becomes confusing when dealing with instances such as in Figure 5.6 wherein the word _ko_ is often followed by another word. A good example is the word _alam_ (know). Figure 5.6 also displays the same characteristics as Figure 5.5 but with a /k/ phoneme in the beginning. Thus, the model may be struggling with instances with a similar enough sequence of phoneme groups. Similar instances are the following: 1) /a l a m/ and /l a ng/ which confuse nasal phonemes at the end, 2) /p o/ and /a k o/ or /k o/ which confuse stop phonemes /p/ and /k/, and 3) /w a l a/ and /b a l a t/ which both have /a l a/. Another instance wherein the model struggles is with a word that is a substring to another word. Sample instances are the words _lang_ (only) and _palang_ (only) as well as _drops_ and _eyedrops_ . The model also struggles similarly 

51 

with different tenses of words with an added prefix, suffix, or even infix. Some of the words are due to a lack of standardization in the transcription in English codeswitching. Some examples include 1) _mam_ and _maam_ , 2) _chocolate_ and _tsokolate_ , and 4) _vitamin_ and _bitamin_ . 

Table 5.11: Most frequent substitutions of the best Filipino models for PS27 and PS35 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**30,000)**|**Count**<br>**(out**<br>_∼_**30,000)**|**PS35**<br>**of**<br>|
|---|---|---|---|---|
|oo|ko|48|30||
|alam|lang|36|33||
|lang|palang|30|30||
|po|ako|30|4||
|mam|maam|28|20||
|lang|nalang|17|17||
|di|hindi|16|16||
|po|ko|13|4||
|vitamin|bitamin|12|17||
|wala|balat|9|19||



52 





<!-- Start of picture text -->
a<br><!-- End of picture text -->

# <u>a</u> 

Table 5.12: Most frequent deletions and insertions of the best Filipino models for PS27 <u>and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**30,000)**|**Count**<br>**PS35**<br>**(out**<br>**of**<br>_∼_**30,000)**|
|---|---|---|---|
|_<_EMPTY_>_|pag|15|15|
|_<_EMPTY_>_|nag|13|13|
|_<_EMPTY_>_|po|10|12|
|_<_EMPTY_>_|ko|7|6|
|_<_EMPTY_>_|pa|6|12|
|na|_<_EMPTY_>_|36|30|
|pa|_<_EMPTY_>_|32|30|
|pag|_<_EMPTY_>_|22|23|
|mag|_<_EMPTY_>_|16|16|
|nag|_<_EMPTY_>_|10|10|



###### **Phoneme-Level Analysis** 

Looking at a simplified phoneme confusion matrix for PS27 in Table 5.13, most of the errors are within the same phoneme group such as vowels, stops, and nasals. Vowel phonemes are one of the most confusing phonemes. Specifically, phonemes /o/ and /u/ are often interchanged as well as phonemes /i/ and /e/. It is worth noting that even if there are significantly more errors or substitutions in the phoneme level, decoding into word level is not necessarily affected by this. This is because it is common for words with /o/ to be pronounced as /u/ and vice versa. Examples of these include _alikabok_ (dust) pronounced as /a l i k a b o k/ or /a l i k a b u k/, _hayop_ (animal) pronounced as /h a y o p/ or /h a y u p/, _hindi_ (no) pronounced as /h i n d i/ or /h i n d e/, and _babae_ (girl) pronounced /b a b a e/ or /b a b a i/. Another interesting case wherein the model sometimes struggles is with the vowel phoneme /i/ and the glide phoneme /y/. Words such as _babae_ (girl) can also be pronounced as /b a b a y i/. This can also be seen with /w/ and /u/. An example is _buwan_ (month) which can be pronounced as /b u w a n/, /b w a n/, or /b u a n/. 

55 

Table 5.13: Most frequent <u>phoneme</u> errors of the best Filipino models for PS27 

|**Ground Truth**|**Hypothesis**|**Count (out of**<br>_∼_**140,000)**|
|---|---|---|
|o|u|4152|
|i|e|331|
|u|o|250|
|e|i|164|
|i|y|77|
|a|u|55|
|e|a|48|
|p|k|47|
|m|ng|38|
|w|u|28|



Looking at the simplified phoneme confusion matrix for PS35 in Table 5.14, the same argument can be said for phoneme groups. However, with the addition of diphones, it introduces a new problem, redundancy. One great example of this is the word _hinahayaan_ (to leave alone). It can be transcribed as both /hi n a ha y a a n/ and /hi n a ha ay a a n/. In other cases, it simply omits one of the phonemes from the diphone or adds one to a single phone. The word _apat_ (four) is pronounced as /a p at/ but is often transcribed as /ha p at/. Although in some cases, this does not affect the decoded word. models may struggle with edge cases due to the redundancy the diphones introduce. This may be one of the reasons PS35 performs slightly worse than PS27. 

Table 5.14: Most frequent <u>phoneme</u> errors of the best Filipino models for PS35 

|**Ground Truth**|**Hypothesis**|**_Count (out of_**<br>_∼_**_140,000)_**|
|---|---|---|
|o|u|3641|
|aw|w|314|
|a|ha|200|
|e|i|129|
|i|e|83|
|at|t|80|
|i|ay|65|
|ay|y|60|
|y|ay|44|
|w|u|40|



56 

##### **5.3.2 HMM-GMM Bisaya ASR** 

In this section, we present the results and discussions obtained from our investigation into the performance of Bisaya HMM-GMM-based ASR systems. To gain a deeper understanding of how the models are performing, word-level and phoneme-level analyses are also discussed. 

###### **Overview of Results** 

Tables 5.15 and 5.16 display the WER of all Bisaya 3-,4-, and 5-state HMM-GMM models with 2-gram and 3-gram language models for PS27 and PS35 respectively. A similar analysis to Filipino can be made on the Bisaya models. Monophone training is the worst overall with the best model having 13.13% WER. Triphone training improved this to 7.28% WER. Using LDA+MLLT, similarly to Filipino models, see no significant change in performance. The best model for LDA+MLLT has an 8.05% WER. Using SAT is the best overall model with a 5.41% WER. The effect of LVTLN on the performances of the models is unclear. On one hand, models that use LVTLN on PS27 see a slightly worse performance. On the other hand, models that use LVTLN on PS35 see an increase in performance. The 2-gram language model consistently outperformed the 3-gram language model. Comparing phoneme sets, in terms of overall performance, PS27 marginally outperformed PS35. However, looking at the best models for each phoneme set, we can see that PS27’s 2-gram 3-state SAT with a WER of 5.41% outperformed PS35’s 2-gram 3-state LVTLN+SAT with a WER of 5.82%. 

Table 5.15: Overview of WER Results for Bisaya HMM-GMM models using PS27 

|**BIS PS27**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**mono**|**13.13%**|13.66%|13.99%|14.92%|15.60%|16.06%|
|**tri**|8.28%|8.13%|**7.61%**|10.50%|11.15%|11.09%|
|**LDA+MLLT**|**8.05%**|8.38%|8.64%|11.36%|10.82%|11.57%|
|**SAT**|**5.41%**|6.69%|6.18%|8.20%|8.91%|8.47%|
|**LVTLN + tri**|**7.22%**|8.25%|8.24%|11.86%|11.08%|11.71%|
|**LVTLN**<br>**+**<br>**LDA**<br>**+**<br>**MLLT**|8.68%|**8.15%**|8.38%|9.44%|9.61%|9.73%|
|**LVTLN**<br>**+**<br>**SAT**|**5.88%**|6.10%|6.22%|11.96%|12.39%|11.78%|



57 

Table 5.16: Overview of WER Results for Bisaya HMM-GMM models using PS35 

|**BIS PS35**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**mono**|**13.57%**|**13.16%**|14.46%|15.83%|15.86%|16.82%|
|**tri**|9.15%|**7.28%**|**7.52%**|11.82%|10.49%|10.74%|
|**LDA+MLLT**|**8.74%**|**8.48%**|8.60%|11.79%|11.66%|11.68%|
|**SAT**|**8.18%**|8.21%|8.68%|11.54%|11.83%|12.14%|
|**LVTLN + tri**|**7.82%**|8.11%|8.16%|10.54%|11.35%|10.90%|
|**LVTLN**<br>**+**<br>**LDA**<br>**+**<br>**MLLT**|7.82%|**7.57%**|7.78%|10.96%|10.96%|11.00%|
|**LVTLN**<br>**+**<br>**SAT**|**5.82%**|6.09%|6.10%|9.40%|9.64%|9.70%|



###### **Word-Level Analysis** 

Table 5.17 shows the word substitutions of the best models using PS27 and PS35. To reiterate, the best-performing model for PS27 is the 2-gram 3-state SAT. For PS35, the best-performing model is the 2-gram 3-state LVTLN+SAT. 

The most frequent word substituted for each other is _miaging_ (formal of previous) and _niaging_ (informal of previous). This is the same argument of the models struggling with the phonemes from the same group. In this case, it is more difficult for the model to decode since it has the same meaning; the language model would not be beneficial. Examples in Table 5.17 wherein the model struggles with the same phoneme group are the words _oh_ (informal of yes) and _ko_ (me/mine), _oh_ (informal of yes) and _oo_ (yes), _kaybaw_ (informal of know) and _kahibaw_ (know), as well as _og_ (a/an) and _ug_ (and). Substring substitutions are also present in Bisaya. Examples of this include _man_ (also) and _naman_ (really), _ko_ (me/mine) and _rako_ (me), _adlaw_ (day) and _kaadlaw_ (day). 

58 

Table 5.17: Most frequent substitutions of the best Bisaya models for PS27 and PS35 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**27,000)**|**Cound**<br>**(out**<br>_∼_**27,000)**|**PS35**<br>**.of**<br>|
|---|---|---|---|---|
|miaging|niaging|173|265||
|oh|ko|115|101||
|oh|oo|114|142||
|og|ug|91|90||
|man|naman|26|28||
|niaging|miaging|22|14||
|duha|duwa|21|10||
|ko|rako|18|18||
|kaybaw|kahibaw|14|18||
|adlaw|kaadlaw|13|12||



Table 5.18 presents the most frequent insertions and deletions of PS27 and PS35 in Bisaya. Similarly to Filipino, the insertions and deletions of Bisaya are mostly enclitic or particle words such as _ko_ (me/mine), _oh_ (informal of yes), _to_ (English word, direction), _ga_ (no), _na_ (that), _nag_ (did), _ra_ (just), _ka_ (you), and _kay_ (from). 

Table 5.18: Most frequent deletions and insertions of the best Bisaya models for PS27 <u>and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**27,000)**|**Count**<br>**PS35**<br>**(out**<br>**of**<br>_∼_**27,000)**|
|---|---|---|---|
|_<_EMPTY_>_|ko|53|15|
|_<_EMPTY_>_|oh|19|20|
|_<_EMPTY_>_|to|13|10|
|_<_EMPTY_>_|kay|3|12|
|_<_EMPTY_>_|ga|0|6|
|na|_<_EMPTY_>_|47|54|
|nag|_<_EMPTY_>_|26|25|
|ra|_<_EMPTY_>_|23|26|
|ka|_<_EMPTY_>_|19|13|
|og|_<_EMPTY_>_|17|18|



59 

###### **Phoneme-Level Analysis** 

Table 5.19 presents a simplified phoneme confusion matrix of the most frequent phonemes being substituted. Similar cases are presented here wherein the model sometimes struggles to differentiate phonemes within the same phoneme groups. Vowel phonemes are once again one of the most confused with phonemes. Specifically, the phonemes that are interchanged the most are /o/ and /u/ as well as /i/ and /e/. The glide /y/ is also confused with /i/ due to its similar pronunciation. Nasal phonemes /n/ and /m/ are also interchanged. The phoneme /th/ is also often interchanged with /t/. 

Table 5.19: Most frequent <u>phoneme</u> errors of the best Bisaya models for PS27 

|**Ground Truth**|**Hypothesis**|**Count (out of**<br>_∼_**100,000)**|
|---|---|---|
|o|u|2159|
|u|o|1114|
|i|y|688|
|y|i|659|
|i|e|582|
|n|m|193|
|e|r|103|
|m|n|93|
|th|t|85|
|e|i|49|



Table 5.20 presents a simplified phoneme confusion matrix for PS35 of the most frequent phoneme substitutions. Again, similar sequences of phoneme groups prove to be a problem for the models with similar cases being present in the list such as vowels and nasal phonemes. The diphones /hi/ and /ay/ are one of the most frequently interchanged phonemes because of the words _kahibaw_ (know) and _kaybaw_ (informal of know). Speakers tend to switch between these two pronunciations frequently. Thus, the model may be struggling with this particular example. The same argument for the omission of a phoneme from a diphone can be made here with /y/ and /ay/ as well as /at/ and /t/. These examples come from the model technically transcribing the word correctly but failing to follow the transcription rules for PS35. An example is the word _katuig_ (year) which is transcribed as /k at u w i g/ but the model often transcribes it as /k a t u w i g/. 

60 

Table 5.20: Most frequent <u>phoneme</u> errors of the best Bisaya models for PS35 

|**Ground Truth**|**Hypothesis**|**Count (out of**<br>_∼_**100,000)**|
|---|---|---|
|u|o|2172|
|o|u|1289|
|hi|ay|852|
|y|ay|562|
|y|i|323|
|i|e|211|
|at|t|180|
|m|n|174|
|e|r|84|
|e|i|82|



##### **5.3.3 Filipino Neural Network Approaches** 

This section presents the results and discussions obtained from the performance of Filipino baseline DNN-HMM-based and TDNN-HMM-based ASR systems. To gain a deeper understanding of how the models are performing, word-level and phoneme-level analyses are also discussed. 

###### **Overview of Results** 

Tables 5.21 and 5.22 display the overview of the results of the Filipino models which are the baseline DNN-HMM, TDNN-HMM symmetrical, TDNN-HMM asymmetrical, and TDNN-HMM subsampled. This also includes the experiments on 2- and 3-gram language models, 3-, 4-, and 5-HMM states, as well as PS27 and PS35. 

The DNN-HMM model performed the worst in relation to neural network approaches. Comparing it with HMM-GMM models, it performs better than monophone training but worse than all other models. The best model for DNNHMM is the PS35 3-gram 5-state DNN-HMM with 7.25% WER. Moving on to TDNN-HMM, the results are all relatively similar to each other. The TDNN models perform similarly to SAT models but with marginal improvements. The best models’ performances for the TDNN approaches are not far from each other with TDNN symmetrical having a 3.60%, TDNN asymmetrical having 3.48% WER, and TDNN subsampled having 3.52% WER which are all models using PS27. Although, models using PS35 are not far behind in terms of performance. With 

61 

this being said, the best model for Filipino is the 3-gram 5-state TDNN asymmetrical model using PS27 with a 3.48% WER. This is a decrease in WER of 0.48% compared to the best HMM-GMM Filipino model. The following word-level analysis and phoneme-level analysis will discuss in which areas the neural network approach improved. 

Table 5.21: Overview of WER Results for Filipino neural network models using <u>PS27</u> 

|**FIL PS27**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**DNN**|9.88%|9.00%|7.77%|9.34%|8.80%|**7.29%**|
|**TDNN**<br>**sym-**<br>**metrical**|4.32%|4.14%|3.99%|4.01%|3.80%|**3.60%**|
|**TDNN asym-**<br>**metrical**|4.64%|4.37%|3.90%|4.29%|4.09%|**3.48%**|
|**TDNN**<br>**sub-**<br>**sampled**|4.34%|4.19%|3.94%|4.08%|3.92%|**3.52%**|



Table 5.22: Overview of WER Results for Filipino neural network models using <u>PS35</u> 

|**FIL PS35**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**DNN**|9.32%|8.49%|7.60%|9.02%|7.85%|**7.25%**|
|**TDNN**<br>**sym-**<br>**metrical**|4.32%|4.41%|4.14%|3.97%|4.16%|**3.66%**|
|**TDNN asym-**<br>**metrical**|4.95%|4.36%|4.28%|4.95%|4.02%|**3.91%**|
|**TDNN**<br>**sub-**<br>**sampled**|4.84%|4.45%|3.86%|4.57%|4.05%|**3.51%**|



###### **Word-Level Analysis** 

The word-level analysis in Table 5.23 is based on the best models for PS27 and PS35 which are the 3-gram 5-state TDNN-HMM asymmetrical and 3-gram 5- state TDNN-HMM subsampled. As opposed to HMM-GMM models, the TDNN models have significantly fewer instances of substitutions overall. Specifically, there are fewer instances of errors regarding similar sequences of phoneme groups such as _alam_ (know) and _lang_ (only). Most of the instances are substrings of the other such as _lang_ (only) with _nalang_ (only), _lang_ (only) with _palang_ (only), 

62 

_di_ (informal of no) with _hindi_ (no), and _inhaler_ with _maginhaler_ (will use an inhaler). Homophones are also present such as the words _mam_ and _maam_ , _vitamin_ and _bitamin_ , as well as _si_ and _c_ . 

Table 5.23: Most frequent substitutions of the best Filipino neural network models for <u>PS27 and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**30,000)**|**Count**<br>**(out**<br>_∼_**30,000)**|**PS35**<br>**of**<br>|
|---|---|---|---|---|
|lang|nalang|16|15||
|lang|palang|16|15||
|di|hindi|12|12||
|mam|maam|12|13||
|alam|lang|10|10||
|na|lang|9|18||
|ng|nang|7|7||
|vitamin|bitamin|6|6||
|inhaler|maginhaler|5|5||
|si|c|4|4||



Table 5.24 presents the insertions and deletions that the models make. Similar to HMM-GMM, these are usually enclitic or particle words. As expected, the TDNN models handle these better since there are fewer deletions and insertions overall. 

Table 5.24: Most frequent deletions and insertions of the best Filipino neural network <u>models for PS27 and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**30,000)**|**Count**<br>**PS35**<br>**(out**<br>**of**<br>_∼_**30,000)**|
|---|---|---|---|
|_<_EMPTY_>_|pag|13|9|
|_<_EMPTY_>_|a|9|2|
|_<_EMPTY_>_|ng|9|4|
|_<_EMPTY_>_|po|7|5|
|_<_EMPTY_>_|lang|6|1|
|mag|_<_EMPTY_>_|10|10|
|pa|_<_EMPTY_>_|10|7|
|pag|_<_EMPTY_>_|10|10|
|na|_<_EMPTY_>_|9|11|
|ko|_<_EMPTY_>_|4|2|



63 

###### **Phoneme Level Analysis** 

Table 5.25 presents a simplified phoneme confusion matrix for PS27. Most of the phoneme errors are within phoneme groups. The same arguments from the HMM-GMM phoneme-level analyses are valid here. One interesting case that the models fail to recognize is the phonemes /v/ with /b/ and /th/ with /t/. This is mentioned in the data analysis section wherein phonemes like /v/ and /th/ are exclusively used for English words. However, speakers sometimes pronounce them with a /b/ or /t/. An example would be vitamins wherein it would be pronounced as /b a y t a m i n s/ or three would be pronounced as /t r i/. 

Table 5.25: Most frequent phoneme errors of the best Filipino neural network models for <u>PS27</u> 

|**Ground Truth**|**Hypothesis**|**Count (out of**<br>_∼_**140,000)**|
|---|---|---|
|o|u|1418|
|u|o|275|
|e|i|75|
|i|y|45|
|i|a|40|
|i|e|34|
|v|b|23|
|e|a|22|
|th|t|16|
|w|u|14|



Table 5.26 presents a simplified phoneme confusion matrix for PS35. Again, the same arguments from PS27 can be made here with the addition of the previously mentioned argument of the omission of a phoneme from a diphone or the insertion of a phoneme to make a diphone. The number of phoneme errors is significantly less than its HMM-GMM counterparts. 

64 

Table 5.26: Most frequent phoneme errors of the best Filipino neural network models for <u>PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count (out of**<br>_∼_**140,000)**|
|---|---|---|
|o|u|1346|
|u|o|214|
|aw|w|103|
|ay|y|80|
|e|i|83|
|i|y|48|
|i|ay|40|
|at|t|20|
|y|ay|18|
|w|u|14|



Table 5.27 displays the average training time for the models and the average inference time per response. These models were trained on an i5-12400 CPU and a GTX 1050Ti GPU. Each model was trained on about 12.5 hours of training data. The inference time was tested on responses with an average of 1.47 seconds in duration. The TDNN symmetrical has the most time to train and the TDNN subsampled has the least time to train. This confirms that the redundancy in overlapping context frames between hidden layers does not significantly affect the performance of the models. Thus, if a shorter training time is necessary, training subsampled models may be a more optimal approach rather than using non-subsampled models. Looking at the inference time per response, DNN is the fastest, and TDNN symmetrical is the slowest. The TDNN asymmetric and TDNN subsampled have a similar inference time with each other. These inference times are expected because of the topology of each architecture. It is worth noting that this inference time is done using the decoding script prepared by Kaldi and can be further optimized to bring down the inference time. 

65 

Table 5.27: Summary of average training time and average inference time per response for Filipino neural network models 

|**Model**|**Avg.**<br>**Train**<br>**Time**<br>**(min-**<br>**utes)**|**Avg.**<br>**Infer-**<br>**ence**<br>**Time**<br>**per**<br>**Response**<br>**(seconds)**|
|---|---|---|
|DNN|98.5 minutes|2.6 seconds|
|TDNN symmet-<br>rical|135.2 minutes|3.8 seconds|
|TDNN<br>asym-<br>metrical|128.0 minutes|3.0 seconds|
|TDNN subsam-<br>pled|88.8 minutes|2.9 seconds|



Table 5.28 compares each Filipino model according to its number of parameters, average training time, average inference time, and overall performance. Both the TDNN asymmetric and the TDNN subsampled are the most optimal and efficient models. Although the baseline DNN model has a lower number of parameters and faster inference time, its WER is still significantly much higher than the TDNN models. The TDNN symmetric, on the other hand, has the highest number of parameters and slowest training time with no significant improvement over the TDNN asymmetric and TDNN subsampled. 

Table 5.28: Comparison of Filipino NN models’ efficiency <u>performance</u> 

|**Model**|**Number**<br>**of**<br>**parameters**|**Avg.**<br>**Train**<br>**Time**|**Avg.**<br>**Infer-**<br>**ence**<br>**Time**<br>**per**<br>**Re-**<br>**sponse**|**Best**<br>**WER**|
|---|---|---|---|---|
|DNN|3.1 million|98.5 minutes|2.6 seconds|7.25%|
|TDNN<br>sym-<br>metrical|4.9 million|135.2 minutes|3.8 seconds|3.60%|
|TDNN asym-<br>metrical|4 million|128.0 minutes|3.0 seconds|3.48%|
|TDNN<br>sub-<br>sampled|3.3 million|88.8 minutes|2.9 seconds|3.51%|



66 

##### **5.3.4 Bisaya Neural Network Approaches** 

This section presents the results and discussions obtained from the performance of Bisaya baseline DNN-HMM-based and TDNN-HMM-based ASR systems. To gain a deeper understanding of how the models are performing, word-level and phoneme-level analyses are also discussed. 

###### **Overview of Results** 

Tables 5.29 and 5.30 display the overview of the results of Bisaya models which are the baseline DNN-HMM, TDNN-HMM symmetrical, TDNN-HMM asymmetrical, and TDNN-HMM subsampled. This also includes the experiments on 2- and 3-gram language models, 3-, 4-, and 5-HMM states, as well as PS27 and PS35. Contrary to the Filipino models’ results, the baseline DNN-HMM model performed better than the TDNN approaches. The best-performing model for DNN-HMM is PS35’s 2-gram 5-state DNN-HMM with a WER of 5.50%. Similarly to Filipino’s TDNN models, the TDNN models’ performances are not far from each other with TDNN symmetrical having a 6.88% WER, TDNN asymmetrical having a 6.61% WER, and TDNN subsampled having a 6.37% WER which are all models using PS35. Again, models using PS27 have performances similar to models using PS35. The best-performing model for Bisaya overall is the 2-gram 5-state DNN-HMM using PS35 with 5.50% WER. Compared to the best HMM-GMM model, there is no significant difference in performance. 

Table 5.29: Overview of WER Results for Bisaya neural network models using <u>PS27</u> 

|**BIS PS27**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**DNN**|**5.88%**|6.08%|6.01%|12.95%|9.91%|9.73%|
|**TDNN**<br>**sym-**<br>**metrical**|**6.56%**|9.65%|7.67%|10.91%|13.07%|11.16%|
|**TDNN asym-**<br>**metrical**|8.76%|8.82%|**7.01%**|11.32%|11.12%|10.62%|
|**TDNN**<br>**sub-**<br>**sampled**|8.80%|8.34%|**6.69%**|10.55%|11.89%|10.32%|



67 

Table 5.30: Overview of WER Results for Bisaya neural network models using <u>PS35</u> 

|**BIS PS35**|**2-gram**|||**3-gram**|||
|---|---|---|---|---|---|---|
||**3-state**|**4-state**|**5-state**|**3-state**|**4-state**|**5-state**|
|**DNN**|6.01%|6.22%|**5.50%**|12.32%|9.38%|8.99%|
|**TDNN**<br>**sym-**<br>**metrical**|10.46%|9.62%|**6.88%**|12.89%|12.62%|10.40%|
|**TDNN asym-**<br>**metrical**|9.12%|8.08%|**6.61%**|11.84%|11.29%|10.13%|
|**TDNN**<br>**sub-**<br>**sampled**|9.14%|8.30%|**6.37%**|11.91%|11.21%|9.86%|



###### **Word-Level Analysis** 

The word-level analysis in Table 5.31 is based on the best models for PS27 and PS35 which are the 2-gram 3-state DNN-HMM model and 2-gram 5-state DNNHMM model. With the performances shown in the overview, it is expected that the TDNN models perform similarly to the HMM-GMM models. 

Table 5.31: Most frequent substitutions of the best Bisaya neural network models for <u>PS27 and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**27,000)**|**Cound**<br>**(out**<br>_∼_**27,000)**|**PS35**<br>**of**<br>|
|---|---|---|---|---|
|oh|ko|168|178||
|miaging|niaging|135|171||
|oh|oo|91|92||
|og|ug|89|82||
|man|naman|29|39||
|og|kog|21|9||
|ko|rako|20|17||
|niaging|miaging|20|15||
|kaybaw|kahibaw|19|12||
|inom|naginom|17|23||



Table 5.32 presents the most frequent insertions and deletions of PS27 and PS35 in Bisaya. These are also mostly enclitic words. The number of insertions and deletions does not see a significant difference from its HMM-GMM counterpart. 

68 

Table 5.32: Most frequent deletions and insertions of the best Bisaya neural network <u>models for PS27 and PS35</u> 

|**Ground Truth**|**Hypothesis**|**Count**<br>**PS27**<br>**(out**<br>**of**<br>_∼_**27,000)**|**Count**<br>**(out**<br>_∼_**27,000)**|**PS35**<br>**of**<br>|
|---|---|---|---|---|
|_<_EMPTY_>_|oh|42|32||
|_<_EMPTY_>_|og|17|8||
|_<_EMPTY_>_|wa|8|4||
|_<_EMPTY_>_|ga|8|3||
|_<_EMPTY_>_|ko|5|3||
|na|_<_EMPTY_>_|67|72||
|nag|_<_EMPTY_>_|32|39||
|ka|_<_EMPTY_>_|29|25||
|ra|_<_EMPTY_>_|27|25||
|ko|_<_EMPTY_>_|19|14||



Table 5.33 shows the average train time for each neural network approach. These models are trained on an i5-12400 CPU and a GTX 1050Ti GPU. Each model was trained on about 7.2 hours of training data. The inference time was tested on responses with an average of 1.43 seconds in duration. The TDNN asymmetrical has the most time to train and DNN-HMM has the least training time. The training time is noticeably shorter than the Filipino models due to the size of the dataset. As for the inference time, it is similar to Filipino models’ inference time since the same architectures were used. Again, TDNN symmetric has the highest inference time, and DNN baseline has the shortest inference time. The TDNN asymmetrical and TDNN subsampled have a similar inference time and are lower than the TDNN symmetrical’s inference time. 

69 

Table 5.33: Summary of average training time and average inference time per response for Bisaya neural network models 

|**Model**|**Avg.**<br>**Train**<br>**Time**<br>**(min-**<br>**utes)**|**Avg.**<br>**Infer-**<br>**ence**<br>**Time**<br>**per**<br>**Response**<br>**(seconds)**|
|---|---|---|
|DNN|51.0 minutes|2.5 seconds|
|TDNN symmet-<br>rical|103.2 minutes|3.3 seconds|
|TDNN<br>asym-<br>metrical|92.5 minutes|2.7 seconds|
|TDNN subsam-<br>pled|82.3 minutes|2.8 seconds|



Table 5.34 compares each Bisaya model according to its number of parameters, average training time, average inference time, and overall performance. Contrary to Filipino models, the best-performing and most efficient model, in this case, is the baseline DNN. This is because it has the shortest training time and inference time as well as having the lowest WER. An explanation of why the TDNN models performed sub-optimally on Bisaya data could be inadequate data. This is further discussed in the experiments of the effects on additional data. 

Table 5.34: Comparison of Bisaya NN models’ efficiency <u>performance</u> 

|**Model**|**Number**<br>**of**<br>**parameters**|**Avg.**<br>**Train**<br>**Time**|**Avg.**<br>**Infer-**<br>**ence**<br>**Time**<br>**per**<br>**Re-**<br>**sponse**|**Best**<br>**WER**|
|---|---|---|---|---|
|DNN|3.1 million|51.0 minutes|2.5 seconds|5.50%|
|TDNN<br>sym-<br>metrical|4.9 million|103.2 minutes|3.3 seconds|6.56%|
|TDNN asym-<br>metrical|4 million|92.5 minutes|2.7 seconds|6.61%|
|TDNN<br>sub-<br>sampled|3.3 million|82.3 minutes|2.8 seconds|6.37%|



##### **5.3.5 Summary of Best Models** 

This section summarizes the best models for HMM-GMM and neural network approaches for both Filipino and Bisaya. Table 5.35 displays the model, language 

70 

model, HMM states, phoneme set, and WER of the best-performing models. 

Table 5.35: Summary of the Best Filipino and Bisaya models 

|**Language**|**Model**|**Language**<br>**Model**|**HMM**<br>**States**|**Phoneme**<br>**Set**|**WER**|
|---|---|---|---|---|---|
|Filipino|HMM-<br>GMM SAT|3-gram|3-state|PS27|3.96%|
||TDNN<br>asymmet-<br>ric|3-gram|5-state|PS27|3.48%|
|Bisaya|HMM-<br>GMMSAT|2-gram|3-state|PS27|5.41%|
||DNN-<br>HMM|2-gram|5-state|PS35|5.50%|



To further analyze the best models, Tables 5.36 and 5.37 display the most and least frequently occurring phonemes in Filipino and their PER for the best models SAT and TDNN asymmetric. This is to see if the number of phonemes affects the performance of the model’s ability to identify the phoneme. As expected, phonemes in Table 5.36 are performing well due to the high total count. Although this only shows the 5 most frequent phonemes, all other phonemes have a low PER with the exception of some phonemes in Table 5.37. Table 5.37 includes problematic phonemes such as /o/ and /u/ as seen in previous phoneme confusion analysis. Although the phoneme /o/ has a high total count, the models still struggle with this particular phoneme. Phoneme /u/, on the other hand, has a relatively low PER compared to /o/ but not as low as other phonemes. Moving on to the least frequently occurring phonemes in Table 5.37, surprisingly, some phonemes still manage to have a low PER despite their count. However, phonemes such as /v/, /th/, and /z/ have a high PER. These are also the phonemes mentioned in the data analysis of the phoneme distribution wherein they are only used on English words exclusively and are sometimes exchanged with /b/, /t/, and /s/. These factors may have led to its poor performance. For cases such as these, more training data may be needed. 

71 

Table 5.36: Most frequent <u>phonemes</u> in Filipino and the PER of the best models 

|**Phoneme**|**Total Count**|**SAT (PER)**|**TDNN**<br>**(PER)**|**asym**|
|---|---|---|---|---|
|a|16770|1.52%|1.72%||
|n|13932|1.46%|4.64%||
|i|13762|3.81%|6.29%||
|l|7432|0.44%|0.59%||
|m|7252|2.21%|3.74%||
|e|2671|9.32%|9.87%||



Table 5.37: Least frequent phonemes and problematic phonemes in Filipino and the <u>PER of the best models</u> 

|**Phoneme**|**Total Count**|**SAT (PER)**|**TDNN**<br>**asym**<br>**(PER)**|
|---|---|---|---|
|**o**|**8983**|**48.18%**|**37.98%**|
|**u**|**4067**|**7.01%**|**13.41%**|
|f|250|1.60%|4.50%|
|sh|238|4.36%|4.03%|
|v|138|8.08%|20.00%|
|ch|142|3.52%,|3.64%|
|j|136|0.74%|3.45%|
|th|40|52.50%|85.00%|
|z|29|41.38%|37.50%|



Tables 5.38 and 5.39 similarly display the most and least frequently occurring phonemes for Bisaya and the models’ PER on each. A similar analysis can be made here wherein most of the phonemes have a low PER. A similar analysis can also be made in Table 5.39 with the addition of the phoneme /i/ and phoneme /e/ as problematic phonemes with a high count and a relatively high PER. Although inconclusive in terms of actual WER, this difference in PER for these problematic phonemes may be the differentiating factor between the performances of Filipino and Bisaya models. 

Table 5.38: Most frequent <u>phonemes</u> in Bisaya and the PER of the best models 

|**Phoneme**|**Total Count**|**SAT (PER)**|**DNN (PER)**|
|---|---|---|---|
|a|26169|0.62%|5.62%|
|k|10007|0.40%|1.52%|
|l|7203|0.64%|1.10%|
|n|7345|3.72%|3.50%|



72 

Table 5.39: Least frequent phonemes and problematic phonemes in Bisaya and the <u>PER of the best models</u> 

|**Phoneme**|**Total Count**|**SAT (PER)**|**DNN (PER)**|
|---|---|---|---|
|**o**|**4903**|**49.81%**|**53.01%**|
|**u**|**9628**|**13.55%**|**9.56%**|
|**i**|**8708**|**10.28%**|**16.42%**|
|**e**|**2223**|**26.72%**|**40.23%**|
|f|340|0.59%|1.76%|
|v|210|12.38%|9.52%|
|sh|200|17.00%|14.00%|
|j|154|1.95%|4.55%|
|th|110|92.73%|100.00%|
|ch|56|83.93%|64.29%|
|z|28|71.43%|71.43%|



These results could confirm that the total count of a phoneme is a factor in the performance of the models in identifying them. However, it is not the only factor. The complexity in which the phonemes are being used could also be a factor in this. An example is the phonemes /o/ and /u/. Another thing to note is that the speech corpora used in this study have a relatively low vocabulary and a high total word count. This could mean a high probability of the models training and testing on the same words. Thus, a high count of phonemes but on the same words. However, this also does not disprove the argument that more data most probably yields better results. This only means that the higher the vocabulary, the more training data is required. 

### **5.4 Experiments** 

This section discusses the analysis of language model weights, the use of crosslanguage acoustic models, and the effect of removing the additional data from the Filipino speech corpus. This gives more insight into the mentioned models. The models used in this section are the best models from Table 5.35 

##### **5.4.1 Effects of Additional data on ASR performance** 

This section evaluates the effect of the additional data this study collected and preprocessed. Table 5.40 compares the WER of models trained on only the original 

73 

Filipino speech corpus and models trained with additional data. The DNN-HMM model significantly improved its performance from 14.63% WER with no additional data to 7.29% WER with additional data. This improvement is even more significant when compared to the TDNN approaches from about 12% to 14% WER without additional data to about 3.50% WER with additional data. This could serve as an argument for Bisaya TDNN models’ performances. The total duration of audio files in the Bisaya speech corpus is about as much as the total duration of Filipino audio files when the additional data is removed. Collecting additional data for Bisaya may also increase the WER significantly given the relatively small amount of data available. 

Table 5.40: Comparison of Results of Filipino neural network models with and <u>without additional data</u> 

|**Model**|**Langua**<br>**Model**|**ge**<br>**HMM**<br>**States**|**Phone**<br>**Set**|**me**<br>**WER**<br>**inal**<br>**corpus)**|**(orig-**<br>**speech**|**WER**<br>**(with**<br>**additional**<br>**data + FSC)**|
|---|---|---|---|---|---|---|
|DNN|3-gram|5-state|PS27|14.63%||**7.29%**|
|TDNN<br>sym-<br>metrical|3-gram|5-state|PS27|12.19%||**3.60%**|
|TDNN<br>asym-<br>metrical|3-gram|5-state|PS27|13.45%||**3.48%**|
|TDNN<br>subsam-<br>pled|3-gram|5-state|PS35|14.04%||**3.52%**|



To inspect the relationship of training data to WER further, this study presents line graphs of the effects of the amount of training data on the WER of both Filipino and Bisaya models. The models are trained on 25%, 50%, 75%, and 100% of the data to see the relationship between data and the performance of the models. Figure 5.7 displays the performances of Filipino models with different amounts of training data. As expected, the lower the amount of training data, the lower the WER, and vice versa. One interesting thing to note is the more training data is added, the models’ WER is improved logarithmically. Comparing 75% to 100% of data, the WER of the models only improves by a minute amount. 

74 



<!-- Start of picture text -->
60 =@=— baseline<br>DNN<br>=—e TONN<br>sym<br>40 =—e TDONN<br>= asym<br>ceuy —e- TDNN<br>= sub<br>20<br>0 a<br>25 50 15 100<br>Data (%a)<br>30 =@ baseline<br>DNN<br>—e TONN<br>sym<br>20 —e TDNN<br>= asym<br>a =e TONN<br>= sub<br>10<br>0 a<br>25 50 15 100<br>Data (%a)<br><!-- End of picture text -->

Table 5.41: Results of the best Filipino and Bisaya models on children’s speech 

|**Language**|**Model**|**HMM**<br>**States**|**Phoneme**<br>**Set**|**PER**<br>**(Chil-**<br>**dren’s**<br>**Speech)**|**PER**<br>**(Adult**<br>**Speech)**|
|---|---|---|---|---|---|
|Filipino|HMM-<br>GMM SAT|3-state|PS27|50.90%|22.74%|
||TDNN<br>asymmet-<br>ric|5-state|PS27|52.77%|20.23%|
|Bisaya|HMM-<br>GMM SAT|3-state|PS27|30.92%|22.86%|
||DNN-<br>HMM|5-state|PS35|31.60%|28.81%|



##### **5.4.2 Evaluation of Models on Children’s Speech** 

This section evaluates the best models of actual children’s speech in healthcare. As mentioned, the phoneme error rate is used instead of the word error rate for this experiment. Table 5.41 presents the best models evaluated on the children’s speech. Both HMM-GMM and neural network approaches’ phoneme error rates are similarly relatively high. Although, the Bisaya models seem to perform better than the Filipino models. One reason all the models may be performing poorly is that, again, the frequency of female adult voices is noticeably much lower than those of children. The nature of speech is also conversational while the training data is only designed to mimic conversational speech. The children’s speech also includes mispronunciation, stutters, fillers, and common conversational sounds while the training data does not. The children’s speech is also relatively noisy compared to the training data. Although noise reduction (Sainburg, Thielk, & Gentner, 2020) is already applied to the children’s speech corpus, some noises are still evident in the final children’s speech corpus. 

##### **5.4.3 Cross-Language Acoustic Model** 

With cross-language acoustic models, as mentioned, the Filipino acoustic model will be used on Bisaya speech and vice versa. Table 5.42 presents the crosslanguage performances of the best Filipino and Bisaya models. Overall, the models perform considerably worse. However, the performance is reasonably well considering it is trained on basically another language with minimal overlapping 

76 

words. Furthermore, the HMM-GMM SAT models’ performances are still better than monophone training. Since there are a plethora of languages and dialects in the Philippines, training acoustic models on phonetically similar languages or dialects may be a great alternative for low-resource languages. 

Table 5.42: Results for models evaluated on cross-language 

|**Acoustic**<br>**Model**|**Model**|**Language**<br>**Model**|**HMM**<br>**States**|**Phoneme**<br>**Set**|**WER**<br>**(Cross**<br>**Lan-**<br>**guage)**|
|---|---|---|---|---|---|
|Filipino|HMM-<br>GMM SAT|Bisaya<br>2-gram|3-state|PS27|11.75%|
||TDNN<br>asymmet-<br>ric|Bisaya<br>2-gram|5-state|PS27|15.46%|
|Bisaya|HMM-<br>GMM SAT|Filipino 3-<br>gram|3-state|PS27|9.05%|
||DNN-<br>HMM|Filipino 3-<br>gram|5-state|PS35|14.53%|



##### **5.4.4 Language Model Weights** 

As mentioned in the previous chapter, the language models’ weights are adjusted from 1% to 25%. Figures 5.9 and 5.10 display line graphs of the WER for each language model weight for Filipino and Bisaya respectively. As expected, low language model weights are not optimal for the best performance. From language model weights 1% to 10%, the WER linearly improves. From 10% to 15%, it starts to decrease in terms of rate of improvement. From 15% to 25%, it seems to completely plateau. All models in this study have an optimal language model weight of somewhere between 15% and 25%. Since the language models used in this study are relatively small, a larger language model trained on more general data may see different results. 

77 



<!-- Start of picture text -->
Filipino Language Model Weight WER<br>10<br>=e: SAT | =e TDONN asym<br>8<br>= 6<br>oe<br>in}<br>=4<br>2<br>0a se ee ee ee ee |<br>5 10 15 20 25<br>Weight (2)<br><!-- End of picture text -->

Bisaya Language Model Weight WER 



<!-- Start of picture text -->
12.5<br>SAT == DNN-HMM<br>10<br>= 75<br>oe<br>in}<br>= 5<br>25<br>0 a se ee ee ee ee |<br>5 10 15 20 25<br>Weight (2)<br><!-- End of picture text -->

## **Chapter 6** 

## **Conclusions and Recommendations** 

Filipino ASR studies are primarily focused on the traditional HMM-GMM approach. Studies on Bisaya ASR are also scarce if any. Numerous studies have employed neural network methodologies and achieved favorable outcomes. Most of these studies revolve around end-to-end systems which require massive amounts of data. The reason Philippine languages rarely see any neural network approaches is mainly due to the need for more speech data. Although, one way to mitigate this is to employ a hybrid TDNN-HMM model which still needs more data than an HMM model but less than an end-to-end model. With this being said, this study was able to collect additional Filipino speech data on top of already available data and analyze it, develop a baseline HMM-GMM and explore model enhancement techniques, and develop a TDNN-HMM-based ASR system. 

This study collected 4 additional Filipino speakers’ worth of data totaling 4.49 hours. The data is already segmented into single responses, preprocessed to reduce noise, and transcribed at both word level and phoneme level. This dataset is used as training data for the Filipino HMM and NN models. As mentioned in the analysis of the effects of these additional data, the collection of additional Bisaya speech data may see a significant increase in performance in Bisaya NN models as the Filipino NN models have. 

The study also analyzed the phoneme distribution of the speech data of both Filipino and Bisaya speech. For both Filipino and Bisaya, PS27 is the same as PS35 except for the diphones being distributed to already existing phonemes. The phoneme distribution of Filipino and Bisaya is relatively similar to each other with some subtle differences. Phonemes used exclusively for English words and 

79 

brands are also identified through this. These phonemes are also one of the least frequently used. However, it may be essential when transcribing conversational speech since English code-switching is fairly common in both Filipino and Bisaya. Although arguably, phonemes such as /f/, /v/, /th/, and /z/ are sometimes pronounced as /p/, /b/, /t/, and /s/ depending on the speaker’s preference. 

The study presented multiple HMM-GMM models for both Filipino and Bisaya. There were various experiments made on the phoneme set, _n_ grams, HMM states, language model weights, and model enhancement techniques such as VTLN, LDA+MLLT, and SAT. The best HMM-GMM models are the 3-gram 3-state SAT using PS27 for Filipino with a 3.96% WER and the 2-gram 3-state SAT using PS27 for Bisaya with a 5.41% WER. Overall, the 3-gram language model performed the best for Filipino while the 2-gram language model performed the best for Bisaya. The number of HMM states seems to have varying effects on the performance with no clear indication of improvement. For model enhancement technique, The SAT is the best performing out of all for both Filipino and Bisaya. On the other hand, both VTLN and LDA+MLLT had little to no significant effects on the performance. The study also delves deeper into the word-level analysis which shows 3 categories with which the models are struggling. First, phonemes within the same phoneme group are often substituted with one another. Second, the substring problem wherein a word that is a substring to another longer word is substituted with each other. This is also similar to the problem of (Ing et al., 2022) wherein compound words are sometimes decoded as two separate words. The last problem is homophones wherein the word is completely pronounced the same but is a different word. It also shows that the model, in some cases, inserts or deletes enclitic or particle words. Further looking into the phoneme level analysis confirms the substitutions and identifies the problematic phonemes within the same phoneme group. The results also point to PS27 being slightly better since the phoneme analysis shows that models that use PS35 sometimes introduce redundancy in the transcriptions. 

The study also presented multiple hybrid NN-HMM models for both Filipino and Bisaya. The best NN models are the 3-gram 5-state TDNN asymmetrical model using PS27 for Filipino with a 3.48% WER and the 2-gram 5-state DNN-HMM model using PS35 for Bisaya with a 5.50% WER. The Filipino model improved by about 0.5% WER but the Bisaya model saw no change in performance. Thus, the Bisaya model’s word level analysis and phoneme level analysis are almost the same as its HMM-GMM counterpart. Since the study compared the performance of the models trained with different amounts of data, the trend showed that adding more Bisaya training data would yield an improvement similar to Filipino models. Out of the 3 problem categories mentioned before, the models improved significantly on the words with phonemes within the same phoneme 

80 

group. The substring and homophone problem also improved but it is limited. Since the experiment focused on the improvement of the acoustic model, it is expected that the latter categories see little improvement; most of the instances could be decoded correctly with a better language model. Thus, future works could explore a more appropriate approach which is to employ a larger language model with examples of these substrings and homophones. Future works could also revolve around the modification of the topology of the neural network approaches and other neural network architectures such as RNN and LSTM. 

The study also experimented with using the acoustic model for the crosslanguage model. The Filipino acoustic model is used in Bisaya speech and vice versa. The results show that although the models performed on a subpar level, the performance is still reasonable in terms of WER. Future research could explore utilizing cross-language models on other Philippine languages or dialects with a limited amount of data. Although not optimal, this could be a great alternative. 

Lastly, the study also evaluated the best models for actual children’s speech in healthcare. For both Filipino and Bisaya models, the phoneme error rate was poor. It seems that training exclusively on female adult speech is not sufficient when evaluating children’s speech. There are multiple factors leading to this such as the nature of speech, frequency of voice, quality of the recording, and verbal disfluencies. Future works could explore transfer learning approaches wherein models trained on adult speech such as the models in this study are fine-tuned further with children’s speech. Another possible experiment that could be done is by training on formant modified speech instead of only speed-perturbed speech. This could modify the training data to match the formant qualities of children’s speech better. To address the poor recording quality of the data, training on data with noise or noise augmentation could assist in creating a noise-robust model. 

81 

## **References** 

- Amodei, D., Ananthanarayanan, S., Anubhai, R., Bai, J., Battenberg, E., Case, C., . . . others (2016). Deep speech 2: End-to-end speech recognition in english and mandarin. In _International conference on machine learning_ (pp. 173–182). 

- Anastasakos, T., McDonough, J., Schwartz, R., & Makhoul, J. (1996). A compact model for speaker-adaptive training. In _Proceeding of fourth international conference on spoken language processing. icslp’96_ (Vol. 2, pp. 1137–1140). 

- Ang, F., Burgos, M. C., & De Lara, M. (2011). Automatic speech recognition for closed-captioning of filipino news broadcasts. In _2011 7th international conference on natural language processing and knowledge engineering_ (pp. 328–333). 

- Ang, F., Miyanaga, Y., Guevara, R. C., Cajote, R., & Bayona, M. G. A. (2014). Open domain continuous filipino speech recognition with code-switching. In _2014 ieee international symposium on circuits and systems (iscas)_ (pp. 2301–2304). 

- Aquino, A., Tsang, J. L., Lucas, C. R., & de Leon, F. (2019). G2p and asr techniques for low-resource phonetic transcription of tagalog, cebuano, and hiligaynon. In _2019 international symposium on multimedia and communication technology (ismac)_ (pp. 1–5). 

- Bautista, J. L., & Kim, Y.-J. (2014). An automatic speech recognition for the filipino language using the htk system. In _Proceedings on the international conference on artificial intelligence (icai)_ (p. 1). 

- Briones, M. R. C., Cai, C. M., Te, E. E. C., & Pascual, R. M. (2020). Development of an automatic speech recognizer for filipino-speaking children. 

- Chen, X., & Cheng, J. (2014). Deep neural network acoustic modeling for native and non-native mandarin speech recognition. In _The 9th international symposium on chinese spoken language processing_ (pp. 6–9). 

- Chua, J., Chua, U., de Padua, C., Tan, J. I., & Cheng, D. (2011). Filitext: A filipino hands-free text messaging application. _Undergraduate thesis, De La Salle University_ . 

- Cohen, J., Kamm, T., & Andreou, A. G. (1995). Vocal tract normalization in 

95 

speech recognition: Compensating for systematic speaker variability. _The Journal of the Acoustical Society of America_ , _97_ (5), 3246–3247. 

- Dimzon, F. D., & Pascual, R. M. (2020). An automatic phoneme recognizer for children’s filipino read speech. In _2020 ieee international conference on teaching, assessment, and learning for engineering (tale)_ (pp. 1–5). 

- Diwan, A., Vaideeswaran, R., Shah, S., Singh, A., Raghavan, S., Khare, S., . . . others (2021). Mucs 2021: Multilingual and code-switching asr challenges for low resource indian languages. 

- Du, C., & Yu, K. (2020). Speaker augmentation for low resource speech recognition. In _Icassp 2020-2020 ieee international conference on acoustics, speech and signal processing (icassp)_ (pp. 7719–7723). 

- Eide, E., & Gish, H. (1996). A parametric approach to vocal tract length normalization. In _1996 ieee international conference on acoustics, speech, and signal processing conference proceedings_ (Vol. 1, pp. 346–348). 

- Fadri, D. C. (2017). _Pasabi: Pagmensahe ng salitang binigkas a filipino speechto-text messaging application using recurrent neural networks_ (Unpublished doctoral dissertation). 

- Fathima, N., Patel, T., Mahima, C., & Iyengar, A. (2018). Tdnn-based multilingual speech recognition system for low resource indian languages. In _Interspeech_ (pp. 3197–3201). 

- Georgescu, A.-L., Cucu, H., & Burileanu, C. (2019). Kaldi-based dnn architectures for speech recognition in romanian. In _2019 international conference on speech technology and human-computer dialogue (sped)_ (pp. 1–6). 

- Glembek, O., Burget, L., Matˇejka, P., Karafi´at, M., & Kenny, P. (2011). Simplification and optimization of i-vector extraction. In _2011 ieee international conference on acoustics, speech and signal processing (icassp)_ (pp. 4516– 4519). 

- Graves, A., Fern´andez, S., Gomez, F., & Schmidhuber, J. (2006). Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks. In _Proceedings of the 23rd international conference on machine learning_ (pp. 369–376). 

- Guevara, R. C. L., Co, M., Espina, E., Garcia, I. D., Tan, E., Ensomo, R., & Sagum, R. (2002). Development of a filipino speech corpus. In _3rd national ece conference._ 

- Hannun, A., Case, C., Casper, J., Catanzaro, B., Diamos, G., Elsen, E., . . . others (2014). Deep speech: Scaling up end-to-end speech recognition. _arXiv preprint arXiv:1412.5567_ . 

- Hasan, M. R., Jamil, M., Rahman, M., et al. (2004). Speaker identification using mel frequency cepstral coefficients. _variations_ , _1_ (4), 565–568. 

- Ing, J. A. Y., Pascual, R. M., & Dimzon, F. D. (2022). A hybrid tdnn-hmm automatic speech recognizer for filipino children’s speech. In _2022 ieee international conference on artificial intelligence in engineering and technology_ 

96 

_(iicaiet)_ (pp. 1–6). 

- Jaitly, N., & Hinton, G. E. (2013). Vocal tract length perturbation (vtlp) improves speech recognition. In _Proc. icml workshop on deep learning for audio, speech and language_ (Vol. 117, p. 21). 

- Juang, B.-H., Levinson, S., & Sondhi, M. (1986). Maximum likelihood estimation for multivariate mixture observations of markov chains (corresp.). _IEEE Transactions on Information Theory_ , _32_ (2), 307–309. 

- Kermanshahi, M. A., Akbari, A., & Nasersharif, B. (2021). Transfer learning for end-to-end asr to deal with low-resource problem in persian language. In _2021 26th international computer conference, computer society of iran (csicc)_ (pp. 1–5). 

- Kipyatkova, I. (2017). Experimenting with hybrid tdnn/hmm acoustic models for russian speech recognition. In _International conference on speech and computer_ (pp. 362–369). 

- Ko, T., Peddinti, V., Povey, D., & Khudanpur, S. (2015). Audio augmentation for speech recognition. In _Sixteenth annual conference of the international speech communication association._ 

- Kroeger, P. (1993). _Phrase structure and grammatical relations in tagalog_ . Center for the Study of Language (CSLI). 

- Kunze, J., Kirsch, L., Kurenkov, I., Krug, A., Johannsmeier, J., & Stober, S. (2017). Transfer learning for speech recognition on a budget. _arXiv preprint arXiv:1706.00290_ . 

- Lee, T., Lee, M.-J., Kang, T. G., Jung, S., Kwon, M., Hong, Y., . . . others (2021). Adaptable multi-domain language model for transformer asr. In _Icassp 20212021 ieee international conference on acoustics, speech and signal processing (icassp)_ (pp. 7358–7362). 

- Li, K., Li, J., Ye, G., Zhao, R., & Gong, Y. (2019). Towards code-switching asr for end-to-end ctc models. In _Icassp 2019-2019 ieee international conference on acoustics, speech and signal processing (icassp)_ (pp. 6076–6080). 

- Liao, E. H., Ganareal, K., Paguia, C. C., Agreda, C., Octaviano, M., & Rodriguez, R. (2019). Towards the development of automatic speech recognition for bikol and kapampangan. In _2019 ieee 11th international conference on humanoid, nanotechnology, information technology, communication and control, environment, and management (hnicem)_ (pp. 1–5). 

- Lim, M. L., Xu, A. J., Lin, C. S., Chen, Z., & Pascual, R. (2022). Developing an automatic speech recognizer for filipino with english code-switching in news broadcast. In _2022 14th international conference on knowledge and smart technology (kst)_ (pp. 13–17). 

- Liu, B., Zhang, W., Xu, X., & Chen, D. (2019). Time delay recurrent neural network for speech recognition. In _Journal of physics: Conference series_ (Vol. 1229, p. 012078). 

- Luci-Atienza, C. (2021, Apr). _Dost launches 9 new ai ramp;d projects._ Re- 

97 

trieved from `https://mb.com.ph/2021/04/08/dost-launches-9-new-ai -rd-projects/` 

- Malaay, E., Simora, M., Cabatic, R. J., Oco, N., & Roxas, R. E. (2017). Development of a multilingual isolated digits speech corpus. In _2017 20th conference of the oriental chapter of the international coordinating committee on speech databases and speech i/o systems and assessment (o-cocosda)_ (pp. 1–5). 

- Nacem, S., Iqbal, M., Saqib, M., Saad, M., Raza, M. S., Ali, Z., . . . Arshad, M. U. (2020). Subspace gaussian mixture model for continuous urdu speech recognition using kaldi. In _2020 14th international conference on open source systems and technologies (icosst)_ (pp. 1–7). 

- Nakatani, T. (2019). Improving transformer-based end-to-end speech recognition with connectionist temporal classification and language model integration. In _Proc. interspeech 2019._ 

- Park, D. S., Chan, W., Zhang, Y., Chiu, C.-C., Zoph, B., Cubuk, E. D., & Le, Q. V. (2019). Specaugment: A simple data augmentation method for automatic speech recognition. _arXiv preprint arXiv:1904.08779_ . 

- Pascual, R. M., & Guevara, R. C. L. (2012). Developing a children’s filipino speech corpus for application in automatic detection of reading miscues and disfluencies. In _Tencon 2012 ieee region 10 conference_ (pp. 1–6). 

- Pascual, R. M., & Guevara, R. C. L. (2017). Experiments and pilot study evaluating the performance of reading miscue detector and automated reading tutor for filipino: A children’s speech technology for improving literacy. _Science Diliman_ , _29_ (1). 

- Payne, T. E. (1994). The pragmatics of voice in a philippine language: Actor-focus and goal-focus in cebuano narrative. _Voice and inversion_ , 317–364. 

- Peddinti, V., Povey, D., & Khudanpur, S. (2015). A time delay neural network architecture for efficient modeling of long temporal contexts. In _Sixteenth annual conference of the international speech communication association._ 

- Pedersen, M., Agersted, A., & Jønsson, A. (2015). Aspects of adolescence and voice: Girls versus boys–a review. _J Child Adolesc Behav_ , _3_ (211), 2. 

- Povey, D., Ghoshal, A., Boulianne, G., Burget, L., Glembek, O., Goel, N., . . . others (2011). The kaldi speech recognition toolkit. In _Ieee 2011 workshop on automatic speech recognition and understanding._ 

- Prasad, M., van Esch, D., Ritchie, S., & Mortensen, J. F. (2019). Building largevocabulary asr systems for languages without any audio training data. In _Interspeech_ (pp. 271–275). 

- Rabiner, L. R. (1989). A tutorial on hidden markov models and selected applications in speech recognition. _Proceedings of the IEEE_ , _77_ (2), 257–286. 

- Sainburg, T., Thielk, M., & Gentner, T. Q. (2020). Finding, visualizing, and quantifying latent structure across diverse animal vocal repertoires. _PLoS computational biology_ , _16_ (10), e1008228. 

- Salido, J. A. A., Oco, N., Roxas, R., Malaay, E., Simora, M., & Cabatic, R. J. 

98 

(2017). Isolated digit filipino speech recognition through spectrogram image classification: Towards application in a disaster preparedness participatory toolkit. In _2017 international conference on asian language processing (ialp)_ (p. 31-35). doi: 10.1109/IALP.2017.8300539 

- Saon, G., Padmanabhan, M., Gopinath, R., & Chen, S. (2000). Maximum likelihood discriminant feature spaces. In _2000 ieee international conference on acoustics, speech, and signal processing. proceedings (cat. no. 00ch37100)_ (Vol. 2, pp. II1129–II1132). 

- Seltzer, M. L., Yu, D., & Wang, Y. (2013). An investigation of deep neural networks for noise robust speech recognition. In _2013 ieee international conference on acoustics, speech and signal processing_ (pp. 7398–7402). 

- Sheng, P., Yang, Z., & Qian, Y. (2019). Gans for children: A generative data augmentation strategy for children speech recognition. In _2019 ieee automatic speech recognition and understanding workshop (asru)_ (pp. 129–135). 

- Swietojanski, P., Ghoshal, A., & Renals, S. (2013). Revisiting hybrid and gmmhmm system combination techniques. In _2013 ieee international conference on acoustics, speech and signal processing_ (pp. 6744–6748). 

- Tan, T., Lu, Y., Ma, R., Zhu, S., Guo, J., & Qian, Y. (2021). Aispeech-sjtu asr system for the accented english speech recognition challenge. In _Icassp 20212021 ieee international conference on acoustics, speech and signal processing (icassp)_ (pp. 6413–6417). 

- Tong, R., Wang, L., & Ma, B. (2017). Transfer learning for children’s speech recognition. In _2017 international conference on asian language processing (ialp)_ (pp. 36–39). 

- Viikki, O., & Laurila, K. (1998). Cepstral domain segmental feature vector normalization for noise robust speech recognition. _Speech Communication_ , _25_ (1-3), 133–147. 

- Yeung, G., & Alwan, A. (2018). On the difficulties of automatic speech recognition for kindergarten-aged children. _Interspeech 2018_ . 

99 

