## Exploring a Mathematical Model for Classifying Unknown Sensitive Information

### Abstract
In the most abstract form, sensitive information (SensI) consists of two parts- 1: Information which is conventually and widely unknown coupled with 2: a strong desire by current poseser[s] of the information that it remain conventually and widely unknown to a degree they control. We define information which is conventually known as the entirity of Wikipedia; or in other words, if an idea is not found in Wikipedia we would classify it as unknown. We define an idea as the information contained in text between the length of a sentence and a paragraph. If a potentially sensitive new document (NewD) contains a number of ideas that surpasses a predetirmined threshold, we classify it as SensI.

### Introduction
We describe an approach for unsupervised learning for discovering SensI by building a model of of all conventually known information through converting sentences into thoughtVectors that captures the meaning of every sentence on Wikipedia. We then calculate the euclidean distance for thoughts in a NewD to known thoughts with the given loss function.

![alt text](http://i.imgur.com/NtT3KZ8.png)

if the distance is greater than some N to any known thought we conclude it is unknonw.

A second proccess is using a distributed sentence encoder. Using the continuity of text from Wikipedia, we train an encoder-decoder model that tries to reconstruct the surrounding sentences in a NewD with the following loss function.

![alt text](http://i.imgur.com/4QFkssS.png)

Sentences that share semantic and syntactic properties are thus mapped to similar vector representations. If we are unable to meet a certain accuracy level when reconstructing a NewD, we conclude it is unknonw.

#### Examples of SensI:
Personal information, protected health information, student education records, customer record information, card holder data, confidential personal data, financials, blueprints, trade secrets etc.


#### Example nearby ideas

+ he ran his hand inside his coat , double-checking that the unopened letter was still there .
+ he slipped his hand between his coat and his shirt , where the folded copies lay in a brown envelope .

***
+ im sure youll have a glamorous evening , she said , giving an exaggerated wink .
+ im really glad you came to the party tonight , he said , turning to her .

***
+ although she could tell he had n’t been too invested in any of their other chitchat , he seemed genuinely curious about this 
+ although he had n’t been following her career with a microscope , he ’d definitely taken notice of her appearances .

***
+ an annoying buzz started to ring in my ears , becoming louder and louder as my vision began to swim .
+ a weighty pressure landed on my lungs and my vision blurred at the edges , threatening my consciousness altogether .

***
+ if he had a weapon , he could maybe take out their last imp , and then beat up errol and vanessa .
+ if he could ram them from behind , send them sailing over the far side of the levee , he had a chance of stopping them .

***
+ then , with a stroke of luck , they saw the pair head together towards the portaloos .
+ then , from out back of the house , they heard a horse scream probably in answer to a pair of sharp spurs digging deep into 
its flanks .

***
+ “i ’ll take care of it , ” goodman said , taking the phonebook
+ “i ’ll do that , ” julia said , coming in .

***
+ he finished rolling up scrolls and , placing them to one side , began the more urgent task of finding ale and tankards .
+ he righted the table , set the candle on a piece of broken plate , and reached for his flint , steel , and tinder 
