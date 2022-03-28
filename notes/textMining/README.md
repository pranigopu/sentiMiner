# Text preprocessing & text mining guidelines
## References
1. Importance of normalization:<br>https://towardsdatascience.com/text-normalization-7ecc8e084e31
2. Definition of language models:<br>https://towardsdatascience.com/the-beginners-guide-to-language-models-aa47165b57f9
3. Stemming vs. lemmatization:<br>https://www.analyticssteps.com/blogs/what-stemming-and-lemmatization-nlp
4. When & when not to stem, lemmatize and remove stopwords:<br>https://opendatagroup.github.io/data%20science/2019/03/21/preprocessing-text.html
5. Stopword removal:<br>https://towardsdatascience.com/sentiment-analysis-with-python-part-2-4f71e7bde59a
6. Why not to remove stopwords:<br>https://medium.com/@limavallantin/why-is-removing-stop-words-not-always-a-good-idea-c8d35bd77214

## Purpose
The goal of text preprocessing is to reduce redundancies in the data, thereby facilitating the deep learning process that uses this data. Redundant or irrelevant data being processed in the machine learning algorithm can affect the speed and accuracy of the learning process, since they are insignificant contributors to the sentiment of the text. Yet, weights of the neural network may be adjusted by traversing these redundant or irrelevant data as inputs to the network, and due to the insignificant contribution of this data to the sentiment, the changes may cause the weights to adjust without causing improvements in the accuracy of the model, potentially even increasing the error of the output.

## Normalization
Normalization is the process of converting a token into its base form, which involves:
- Removing inflections from a word to obtain the root word
- Replacing abbreviations with their actual meaning
- Identify informal intensifiers such as all-caps and character repetitions
- Special tokens such as hashtags, user tags, and URLs are replaced by placeholders

**NOTE**: These placeholders indicate the token type that has been substituted.
<br><br>
Normalization can be extremely useful, since reducing data size (while retaining relevant content) can reduce processing time and space complexity. The goal of normalization is to reduce redundancies in the data, thereby facilitating machine learning that uses this data, since irrelevant data being processed in the machine learning algorithm can affect the speed and accuracy of the process.


### Stemming vs. lemmatization
Normalization can involve **stemming** or **lemmatization**, which are distinct concepts with certain similarities. Stemming works in a more generalized manner, by reducing a word to a root (stem) derived through rule-based removals of parts of a word. Lemmatization works in a more language-specific manner, by reducing a word to an actual root (lemma) derived using language models and dictionaries. In other words, lemmatization applies available vocabulary and morphological analysis of the words.
<br><br>
Lemmatization always gives a valid word while converting to root, while stemming may give roots that are not valid words in the language. Stemming is preferred when the meaning of the word is not important for analysis. Lemmatization would be recommended when the meaning of the word is important for analysis. Since the sentiment being conveyed is highly dependant on the meaning of the words and phrases being used, lemmatization is the prefered method of normalization, although it is more computationally intensive.
<br><br>
### Utility of lemmatization in our project
Lemmatization reduces data complexity (by removing variation in word forms), allowing for easier text categorization. In particular, reducing words to their valid roots is useful in sentiment, aspect, topic categorization.
<br><br>
**NOTE ON LANGUAGE MODEL**<br>
A statistical language model is a probability distribution of words or word sequences. In practice, a language model gives the probability of a certain word sequence being 'valid' in a given context. Note that validity here is not grammatical validity, but validity with respect to the actual usage of language. In other words, it aims to model how people use language.

## Removing stopwords
Stop words are the very common words like 'if', 'but', 'we', 'he', 'she', and 'they'. We can usually remove these words without changing the semantics of a text and doing so often (but not always) improves the performance of a model, since removing stopwords reduces data size and can reduce the processing of irrelevant data. However, sentiment analysis is more sensitive to
- Sequence of words appearance
- Word context

Hence, removing stopwords can hide the effect of the sequence of words preceding a word. Furthermore, removing certain stopwords can change the sentiment underlying the text. For example, if 'don't' is considered a stopword, negatives may be interpreted as positives.

## Conclusions
For preserving the maximum possible meaning of the text while reducing its complexity, we will only perform lemmatization on our texts, without removing stopwords.
