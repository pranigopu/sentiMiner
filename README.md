# Text mining & sentiment analysis extension prototype
## Personal learning and testing repositories for this project
- Learning about text mining:<br>https://github.com/pranigopu/exploringTextMining
- Learning about sentiment analysis:<br>https://github.com/pranigopu/exploringSentimentAnalysis
- Learning about browser extension:<br>https://github.com/pranigopu/exploringChromeExtensions
- Learning TensorFlow:<br>https://github.com/pranigopu/exploringTensorFlow

## Project aims
Run and view the results of text mining and sentiment analysis functions implemented in a Python backend using a Chrome extension.

## Purpose of each script
**Popup script**:<br>
Process user input, make requests to the background service worker for data, get response, and perform operations on the data to finally present it in the popup page.

**Background service worker**:<br>
Make requests to the Django-based localhost server and send response to popup script. Background service worker is used since it only unloads when the process it has performed has completed, while popup script will unload if you click away from the popup page. This can pose problems, since HTTP requests and data processing can take time, and we want to be able to collect the necessary data any time it is ready.

## Dependencies
To run the backend properly, make sure that you have installed the following Python packages in your Python environment:

- nltk<br>_Needed for word tokenization & POS tagging._
- textblob<br>_Needed for lemmatization & sentiment analysis._
- requests<br>_Needed for making get requests to a URL to obtain the webpage HTML DOM._
- bs4<br>_Has **BeautifulSoup** needed for parse the received data from a **get** request as HTML._
- pandas<br>_Needed for reading from and writing to CSV files._
- re<br>_Needed for string pattern identification and processing._

## Implementation notes
### Using service worker vs. using popup script
To make the request to the server, we can use any extension script. Using popup script would have been most direct, since messaging would not be necessary, and we can directly show the response in the popup page.
<br><br>
My reason for using background service worker was because a background service worker loads when an event it listens for is triggered, and only halts after the completion of its code's exectution. However, a popup script will only run as long as the popup page is loaded. While in this mini-project, this is not an issue, since the processes happen quite quickly, for more time consuming processes, such as text mining or sentiment analysis, it could be an issue, since closing the popup page would halt those processes.

### Wordcloud script
The JavaScript code for wordcloud was taken from

- https://www.npmjs.com/package/wordcloud

I have modified the installed package, removing all the files I deemed unnecessary and renaming the package directory to simply 'wordcloud'.

#### Accessing through popup script
To access the 'WordCloud' function from 'wordcloud2.js' using the popup script, I simply include the script in 'popup.html' before the popup script. The required canvas element must be created in the popup page's DOM, either dynamically or in the HTML document itself.

#### Accessing through content script
__(And why this approach was abandoned)__ <br><br>
To access the 'WordCloud' function from 'wordcloud2.js' using the content script, I simply added the relative path to 'wordcloud2.js' in the "content_scripts" field of the 'manifest.json' file. Accessing the wordcloud functionalities in the content script was necessary to create and insert a canvas object with the wordcloud within the current webpage's DOM (since the current webpage is not stored locally in the extension's directory, we cannot simply add a script tag with a reference to 'wordcloud2.js' using the relative path).
<br><br>
This approach to a user interface was abandoned due to the following reasons:

- Even if we insert the canvas at the beginning of the current webpage, and even if we do it within a division (div) tag, the result may not appear as desired for every webpage as desired, due to the possible particular features applied for the webpage. For example, when trying to insert the canvas at the beginning of a Wikipedia page's body, the wordcloud display always clashed with the Wikipedia logo at the top left of the page. We could fine-tune our code for Wikipedia, but then we would lose generality.
- As a user, it may be more convenient to have the results always readily accessible in the popup page, and not at the very top of the webpage's body. This inconvenience may occur if the user wishes to scroll around the webpage or go to other tabs but still wishes to have the results easily accessible through the extension's button (that would open the popup page).<br><br> __The issue with a popup page, however, is that a popup page and its script are only loaded when the popup page is opened, and the dynamic results on the page are not persistent. If this issue can be overcome, the popup page interface would be undoubtedly superior, in my eyes.__
- To display the results in the current webpage's DOM, anu open webpage had to be reloaded whenever the extension was reloaded in developer mode. This issue is not going to occur for the end-user of course, since the end-user is not supposed to want to (or be able to) reload the extension as a developer. But this is a minor developer hassle that added to our other woes.

### Cross origin request from extension to localhost server
To prevent leaks of sensitive information, webpages are generally not allowed to fetch cross-origin data. Unless a valid CORS header is present on the response, the page's request will fail with an error like the one above.
<br><br>
A valid CORS header in this case would indicate that the requested resource (in whose response the header would be present) (ex. a server host or website) allows requests from other origins (ex. other server hosts or websites) to access its resources (ex. response data)

### Reiteration of key point and side notes
Just to emphasise the point, the extension package and Django-based backend are stored in and run from different domains, hence a request from the extension scripts to the server web application's service is a cross-origin request.
<br><br>
To allow the cross-origin request (from the extension's scripts) to access the requested resource (i.e. the localhost server's web application's service), the server host (my computer's local IP address) must add the appropriate header to its responses, so that there is no issue according to the CORS policy.

### Solution details
To handle CORS headers in Python, we installed the `django-cors-headers` package. In the Django-based website's configurations directory (i.e. backend/backend), in the 'settings.py' file, we did the following:

- Added `corsheaders` in the `INSTALLED_APPS` list
- Added `corsheaders.middleware.CorsMiddleware` in the `MIDDLEWARE` list
- To allow any possible host (for my website) to add the valid CORS header to the website's responses, I did the following (within the 'settings.py' file)

```
ALLOWED_HOSTS=['*']
CORS_ORIGIN_ALLOW_ALL = True
```

### REFERENCES
- https://www.chromium.org/Home/chromium-security/extension-content-script-fetches/
- https://dzone.com/articles/how-to-fix-django-cors-error
