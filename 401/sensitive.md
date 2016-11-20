## Exploring a Mathematical Model for Classifying Unknown Sensitive Information

### Abstract
In the most abstract form, sensitive information (SensI) consists of two parts- 1: Information which is conventually and widely unknown coupled with 2: a strong desire by current poseser[s] of the information that it remain conventually and widely unknown to a degree they control. We define information which is conventually known as the entirity of Wikipedia; or in other words, if an idea is not found in Wikipedia we would classify it as unknown. We define an idea as the information contained in text between the length of a sentence and a paragraph. If a potentially sensitive new document (NewD) contains a number of ideas that surpasses a predetirmined threshold, we classify it as SensI.

### Introduction
We describe an approach for unsupervised learning for discovering SensI by building a model of of all conventually known information through converting sentences into thoughtVectors that captures the meaning of every sentence on Wikipedia. We then calculate the euclidean distance for thoughts in a NewD to known thoughts with the given loss function.
![alt text](http://i.imgur.com/mMagavR.png)
if the distance is greater than some N to any known thought we conclude it is unknonw.

A second proccess is using a distributed sentence encoder. Using the continuity of text from Wikipedia, we train an encoder-decoder model that tries to reconstruct the surrounding sentences in a NewD. Sentences that share semantic and syntactic properties are thus mapped to similar vector representations. If we are unable to meet a certain accuracy level when reconstructing a NewD, we conclude it is unknonw.

#### Examples of SensI:
Personal information, protected health information, student education records, customer record information, card holder data, confidential personal data, financials, blueprints, trade secrets etc.
