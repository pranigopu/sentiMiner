# Stemming
## References
1. Intro to stemming:<br>https://www.geeksforgeeks.org/python-stemming-words-with-nltk/
2. Under-stemming & over-stemming<br>https://towardsdatascience.com/stemming-of-words-in-natural-language-processing-what-is-it-41a33e8996e2

## Definition & stemming algorithms
Stemming is the process of substituting a word for its root word i.e. stem. For example, a stemming algorithm reduces the words 'running', 'ran' and 'run' to the stem, 'run', and the words 'retrieval', 'retrieved', 'retrieves' to the stem 'retrieve'. There are many available stemming algorithms (also called stemmers), each with its own advantages and disadvantages, such as:
- Porter stemmer
- Lovins stemmer
- Dawson stemmer
- N-gram stemmer
- Snowball stemmer

## Potential issues
Over-stemming is when a word is reduced more than appropriate, which leads to two or more words being reduced to the same root word or stem (incorrectly) when they should have been reduced to two or more stem words. For example, 'university' and 'universe' are supposed to be considered as different roots, since their meanings are significantly distinct.
<br><br>
Under-stemming is when two or more words are wrongly reduced to more than one root word, when they actually stem from the same root word. For example, 'data' and 'datum' stem from 'dat', but some algorithms may reduce these words to 'dat' and 'datu' respectively, which is wrong. Both of these have to be reduced to the same stem 'dat'. However, note that trying to optimize such models might lead to over-stemming.

## Choosing the right stemming algorithm
Some stemmers are more applicable for a particular language (ex. Porter stemmer was designed for English), while others are designed to be applicable for any language, even when it is unknown (ex. snowball stemmer). Since our application was only intended for English language text sources, and since sentiment analysis techniques we are using are designed only for English language texts, we will use stemmers designed for English.
<br><br>
Furthermore, the expression of sentiment can be quite complex and subtle, and having an excess of words is preferable to not having key words that could potentially affect the sentiment significantly. Hence, for analysing sentiment, under-stemming is preferable to over-stemming. Keeping this in mind, we shall use a less aggressive stemmer, such as Porter stemmer.
<br><br>
A Python implementation of Porter stemmer is available in the 'stem' module of the 'nltk' library.
