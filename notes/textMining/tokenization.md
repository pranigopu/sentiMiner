# Tokenization
## References
1. Comparing NLTK and spaCy:<br>
    - https://medium.com/@akankshamalhotra24/introduction-to-libraries-of-nlp-in-python-nltk-vs-spacy-42d7b2f128f2
    - https://www.activestate.com/blog/natural-language-processing-nltk-vs-spacy/

## Definition
Tokenizing of text is the process of breaking a text into tokens (usually individual words). This can be achieved using the built-in Python function **.split**, which partitions the texts based on whitespaces. For more advanced partitioning, we can even use the **split** function from the module **re** (regular expressions handling module). However, instead of bothering ourselves with the exact implementation, we will use available tokenization implementations.

## Choosing a suitable implementation
Python contains two libraries specifically designed for language processing, namely **NLTK**, and **spaCy**. NLTK tokenizer functions take a string (single text) as an input, and returns a processed string (list of sentences or list of words, based on the tokenizer function used). It is a simple method of tokenization that we can easily implement using the .split function or using the regular expressions.
<br><br>
spaCy has a tokenizer class that is optimized for word tokenization. An instance of this tokenizer is a callable object that accepts a string as an argument and returns an object of type Doc (more precisely, spacy.tokens.doc.Doc). This object contains various attributes that are applicable to the tokenized words, including conversion to JSON format and text vectorization (i.e. converting tokenized text into its numerical representation).
<br><br>
Furthermore, spaCy also provides language models that offer powerful features, such as parts-of-speech tagging (i.e. identifying the grammatical role of a word or word sequence in a sentence), noun chunk extraction (i.e. detecting nouns) and named entity recognition (i.e. detecting proper nouns), all of which would lead to easier and more comprehensive language processing.
<br><br>
TensorFlow also offers a tokenizer class that abstracts the exact implementation of tokenization for a whole collection of texts. The main advantage of TensorFlow is that its tokenizer class abstracts the tokenization for an entire collection of texts, and not just a single text, as is the case with the NLTK or spaCy tokenizers. Furthermore, information about these texts and the occurrence of each word in these texts is also stored. Lastly, the TensorFlow tokenizer class stores various informative attributes and methods that facilitate processes such as:
- Looking up the index for a word, and the word for an index
- Encoding texts (facilitated by the above features as well as in-built functions)