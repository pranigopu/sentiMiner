import requests
from bs4 import BeautifulSoup
from textblob import Word, TextBlob
import pandas as pd
import nltk
import re
#================================================
# MAINTENANCE CODE
# Ensuring the required NLTK modules are downloaded and are up-to-date
nltk.download('punkt')
#================================================
# Create your views here.
from .views_globals import * # Global variables and objects
from .views_helpers import * # Helper functions I created
#================================================
# ENDPOINT FUNCTION MAKER (helper function)
# For wrapping intermediate functions as endpoint functions
"""
Though it is a helper function, it is put here since
it needs to access functions defined here.
"""
def endpoint(*, request, operation, returnData=True, specialCase=None):
    # request is a URL 'request' object
    # operation is a string
    # returnData is Boolean, by default True
    # specialCase is by default None. Otherwise, it must be a list with
    # - first element being the special case value
    # - second element being the special case report

    data, report = [], True

    # Obtaining data from the appropriate function
    # (We don't ValueError exceptions since we don't expect them to happen in this context)
    data = {
        'scrape': scrape,
        'clean': clean,
        'normalize': normalize,
        'summarize': summarize,
        'analyze': analyze
    }[operation](request)

    # Special case
    if specialCase != None and data == specialCase[0]: report = specialCase[1]
    # Fail case
    elif len(data) == 0: report = False
    # (Success case report value is default)

    """
    DO WE ALWAYS WANT RETURN DATA?
    For functions like scrape, clean and normalize, we don't want
    any data returned, since their data is unused by the Chrome extension.
    Furthermore, their data can be quite large, so we don't want to
    needlessly bog the computation process.

    To specify that the response data should be empty,
    we give 'returnData = False' when calling the function.
    Note that we make the data an empty list ONLY after
    - Calling the function and obtaining its returned data
    - Checking for data length in the conditions above
    """
    if returnData == False: data = []
    return sendResponse(operation, report, data)
    # (using 'sendResponse' from .views_helpers)
#================================================
# PYTHON WEB SCRAPER (endpoint function)
# As an intermediate function
def scrape(request):
    # READING REQUEST
    # Target URL
    targeturl = request.GET.get('targeturl')
    # User input
    userinput = request.GET.get('userinput')

    # Printing request obtained values
    print("TARGET URL:", targeturl)
    print("USER INPUT:", userinput)

    # If user input is empty or NoneType...
    r = notEmptyString(userinput)
    if r == False: return []
    elif r == -1: return -1
    """
    REASON FOR SPECIAL CASE FOR 'r == -1'
    Sometimes, for requests to certain webpages, I noticed that I am unable to
    get any value for 'userinput' that I give in my request URL, getting a NoneType object instead.
    I am not sure why this issue occurs for certain webpages.
    For now, I want to give a special message to indicate this.
    Hence, the special case.
    """
    #------------------------
    # GETTING DOM CONTENTS FROM URL
    try: html = requests.get(targeturl, timeout=10)
    except: return []
    """
    If the requested resource does not respond, the 'requests.get' call
    will never terminate. To avoid this, we set a timeout (here, 10 seconds).
    """
    element = BeautifulSoup(html.content, 'html.parser')
    #------------------------
    # OBTAINING RESULTS
    """
    ABOUT 'find_all'
    'find_all' has 1 optional non-keyword argument (for tag), and
    multiple optional keyword arguments (for ID and class).
    We can pack the keyword arguments in a dictionary as
    **keywordArgs
    (keywordArgs is a previously made dictionary)

    NOTE:
    If the non-keyword argument is '', the results will not return anything,
    since no matches would be found. Hence, we have the below if-else condition...
    """
    # Getting the arguments for the 'find_all' function
    (tag, keywordArgs) = getArgs(userinput)
    # 'getArgs' from the .viewsHelpers module

    # Getting the results
    results = []
    if tag == '': results = element.find_all(**keywordArgs)
    else: results = element.find_all(tag, **keywordArgs)
    print("Scraping complete!")

    # Extracting individual texts
    scrapedData = []
    for x in results:
        try: scrapedData.append(x.text)
        except: continue
    #------------------------
    if len(scrapedData) > 0:
        # Saving as CSV only if scraping results were non-empty
        # (using 'saveCSV' from .views_helpers)
        saveCSV(SCRAPED, ['index', 'value'], list(enumerate(scrapedData)))
    #------------------------
    return scrapedData

# As an endpoint function
def scrapeEndpoint(request):
    return endpoint(
        request = request,
        operation = 'scrape',
        returnData = False,
        specialCase = [-1, "User input was inaccessible for request to this website!"])
"""
NOTE ON ATTRIBUTES OF A REQUEST
'request' objects may contain additional attributes.
These are specified in the URL using the following formal:
<base url>?attribute=value

Or for multiple attributes:
<base url>?attribute1=value1&attribute2=value2...

For the above 'scrape' function, we need to provide:
http://127.0.0.1:8000/alpha/name?name=xyz
...to get response of the name 'xyz'.
If the attribute is not found, 'None' is returned.
"""
#================================================
# DATA CLEANING
# Simultaneously performs tokenization
"""
PROCESS FLOW
The following functions were intended to be executed in the same order as they are defined here.
'clean' is the function that calls 'format', 'spellCheck' and 'removeStopwords'.
The intended order of the operations is:
- Formatting
- Spell checking
- Stopword removal

(Spell checking may be omitted)
____________
REASON FOR SEPARATION INTO FUNCTIONS
The preprocessing operations were separated into different functions to make the programming and testing process
easier. This makes
- Individual testing easier
- Modification of 'clean' function easier

For example, if the spell-checking operations are taking too long and are not that essential to include,
I can easily comment the 'spellCheck' function call and modify the 'clean' function accordingly.
"""
def format(data): # Simultaneously performs tokenization
    """
    We are using 'nltk.word_tokenize' from the 'nltk' library
    since it efficiently removes punctuations appearing next to words
    ex. commas, quotes, colons. This is not achieved when using .split() alone.
    """
    # Removing punctuations and empty texts
    formattedData = []
    for x in data:
        x, row = nltk.word_tokenize(x), []
        for word in x:
            # Removing all words starting with non-alphanumeric or non-space characters
            try:
                word.strip() # Removing leading or trailing spaces
                # Only appending non-whitespace words not beginning with special characters or numbers.
                if not re.match(r"[^\w\s]|\d", word): row.append(word)
            except: pass
        # Adding row to the list only if row is non-empty
        if len(row) > 0:
            formattedData.append(' '.join(row))
    print("Formatting complete!")

    # Saving the formatted data in the CSV file (only for my own reference while testing)
    saveCSV(CLEANED + "-formatted", ['index', 'value'], list(enumerate(formattedData)))
    return formattedData
def spellCheck(data):
    # Correcting spelling
    spellCheckedData = []
    for x in data:
        x, row = x.split(' '), []
        for word in x:
            row.append(str(TextBlob(word).correct()))
        spellCheckedData.append(' '.join(row))
    print("Spelling correction complete!")

    # Saving the spell-checked data in the CSV file (only for my own reference while testing)
    saveCSV(CLEANED + "-spellchecked", ['index', 'value'], list(enumerate(spellCheckedData)))
    return spellCheckedData
def removeStopwords(data):
    # Removing stopwords
    """
    NOTE ON REMOVING STOPWORDS
    When training a sentiment analysis model , we must be careful not to remove words that are important in giving
    context, such as 'not'. However, in our case, cleaning and normalization is done for summarization purposes, not
    for training any model. Hence, we can remove words such as 'not', 'don't' and other such words that are necessary
    for context but not for summary.
    """
    stopwords = open("data/stopwords.txt", "r").read().split(",")
    noStopwordsData = []
    for x in data:
        processedText = ' '.join([word for word in decontracted(x).split(' ') if word.lower() not in stopwords])
        # ('decontracted' from .views_helper)
        # ('stopwords' set from .views_globals)
        if len(processedText) > 0:
            noStopwordsData.append(processedText)
    print("Stopword removal complete!")
    # No data saved here, since this is the last step in the cleaning process.
    return noStopwordsData

# As an intermediate function
def clean(request):
    # Checking for user input...
    data = []
    # If user input is not empty
    if userInputPresent(request) == True: data = scrape(request)
    else: 
        # If user input empty, obtaining data from the scraped dataset
        try: data = pd.read_csv(SCRAPED + ".csv")['value']
        except: return []
    #------------------------
    # Removing punctuations + Converting to lowercase
    cleanedData = format(data)
    #------------------------
    # Correcting spelling
    # cleanedData = format(cleanedData)
    #------------------------
    # Removing stopwords
    cleanedData = removeStopwords(cleanedData)
    #------------------------
    # Saving if non-empty
    if len(cleanedData) > 0:
        # Saving as CSV only if scraping results were non-empty
        # (using 'saveCSV' from .views_helpers)
        saveCSV(CLEANED, ['index', 'value'], list(enumerate(cleanedData)))
    #------------------------
    return cleanedData

# As an endpoint function
def cleanEndpoint(request): return endpoint(request=request, operation='clean', returnData=False)
#================================================
# TOKENIZATION + LEMMATIZATION USING SPACY
# Main focus is on lemmatization
# We will use the cleaned data we have obtained for efficiency
"""
NOTE ON USAGE OF SPACY VS. NLTK
I tried NLTK lemmatizer, it was not as effective.
Hence, I decided to use spaCy, which gave the best results
for lemmatization, but was sometimes overly aggressive.
Furthermore, I wanted to reduce the dependencies for this code,
and spaCy's usage was both very limited and easily replaceable using other imported modules.
Hence, I settled for the package 'textblob', which gave more satisfactory results than NLTK
through the module "Word".
"""
# As an intermediate function
def normalize(request):
    # Checking for user input...
    data = []
    # If user input is not empty
    if userInputPresent(request) == True: data = clean(request)
    else: 
        # If user input empty, obtaining data from the cleaned dataset
        try: data = pd.read_csv(CLEANED + ".csv")['value']
        except: return []
    #------------------------
    # Tokenizing & simultaneously lemmatizing each review
    normalizedData, summarizableData = [], []
    # normalizedData: contains data fit for sentiment analysis
    # summarizableData: contains data fit for summaries
    
    for x in data:
        # Obtaining tokens for the text
        x, row_normalized, row_summarizable = nltk.pos_tag(nltk.word_tokenize(x)), [], []
        """
        nltk.pos_tag accepts a list of strings (words), and returns the POS tags for each string (word) in the form
        [
            (<string 1>, <POS tag 1>),
            (<string 2>, <POS tag 2>)
            ...
        ]
        """
        
        # POS tags that should be excluded for summary data (using NLTK POS tags)
        excludedTags = ('PRP', 'IN', 'DT', 'CC', 'MOD', 'POS', 'WDT', 'WP', 'WP$', 'WRB', 'CD')
        
        # Iterating through each token
        for word in x:
            lemma = Word(word[0]).lemmatize()
            # Including token lemma into 'normalizedData'
            row_normalized.append(lemma)
            # Including token lemma into 'summarizableData' only if POS tags are appropriate
            if word[1] not in excludedTags: row_summarizable.append(lemma)
        
        normalizedData.append(' '.join(row_normalized))
        summarizableData.append(' '.join(row_summarizable))
    """
    NOTE ON MAKING RESULTS AS PROPER STRINGS
    For the normalized data, I am saving the results as proper, whole strings.
    This is because the normalization of data is the text mining process,
    so I want this data to be easily accessible by other functions.
    Storing the texts as proper strings make them easier to split and covert to a list.
    
    NOTE ON POSSIBLE STOPWORD REMOVING WITH LEMMATIZATION
    Note that the English language model we have instantiated (we named it 'nlp')
    performs parts-of-speech analysis along with lemmatization.
    Since most pronouns, prepositions and conjunctions can be considered stopwrds,
    we could be selective of the words added to our 'normalizedData' list based on their POS tag,
    given by each token's 'pos_' attribute, which can be accessed using 'word.pos_'.
    ___
    However, stopword removal before lemmatization reduces the computational load greatly,
    hence increasing performance, since POS tagging is more computationally intensive task than stopword removal.
    Of course, by default, POS tagging is always performed. But by removing stopwords beforehand,
    POS tagging is done on fewer words, hence improving performance.
    """
    print("Normalization complete!")
    #------------------------
    # Saving if non-empty
    if len(normalizedData) > 0:
        # Saving as CSV only if scraping results were non-empty
        # (using 'saveCSV' from .views_helpers)
        saveCSV(NORMALIZED, ['index', 'value'], list(enumerate(normalizedData)))
    if len(summarizableData) > 0:
        # Saving as CSV only if scraping results were non-empty
        # (using 'saveCSV' from .views_helpers)
        saveCSV(SUMMARIZABLE, ['index', 'value'], list(enumerate(summarizableData)))
    #------------------------
    return {'normalized': normalizedData, 'summarizable': summarizableData}

# As an endpoint function
def normalizeEndpoint(request): return endpoint(request=request, operation='normalize', returnData=False)
#================================================
# WORD FREQUENCIES (purely intermediate function)
# Needs tokenized texts
# The same request structure as 'scrape'
def wordFreq(request):
    # Checking for user input...
    data = []
    # If user input is not empty
    if userInputPresent(request) == True: data = normalize(request)['summarizable']
    # If no summarizable data available for 'normalize'
    else: 
        # If user input empty, obtaining data from the cleaned dataset
        try: data = pd.read_csv(SUMMARIZABLE + ".csv")['value']
        except: return {}
    #------------------------
    freqDist = {}
    for x in data:
        x = x.split(' ')
        for w in x:
            try: freqDist[w] = freqDist[w] + 1
            except: freqDist[w] = 1
    
    """
    For the functions I am using, a dictionary is not very helpful.
    I used a dictionary above since it is the most efficient
    data structure for updating word-frequency pairs.
    """
    if len(freqDist) == 0: return {"No response!": 0.25}
    return freqDist
#================================================
# SORTED WORD FREQUENCIES (purely intermediate function)
# Needs word frequency dictionary.
# Sorting by descending order of frequency
def sortedWordFreq(request):
    freqDist = wordFreq(request)
    if len(freqDist) == 0: return []
    #------------------------
    keys, values = list(freqDist.keys()), list(freqDist.values())
    upper = len(values)
    # Sorting using insertion sort
    for i in range(0, upper):
        k, switchAt = values[i], -1
        for j in range(i - 1, -1, -1):
            # Keep looping back until we reach index 0 or until we find a value greater than the maximum.
            if values[j] > k:
                switchAt = j + 1
                break
        # Swapping
        if switchAt > -1:
            tmp1, tmp2 = values[i], keys[i]
            values[i], keys[i] = values[switchAt], keys[switchAt]
            values[switchAt], keys[switchAt] = tmp1, tmp2
    #------------------------
    # Packing the lists as necessary for the wordcloud function in the extension scripts
    res = list(zip(keys, values))
    return res
#================================================
# DATA SUMMARY
# Only created for abstraction of summarization process.
def summarize(request):
    data = sortedWordFreq(request)
    return data
def summarizeEndpoint(request): return endpoint(request=request, operation='summarize')
#================================================
# SENTIMENT ANALYSIS (intermediate function)
# Needs cleaned data.
"""
The TextBlob class from the 'textblob' package has a pre-trained
polarity-based sentiment analysis model. We will be using this.
"""
def analyze(request):
    # Checking for user input...
    data = []
    # If user input is not empty
    if userInputPresent(request) == True: data = clean(request)
    else: 
        # If user input empty, obtaining data from the tokenized dataset
        try: data = pd.read_csv(CLEANED + ".csv")['value']
        except: return []
    #------------------------
    sentiments = []
    for x in data:
        sentiments.append(TextBlob(x).sentiment[0])
    print("Analysis complete!")
    #------------------------
    # Saving if non-empty
    if len(data) > 0:
        # Saving as CSV only if scraping results were non-empty
        # (using 'saveCSV' from .views_helpers)
        indices = list(range(0, len(data)))
        saveCSV(ANALYZED, ['index', 'value', 'sentiment'], list(zip(indices, data, sentiments)))
    else: return []
    #------------------------
    return list(zip(data, sentiments))

# As an endpoint function
def analyzeEndpoint(request): return endpoint(request=request, operation='analyze')