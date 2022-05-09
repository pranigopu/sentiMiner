# SentiMiner
_Text mining & sentiment analysis Chrome extension (prototype)_
## Test repositories for this project
- Test codes and notes for sentiment analysis:<br>https://github.com/pranigopu/exploringSentimentAnalysis

## Other learning repositories
- Learning about text mining:<br>https://github.com/pranigopu/exploringTextMining
- Learning about browser extension:<br>https://github.com/pranigopu/exploringChromeExtensions
- Learning TensorFlow:<br>https://github.com/pranigopu/exploringTensorFlow

## Project aims
Run and view the results of text mining and sentiment analysis functions implemented in a Python backend using a Chrome extension.

## Purpose of each extension script
**Popup script**:<br>
Processes user input, make requests to the background service worker for data, get response, and performs operations on the data to finally present it in the popup page.

**Background service worker**:<br>
Makes requests to the Django-based localhost server and sends the obtained response back to the popup script. Now, note that we can simply use the popup script to send a request to the Django-based localhost server and get back the required response. Practically, taking this approach will not degrade the current performance of the extension. Our reasons for using the background service workers are elaborated in the implementation notes.

## Python backend dependencies
To run the backend properly, make sure that you have installed the following Python packages in your Python environment:

- `django`<br>_Needed for running the backend (the localhost server)_
- `django-cors-headers`<br>_Needed for allow the localhost server to send data in responses to cross-origin requests (in our case, these are requests from the extension) by setting the appropriate CORS headers (discussed further in implementation notes)._
- `textblob`<br>_Needed for lemmatization, POS tagging & sentiment analysis... It depends on the `nltk` package, which should be installed automatically when installing `textblob`_
- `requests`<br>_Needed for making get requests to a URL to obtain the webpage HTML DOM._
- `bs4`<br>_Has **BeautifulSoup**, which is needed to parse the received data from a **get** request as HTML._
- `csv`<br>_Needed for reading from and writing to CSV files._
- `re`<br>_Needed for string pattern identification and processing._

## How to install
- Download the repository (it will be available as a local directory)
- In Google Chrome, go to "chrome://extensions/" and toggle developer mode on (toggle switch at window's top right)
- Select the "Load unpacked" option (button near window's top left)
- Select the "extension" subdirectory from the local repository directory
- In your local system's terminal / command prompt, navigate to the "backend" subdirectory in the local repository directory
- Run the "manage.py" file with the option "runserver", i.e. type and enter<br>`python manage.py runserver`
- In Google Chrome, click the extensions icon in the menu bar and pin this extension (called "Beta")
- Click the button of the pinned extension to view the popup and enter commands

## How to use
The popup of the extension has three input boxes. The first input denotes the HTML element (in lowercase only) that you want to extract from the current webpage's DOM, such as _p_, _div_, _h1_... The second input denotes the particular command you want to perform on the scraped data. The command list is as follows (in lowercase only):

**Testing functions...**<br>

- scrape _(to simply perform scraping and obtain the data as CSV in the subdirectory "backend/data")_
- format _(to simply perform text formatting and obtain the data as CSV in the subdirectory "backend/data")_
- clean _(to simply perform stopword removal and obtain the data as CSV in the subdirectory "backend/data")_
- normalize _(to simply perform text mining and lemmatization and obtain the data as CSV in the subdirectory "backend/data")_

**End-user functions...**<br>

- summarize _(to obtain the word cloud and word frequency bar graph for the normalized data)_
- analyze _(to obtain bipolar sentiment analysis summary and fine grained analysis of sentiment polarities)_<br>_(Note that sentiment analysis is done element by element. For example, if you have scraped paragraphs using **p** in the first input, the sentiment analysis will be done for each paragraph)_

The third input denotes the particular option you want to add to the command. The option list is as follows, for each command that has options:

**summarize**<br>

- wordcloud _(to only obtain word cloud)_
- freqdist _(to only obtain word frequency distribution of top 10 most frequent words)_
- freqdist, n _(where n is an integer, to only obtain word frequency distribution of top n most frequent words)_

**analyze**<br>

- bipolar _(to only obtain bipolar sentiments pie chart (positive, negative and neutral))_
- bipolar, noneutral _(where noneutral is as it is, to only obtain bipolar sentiments pie chart (positive and negative, no neutral))_
- finegrained _(to only obtain finegrained distribution of sentiment polarities within 4 class intervals)_
- finegrained, n _(where n is an integer, to only obtain fine-grained distribution of sentiment polarities within n class intervals)_

## Implementation notes
### Using service worker vs. using popup script
To make the request to the server, we can use any extension script. Using popup script would have been most direct, since messaging would not be necessary, and we can directly show the response in the popup page. However, the background service worker is used for the following reasons...

- Abstraction between presentation layer (popup script) and application layer
- Background service worker only unloads when unused (hence, after it has completed its processes), while popup script unloads when the popup page is closed. In the current implementation of the project, this is not an issue. But to allow for functionalities that may happen independently the popup page, such as
    - Downloading results from analysis
    - Perform analysis (which could be time consuming) and store the results in a database to be retrieved when desired

Admittedly, for our project as it is currently, it was not practically necessary to use a background service worker, but we have done so due to the above points.

### Word cloud script
The JavaScript code for word cloud was taken from the 'wordcloud' library:

- https://www.npmjs.com/package/wordcloud

I have modified the installed package (in the "extension" directory in the repository), removing all the files I deemed unnecessary and renaming the package directory to simply 'wordcloud'.

#### Accessing through popup script
To access the 'WordCloud' function from 'wordcloud2.js' using the popup script, I simply include the script in 'popup.html' before the popup script. The required canvas element must be created in the popup page's DOM, either dynamically or in the HTML document itself.

#### Accessing through content script (unused)
_(And why this approach was abandoned)_ <br><br>
To access the 'WordCloud' function from 'wordcloud2.js' using the content script, I simply added the relative path to 'wordcloud2.js' in the "content_scripts" field of the 'manifest.json' file. Accessing the word cloud functionalities in the content script was necessary to create and insert a canvas object with the word cloud within the current webpage's DOM (since the current webpage is not stored locally in the extension's directory, we cannot simply add a script tag with a reference to 'wordcloud2.js' using the relative path).
<br><br>
This approach to a user interface was abandoned due to the following reasons:

- Even if we insert the canvas at the beginning of the current webpage, and even if we do it within a division (div) tag, the result may not appear as desired for every webpage as desired, due to the possible particular features applied for the webpage. For example, when trying to insert the canvas at the beginning of a Wikipedia page's body, the word cloud display always clashed with the Wikipedia logo at the top left of the page. We could fine-tune our code for Wikipedia, but there is no guarantee that such issues will not happen for some other websites.
- As a user, it may be more convenient to have the results always readily accessible in the popup page, and not at the very top of the webpage's body. This inconvenience may occur if the user wishes to scroll around the webpage or go to other tabs but still wishes to have the results easily accessible through the extension's button (that would open the popup page).<br>_(The issue with a popup page, however, is that a popup page and its script are only loaded when the popup page is opened, and the dynamic results on the page are not persistent...)_
- To display the results in the current webpage's DOM, anu open webpage had to be reloaded whenever the extension was reloaded in developer mode. This issue is not going to occur for the end-user of course, since the end-user is not supposed to want to (or be able to) reload the extension as a developer. But this is a minor developer hassle that added to our other woes.

### Graph and chart script
The JavaScript code for charts, and in particular, for the bar and pie charts used in the extension, was taken from the 'Chart.js' library:

- https://www.chartjs.org/docs/latest/getting-started/installation.html

I have modified the installed package (in the "extension" directory in the repository), removing all the files I deemed unnecessary and renaming the package directory to simply 'chart'.

#### Accessing through popup script
To access and instantiate the 'Chart' class from 'chart.js' using the popup script, I simply include the script in 'popup.html' before the popup script. The required canvas element must be created in the popup page's DOM, either dynamically or in the HTML document itself.

#### NOTE ON THE Chart.js library AND REUSING CANVAS ELEMENT
    
Unlike the word cloud function we used, we cannot simply add the new chart to the same canvas element if we had already added an instance to it. This is because the canvas element for which the chart object was created acts as a unique key for the chart object, hence preventing other chart objects from using the same key i.e. canvas element. Applying `.destroy` to a chart object destroys a created chart instance. This will clean up any references stored in the chart object, along with any associated event listeners attached to the JavaScript code by the 'Chart.js' library. This must be called before the canvas is reused for a new chart.
<br><br>
To obtain the previous chart object created for the given canvas element, we shall use the function 'getChart' defined in the 'chart.js' module, called as

```
Chart.getChart(key)
```

Here, `key` refers to the canvas element. It can be any one of the following:

- String denoting the ID of the canvas element
- HTML DOM element object _(HTMLElement)_
- CanvasRenderingContext2D object
    
##### REFERENCES
- https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas

### Cross origin request from extension to localhost server
To prevent leaks of sensitive information, webpages are generally not allowed to fetch cross-origin data. Unless a valid CORS header is present on the response, the page's request will fail with an error like the one above.
<br><br>
A valid CORS header in this case would indicate that the requested resource (in whose response the header would be present) (ex. a server host or website) allows requests from other origins (ex. other server hosts or websites) to access its resources (ex. response data)

#### Reiteration of key point and side notes
Just to emphasise the point, the extension package and Django-based backend are stored in and run from different domains, hence a request from the extension scripts to the server web application's service is a cross-origin request.
<br><br>
To allow the cross-origin request (from the extension's scripts) to access the requested resource (i.e. the localhost server's web application's service), the server host (my computer's local IP address) must add the appropriate header to its responses, so that there is no issue according to the CORS policy.

#### Solution details
To handle CORS headers in Python, we installed the `django-cors-headers` package. In the Django-based website's configurations directory (i.e. backend/backend), in the 'settings.py' file, we did the following:

- Added `corsheaders` in the `INSTALLED_APPS` list
- Added `corsheaders.middleware.CorsMiddleware` in the `MIDDLEWARE` list
- To allow any possible host (for my website) to add the valid CORS header to the website's responses, I did the following (within the 'settings.py' file)

```
ALLOWED_HOSTS=['*']
CORS_ORIGIN_ALLOW_ALL = True
```

#### REFERENCES
- https://www.chromium.org/Home/chromium-security/extension-content-script-fetches/
- https://dzone.com/articles/how-to-fix-django-cors-error

### Word and sentence tokenization
We were using 'nltk.word_tokenize' from the 'nltk' library to tokenize words since it efficiently removes punctuations appearing next to words (ex. commas, quotes, colons), and includes these punctuations as separate items. This is not achieved when using .split() alone, or using regular expressions alone. However, to reduce the dependencies for this code, we have created a function to achieve what 'nltk.word_tokenize' achieves.
<br><br>
For a similar reason, we were using 'nltk.sent_tokenize' from the nltk library to split a paragraphs into sentences (if splitBySentence == True). However, to reduce the dependencies for this code, we have created a function to achieve what 'nltk.sent_tokenize' achieves.
<br><br>
Now note that when we say "reduce dependencies", we don't mean remove the dependency on NLTK, since the TextBlob package depends on NLTK. However, "reduce dependencies" does mean that nothing extra will need to be downloaded or installed from the broader NLTK library, such as the `punkt` module, which contains the word and sentence tokenizing functions.

### Data formatting and cleaning
#### Process flow
The data formatting and cleaning functions were intended to be executed in the same order as they are defined in the code. 'clean' is the function that calls 'format' 'spellCheck' and 'removeStopwords', though 'format' can be a standalone endpoint function as well.
The intended order of the operations is:

- Formatting
- Spell checking
- Stopword removal

(Spell checking may be omitted)

#### Reason for separation into functions
The preprocessing operations were separated into different functions to make the programming and testing process easier. This makes

- Individual testing easier
- Modification of 'clean' function easier

For example, if the spell-checking operations are taking too long and are not that essential to include, I can easily comment the 'spellCheck' function call and modify the 'clean' function accordingly.

#### Note on the difference in formatting and cleaning
Formatted data is better for sentiment analysis, since key stopwords such as 'not', 'don't', etc. are not omitted, and hence the full underlying sentiment is preserved.
<br><br>
Formatted data after stopword removal is better for summarizing, since stopwords are omitted, and only the words more indicative of the contents of the text are retained.
