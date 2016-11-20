Sensitive information 

Abstract

In the most abstract form, sensitive information consists of two parts:
1: Information which is conventually and widely unknown coupled with 2: a strong desire by current poseser[s] of the information that said knowledge remain conventually and widely unknown to a degree they control. 

Examples:
Personal information, protected health information, student education records, customer record information, card holder data, confidential personal data, financials, blueprints, trade secrets etc.

We describe an approach for unsupervised learning for document processing convert a sentence into a vector that captures the meaning of the sentence

We describe an approach for unsupervised learning of a generic, distributed sentence encoder. Using the continuity of text from books, we train an encoder-decoder model that tries to reconstruct the surrounding sentences of an encoded passage. Sentences that share semantic and syntactic properties are thus mapped to similar vector representations. We next introduce a simple vocabulary expansion method to encode words that were not seen as part of training, allowing us to expand our vocabulary to a million words. After training our model, we extract and evaluate our vectors with linear models on 8 tasks: semantic relatedness, paraphrase detection, image-sentence ranking, question-type classification and 4 benchmark sentiment and subjectivity datasets. The end result is an off-the-shelf encoder that can produce highly generic sentence representations that are robust and perform well in practice. We will make our encoder publicly available.

"The implications of this for document processing are very important. If we convert a sentence into a vector that captures the meaning of the sentence, then Google can do much better searches; they can search based on what's being said in a document.
	Also, if you can convert each sentence in a document into a vector, then you can take that sequence of vectors and [try to model] natural reasoning. And that was something that old fashioned AI could never do.
	If we can read every English document on the web, and turn each sentence into a thought vector, you've got plenty of data for training a system that can reason like people do. 
	Now, you might not want it to reason like people do, but at least we can see what they would think.
	What I think is going to happen over the next few years is this ability to turn sentences into thought vectors is going to rapidly change the level at which we can understand documents. 
	To understand it at a human level, we're probably going to need human level resources and we have trillions of connections [in our brains], but the biggest networks we have built so far only have billions of connections. So we're a few orders of magnitude off, but I'm sure the hardware people will fix that."
