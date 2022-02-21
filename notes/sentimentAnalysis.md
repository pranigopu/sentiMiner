# Sentiment analysis
## Defining the problem
- What is the sentiment behind a text?
- What sentiments are directed towards what aspects?
- How can we obtain the answers to the above through machine learning?

### Elaborating on the terms
#### Sentiment
Sentiment refers to
- Expression of emotion (or lack thereof)
- Expression of approval (or lack thereof)

**_Identifying sentiment without identifying its target_**<br>
Sentiment presupposes a target (i.e. an entity or event) for the sentiment. In other words, sentiment is always sentiment about something. However, natural languages allow for more generalized expressions of sentiment i.e. they allow for the identification of a sentiment without having to specify the target of the sentiment, which does exist, but may exist in any form. In other words, we can identify the sentiment (either approximately or accurately) without having to specify what the sentiment is directed towards.
<br><br>
**_Context and sequence_**<br>
The context in which a linguistic unit is used can play a significant role in determining the linguistic unit's meaning and sentiment. Here, context can be defined as the combination of
- The known circumstances surrounding the linguistic unit
- Other linguistic units neighboring the linguistic unit
- The domain of discussion (ex. subject doubts, hotel reviews, movie critiques...)

Evaluating each unit of the text in appropriate context can be key in determining the meaning and sentiment of the text.
<br><br>
Secondly, the sequence in which linguistic units appear, particularly words, can greatly impact the meaning and sentiment of the given text, particularly in more analytical  languages like English. The sequence can help determine
- Emphases
- Subjects and objects of a sentence
- Topic of a sentences
- Relations between aspects text and modifiers
- Link between entities, events and actions

#### Machine learning
**_General overview_**
Machine learning is a subset of artificial intelligence. Artificial intelligence, in general terms, is a machine's capacity to perform tasks that used to require sentient intelligence. In more precise terms, artificial intelligence is a machine's capacity to reason, discover meaning in data, generalize observations or learn to past experiences .

Machine learning is artificial intelligence that learns from available data, and adapts accordingly. In other words, in machine learning, the machine's behavior does not rely only on programmed instructions, but also on the machine's interpretation of available data. Here, programmed instructions define the machine's approach to interpreting the data, but not the machine's ultimate behavior.

Need for machine learning
1. Computation power
Increasing computation power increases the scalability of an application. Machine learning harnesses the computational power of a computer, allowing for applications that process a much greater quantity of data in much lesser time, compared to human labor. Processing more data is helps in the following:
•	Increasing the probability of find underlying patterns
•	Decreasing the effect of outliers or abnormal data
•	Identifying more variables and classes

Furthermore, being able to process greater quantities of data in much lesser time can help in creating a more useful and usable application.

2. Necessity to adapt to data
Natural language is extremely diverse in terms of concepts and expressions, and varies greatly depending on context. Furthermore, the number of permutations and combinations in which concepts and expressions may appear are practically infinite, and the effects of these permutations and combinations on meaning are often significant.

However, language is based on rules, which may be clearly defined or implicit in usage. Usage of language usually follows discernible patterns that human speakers learn to identify over time, through experience and education. Similarly, in order to interpret natural language texts accurately, using available data to shape a computer's models of natural language meaning seems to be the best approach.

Note that this does not consider the validity of the source of the data. For example, the frontpage of a hotel's website may contain overwhelmingly positive reviews, while online review sections may contain a more diverse range of reviews.

Case specific
Requirement
In our case, we need the machine to interpret texts that are written in English, and thereby determine:
•	The overall underlying sentiment
•	The underlying sentiments with respect to aspects

The broad area of machine learning involved here is natural language processing (NLP), which includes sentiment analysis (our area of focus). The logical, algorithmic and programming approach to sentiment analysis is discussed later.

Elaborating on relevant NLP concepts
Overview
NLP is a subfield of both linguistics and artificial intelligence. It is the study of computational  methods to process, analyze and interpret natural language data. It involves two broad components:
1.	Natural language understanding (NLU)
2.	Natural language generation (NLG)

For this project, the focus will be on NLU, which deals with the computer's reading comprehension i.e. the ability of the computer to gather, structure and analyze the elements of a natural language source. In this project, we will only focus on digital text sources.

NLU approach
Text mining
1. Overview
Text mining or text analytics is the process of transforming unstructured text into a structured, normalized data. Structured data  implies
1.	Standardized format (i.e. format uniformly used for every use case)
2.	Well-defined structure
3.	Accessible to humans and programs

Data normalization is the organization of data into a more logical structure, which involves:
1.	Removing redundancies
2.	Data munging (i.e. transforming the data into a more usable format)
3.	Grouping data according to shared characteristics

2. Purpose
Structuring and normalizing data makes complex processes like machine learning more efficient and effective, since machine learning relies on data quality and accessibility. For example, structuring and normalizing data can help in:
•	Iterating through elements more efficiently (ex. iterating through words)
•	Dealing with necessary data (by removing redundancies)
•	Generalizing a computational method for a standardized format
•	Efficiently accessing necessary metadata (ex. word index, word count)

Dealing with ambiguity
Ambiguity in natural language can appear in the following forms:
1.	Lexical ambiguity (also called semantic ambiguity)
2.	Syntactic ambiguity
3.	Referential ambiguity
Solution approach
Breakdown
The different parts of our solution are covered in the following order:
1.	Data gathering
a.	Identifying appropriate online sources
b.	Web scraping methods
c.	Data storage and usage
2.	Analyzing the overall sentiments for a single text
a.	Text mining
b.	Analyzing sentiment
i.	Conceptual method
ii.	Machine learning algorithm
iii.	Programming
3.	Analyzing aspects for a single text
a.	Text mining
i.	Conceptual method
ii.	Machine learning algorithm
iii.	Programming
4.	Analyzing relationship between aspects and sentiments
5.	Scaling up sentiment analysis
6.	Packaging the application
Domain of focus
For the purpose of simplicity, the sentiment analysis is focused on online reviews of hotels. This domain was chosen because hotels depend on reputation and customer satisfaction, and must aim to understand their customers' needs quickly and carefully, which is why sentiment analysis of hotel reviews is a potentially useful application.

Furthermore, hotels must not only gather the overall sentiments of their customers, but also gather their sentiments regarding the different aspects of hotel services, such as housekeeping, furnishing, amenities, etc., so that they can obtain information they can act upon more precisely.
Data gathering
Overview
Before discussing the methods of analyzing text, we must discuss the methods of acquiring the necessary data. Digital textual data can be available in many forms, such as:
•	Plain text
•	Rich text
•	HTML elements
•	Photographs

Since the focus of our project is on analyzing online hotel reviews, we will be gathering data from websites. Hence, we will focus on gathering data from plain text and HTML elements.
Identifying appropriate online sources
For an online source to be appropriate for our purpose, it needs to be:
•	Directly related to the hotel business
•	Contain a well-defined reviews section
Web scraping methods
Web scraping is the extraction of data from websites, which can be done manually or through a program. Our focus is on creating programs to perform web scraping and automatically detect and retrieve reviews.
Analyzing the overall sentiments for a single text
Overview
Here, we aim to understand the methods through which we can identify:
•	The level of appreciation or disapproval
•	The level of positive or negative emotions
•	The overall tone and mood of the text
Text mining
Before any analysis is performed, we need to obtain the necessary data in an efficient and usable form. Text mining involves the following steps :
1.	Tokenization
2.	Sentence breaking
3.	Part of speech tagging
4.	Chunking
5.	Syntax parsing
6.	Sentence chaining

Tokenization
This divides a text into a collection of individual units (tokens). This is the first step in structuring text data, since tokenization converts a text into a well-defined data structure (such as a list or an array) with each unit accessible through simple iteration.

For our purposes, the tokens are individual words of the text. English follows a regular set of rules defining the division of words, phrases and sentences, making tokenization straightforward. At the most basic level, we can split the text string by whitespace characters.

Sentence breaking
Sentences are independent units of meaning. Relationships between linguistic units, such objects and modifiers, or aspect and sentiment, are mostly contained within sentences. The end of a sentence signals a temporary end of the process of establishing relationships between linguistic units, which helps in finalizing the observed relationships until that point.

End of sentences can be signaled by punctuations such as the period, the exclamation mark or the question mark. But this is not always the case, such punctuations may appear in other contexts.
![image](https://user-images.githubusercontent.com/69959590/155014544-09188f8e-73f2-4fbf-af4c-dde5bf6dff6e.png)
