import requests
from bs4 import BeautifulSoup
from textblob import Word, TextBlob
import re
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
    # (ValueError exceptions are not handled since we don't expect them to happen here)
    data = {
        'scrape': scrape,
        'format': format,
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
    scrapeby = request.GET.get('scrapeby')
    if scrapeby == "sentence": scrapeby = "p"

    # Printing request obtained values
    print("TARGET URL:", targeturl)
    print("USER INPUT:", scrapeby)

    # If "scrape by" value is empty or NoneType...
    r = notEmptyString(scrapeby)
    if r == False: return []
    elif r == -1: return -1
    """
    REASON FOR SPECIAL CASE FOR 'r == -1'
    Sometimes, for requests to certain webpages, I noticed that I am unable to
    get any value for 'scrapeby' that I give in my request URL, getting a NoneType object instead.
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
    (tag, keywordArgs) = getArgs(scrapeby)
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
http://127.0.0.1:8000/alpha/scrape?scrapeby=xyz
...to get response of the user input 'xyz'.
If the attribute is not found, 'None' is returned.
"""
#================================================
# DATA PREPROCESSING 1: FORMATTING
# Simultaneously performs tokenization

# As an intermediate function
def format(request): # Simultaneously performs tokenization
    # Checking for user input...
    data = []
    # If "scrape by" value is not empty
    """
    For 'format', we need user input value to check if
    we need to split scraped data into sentences.
    (If so, scrapeby == "sentence" will be true)
    """
    scrapeby = scrapeByValue(request)
    if scrapeby != False: data = scrape(request)
    else: 
        # If "scrape by" value empty, obtaining data from the scraped dataset
        try: data = readCSV(SCRAPED + ".csv")['value']
        except: return []
    #------------------------
    # Removing punctuations and empty texts
    formattedData = []
    # If we need to split the textual data by sentences...
    if scrapeby=="sentence":
        # Sentence tokenization
        data = sentenceTokenize('. '.join(data))
    # Let's go...
    for x in data:
        # Tokenizing the words in x
        x, row = wordTokenize(x), []
        for word in x:
            # Removing all words starting with non-alphanumeric or non-space characters
            try:
                word.strip() # Removing leading or trailing spaces
                # Appending only non-whitespace words that are not only composed of special characters or numerals
                if len(word) > 1 and re.search(r"[^\W\d]+", word): row.append(word)
                """
                NOTE ON ABOVE CONDITIONS
                --re.search(r"[^\W\d]", word)--
                checks if the word has at least one character that is not a
                special character or a digit (a word should not contain only special characters or numerals).
                This rule helps avoid summarization of citation numbers,
                page numbers, and other miscellaneous symbols and markers.
                """
            except: pass
        # Adding row to the list only if row is non-empty
        if len(row) > 0:
            row = ' '.join(row)
            formattedData.append(row)
    print("Formatting complete!")

    # Saving the formatted data in the CSV file
    saveCSV(FORMATTED, ['index', 'value'], list(enumerate(formattedData)))
    return formattedData

# As an endpoint function
def formatEndpoint(request): return endpoint(request=request, operation='format', returnData=False)
#================================================
# DATA PREPROCESSING 2: CLEANING

# Helper functions...
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

# Main function...
# As an intermediate function
def clean(request):
    # Checking for user input...
    data = []
    # If "scrape by" value is not empty
    if scrapeByValue(request) != False: data = format(request)
    else: 
        # If "scrape by" value empty, obtaining data from the scraped dataset
        try: data = readCSV(FORMATTED + ".csv")['value']
        except: return []
    #------------------------
    # Correcting spelling
    # cleanedData = format(cleanedData)
    #------------------------
    # Removing stopwords
    cleanedData = removeStopwords(data)
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
    # If "scrape by" value is not empty
    if scrapeByValue(request) != False: data = clean(request)
    else: 
        # If "scrape by" value empty, obtaining data from the cleaned dataset
        try: data = readCSV(CLEANED + ".csv")['value']
        except: return []
    #------------------------
    # Tokenizing & simultaneously lemmatizing each review
    normalizedData = []
    # Will contain data fit for summaries
    
    for x in data:
        # Obtaining tokens for the text along with POS tags
        x = TextBlob(x).tags
        
        # POS tags that should be excluded for summary data (using TextBlob POS tags)
        excludedTags = ('PRP', 'PSP$', 'TO', 'IN', 'DT', 'CC', 'MD', 'POS', 'WDT', 'WP', 'WP$', 'WRB', 'CD')
        
        # Lists for containing words of each text
        row = []

        # Iterating through each token
        for word in x:
            lemma = Word(word[0]).lemmatize()
            # Including token lemma into 'normalizedData' only if POS tags are appropriate
            if lemma.isalnum() and word[1] not in excludedTags: row.append(lemma)
        
        normalizedData.append(' '.join(row))
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
    #------------------------
    return normalizedData

# As an endpoint function
def normalizeEndpoint(request): return endpoint(request=request, operation='normalize', returnData=False)
#================================================
# WORD FREQUENCIES (purely intermediate function)
# Needs tokenized texts
# The same request structure as 'scrape'
def wordFreq(request):
    # Checking for user input...
    data = []
    # If "scrape by" value is not empty
    if scrapeByValue(request) != False: data = normalize(request)
    # If no summarizable data available for 'normalize'
    else: 
        # If "scrape by" value empty, obtaining data from the cleaned dataset
        try: data = readCSV(NORMALIZED + ".csv")["value"]
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
    if len(freqDist) == 0: return {}
    return freqDist
#================================================
# SORTED WORD FREQUENCIES (purely intermediate function)
# Needs word frequency dictionary.
# Sorting by descending order of frequency

def sortedWordFreq(request):
    freqDist = wordFreq(request)
    if len(freqDist) == 0: return []
    #------------------------
    # Obtaining words and corresponding frequencies
    keys, values = list(freqDist.keys()), list(freqDist.values())
    # Sorting using merge sort
    mergeSort(keys, values)
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
    # If "scrape by" value is not empty
    if scrapeByValue(request) != False:
        # 'format' produces required data for analysis
        # 'clean' produces required data for normalization
        # 'normalize' produces required data for summarization
        # Hence, we will run 'normalize'...
        """
        This comes in handy when you run 'analyze' before 'summarize',
        but want the same data available for 'summarize' as well.
        It is sufficient to run 'normalize', since it runs 'clean',
        and 'clean' runs 'format'.
        """
        normalize(request)
   
   # No 'else' block, since we will always read from the formatted data file anyways...
    try: data = readCSV(FORMATTED + ".csv")['value']
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
