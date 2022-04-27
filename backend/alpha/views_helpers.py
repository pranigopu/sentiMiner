# CHECKING IF USER INPUT IS PRESENT
# For general strings
def notEmptyString(s):
    if s == '' or str(s).isspace(): return False
    elif s == None: return -1
    """
    REASON FOR SPECIAL CASE FOR 's == None'
    Sometimes, for requests to certain webpages, I noticed that I am unable to
    get any value for 'userinput' that I give in my request URL, getting a NoneType object instead.
    I am not sure why this issue occurs for certain webpages.
    For now, I want to give a special message to indicate this.
    Hence, the special case.
    """
    return True
# For requests
def userInputPresent(request):
    userinput = request.GET.get('userinput')
    return notEmptyString(userinput)
#================================================
# SAVING AS CSV
import csv
import string
def saveCSV(fileName, headers, rows):
    # Saving as CSV file
    file = open(fileName + ".csv", 'w', encoding='UTF8')
    myWriter = csv.writer(file)
    # Giving header row
    myWriter.writerow(headers)
    # Giving texts
    myWriter.writerows(rows)
#================================================
# RESPONSE MAKER
from django.http import JsonResponse
def sendResponse(operationName, hasSucceeded, data):
    #------------------------
    # If operation has succeeded
    if hasSucceeded == True:
        report = operationName.title() + ' successful!'
        # .title converts process name to title case i.e. only first letter capitalised
    #------------------------
    # If operation has failed
    elif hasSucceeded == False:
        report = {
            'scrape': 'No matches found!',
            'clean': 'Empty result!',
            'normalize': 'Empty result!',
            'summarize': 'Empty result!',
            'analyze': 'No data to analyze!'
        }[operationName]
        # Each operation can have a different error message.
        # We assume that operation name is given correctly.
        # Hence, we don't have exception handling for ValueError.
   #------------------------
   # Special case
    else:
        # Special report message case
        report = hasSucceeded
    return JsonResponse({
        'operation': operationName,
        'report': report,
        'data': data})
#================================================
# FOR PYTHON WEB SCRAPER
def getArgs(userinput):
    # Extracting desired tag, ID and class from the input
    """
    NOTE ON USER INPUT INTENDED FORMAT
    By design, user input can be a comma separated value in the format
    id>..., class>..., tag>...
    
    Not all the above options are necessary to add, and by default,
    the input is taken as 'tag'.
    """
    options = ['id', 'class']
    # Keyword arguments (if any) for the coming 'find_all' function
    tag, keywordArgs = '', {}

    userinput = userinput.split(',')
    for u in userinput:
        # Trimming the input (i.e. removing leading and trailing spaces)
        u = u.strip()
        flag = 0
        for o in options:
            try:
                """
                Checking if the start of the input indicates any option, example
                - id> (hence we need to check first 3=2+1 elements)
                - class> (hence we need to check first 6=5+1 elements)

                TO COMPARE
                Hence, to slice the string appropriately, we need to have the range
                0 to length of option + 1
                since length of option must be the last included index
                (as it includes the '>' as well), and
                upper bound index is excluded in Python slicing.

                TO ADD VALUE TO DICTIONARY
                Hence, the value of the ID or class is in the range
                length of option + 1 (excluding the '>') to maximum index
                """
                if o+'>' == u[:len(o)+1]:
                    keywordArgs[o] = u[len(o)+1:]
                    break
            except: pass

            # Flag within the expect block won't update outside the block.
            flag = flag + 1
        
        # If no specifier, then consider as tag (1st non-keyword argument in 'find_all')
        if flag >= len(options):
                tag = u
    return (tag, keywordArgs)

    """
    NOTE ON RETURN VALUE
    The return value must serve as arguments for 'find_all',
    an attribute function of BeautifulSoup objects.

    'find_all' has 1 optional non-keyword argument (for tag), and
    multiple optional keyword arguments (for ID and class).
    We can pack the keyword arguments in a dictionary as
    **keywordArgs
    """
#================================================
# ABBREVIATION DECONTRACTION FOR WHOLE PHRASE
import re
def decontracted(phrase):
    phrase = phrase.lower()

    phrase = re.sub(r"\'re", " are", phrase)
    
    # Expanding irregular shortened negatives
    # Can't
    phrase = re.sub(r"can\'t", "cannot", phrase)
    phrase = re.sub(r"can\st[\.\,\s]+", "cannot", phrase)
    # Won't
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"won\st[\.\,\s]+", "will not ", phrase)
    # Shan't
    phrase = re.sub(r"shan\'t", "shall not", phrase)
    phrase = re.sub(r"shan\st[\.\,\s]+", "shall not ", phrase)
    """
    NOTES:
    I think "won't" and "shan't" i.e. "will not" and "shall not"
    can be safely replaced by "not" without losing much meaning.
    """
    
    # Expanding regular shortened negatives
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"n\st[\.\,\s]+", " not ", phrase)
    
    # Other shortened forms
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    """
    NOTES:
    I think "will" can be safely removed without losing much meaning.
    """
    return phrase
"""
NOTE ON SPACING FOR SHORTENED NEGATIVES
For the second patterns, since you are also checking for potential spaces, periods or commas
after n\st, you will also be replacing spaces. Hence, make sure you have
spaces in the substitute text.

WHY THE SECOND PATTERNS FOR SHORTENED NEGATIVES?
When tokenizing, the Python code treats the
directed inverted quotes as whitespace characters.
Hence, "aren’t" would be tokenized into 'are' and 't'.
Hence, when the data is cleaned, "aren’t" will become "aren t".
To account for such issues, I have included a second pattern for each abbreviation.

Note that directed inverted quote are often found in online documents,
as opposed to the directionless quote that is common in code.

NOTE ON SINGLE QUOTES:
The character U+2019 "’" could be confused with
the character U+0060 "`", which is more common in source code.
"""
#================================================
# MERGE SORT WITH LABELS (descending order)
# Thanks to: https://www.geeksforgeeks.org/merge-sort/
def mergeSort(x, y):
    # x denotes labels i.e. keys
    # y denotes values
    # NOTE: y will be sorted, x will be changed correspondingly
    
    # If more than one element, split into two and perform merge sort on each subtree
    if len(y) > 1:
        mid = len(y) // 2
        # Dividing into left and right subtrees
        Lx, Ly = x[:mid], y[:mid]
        Rx, Ry = x[mid:], y[mid:]
        # Applying merge sort for each subtree
        mergeSort(Lx, Ly)
        mergeSort(Rx, Ry)
        # Merging into descending order
        i = j = k = 0
        while i < len(Ly) and j < len(Ry):
            if Ly[i] > Ry[j]: x[k], y[k], i = Lx[i], Ly[i], i+1
            else: x[k], y[k], j = Rx[j], Ry[j], j + 1
            k += 1
        # If an element was left out in left subtree
        while i < len(Ly): x[k], y[k], i, k = Lx[i], Ly[i], i+1, k+1
        # If an element were left out in left subtree
        while j < len(Ry): x[k], y[k], j, k = Rx[j], Ry[j], j+1, k+1
        """
        NOTE ON ELEMENTS LEFT AFTER 1ST WHILE LOOP
        Due to the way the elements are added in the first while loop,
        elements will be left out either in the left subtree or in the
        right subtree, but never in both.
        """

"""
NOTE ON MERGE SORT
At the last nested call of 'mergeSort' with x and y lengths being more than one,
the function handles subtrees having either 1 or 0 elements.
This means the previous call will handle subtrees having either 2 or 1 elements.
On the whole, this means individual subtrees will be properly sorted.
Hence, suppose we add all the elements of one subtree in the 1st loop,
even if we add all the remaining elements of the other subtree in the 2nd or 3rd
loop, the sorting order will be achieved.
"""