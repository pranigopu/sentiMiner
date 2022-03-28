# WORKING NOTES
## NOTE ON NAMING FORMAL ARGUMENTS OF CALLBACKS
The arguments discussed for the callbacks are not keywords, unless otherwise specified, i.e. any name can be given to them, provided they are passed in the appropriate order. However, for convenience, we usually use the above names as the formal arguments of our callback definitions.

## chrome.tabs.getCurrent()
_Why is cannot be used for pop-ups or background service workers..._
<br><br>
`chrome.tabs.getCurrent(function callback)` returns an object containing information on the tab in which the script call is made. It may be undefined if it is called from a non-tab context, such as a background page, background script and pop-up views.

## chrome.tabs.query()
`chrome.tabs.query(object queryInfo, function callback)` returns objects containing information for every tab that satisfies the properties specified in `queryInfo`. If no properties are specified, it returns objects containing information for every open tab in the browser.

## Anatomy of chrome.runtime.sendMessage
`chrome.runtime.sendMessage` can have the following optional arguments:

- message (to be sent)
- response (sent from the receiver)

### response
This argument is a callback, which executes upon receiving a response from the receiver of the message that was sent. It can have at most one argument (you can define more, but they won't be used, since the sent reponse (as seen later) will only contain one argument's worth of data), which will by default store the data passed in the response.
<br><br>
For example...
```
chrome.runtime.sendMessage(
        message,
        getResponse);
// getResponse is a callback defined as follows...
function getResponse(response){
    console.log("Response:", response)
    }
```

## Anatomy of a chrome.runtime.onMessage event listener callback
To detect an `onMessage` event, we add a listener for this event using `chrome.runtime.onMessage.addListener(<callback>)`.
<br><br>
The callback (i.e. the function that whose call will be triggered upon event) here has three optional arguments:

- message (also called request, in different contexts)
- sender (information about the sender), which contains
	- message ID
	- message origin _(as URL... is null when message is sent from a non-tab context ex. from a background page)_
	- message tab _(from which message was sent)_
- sendResponse

### sendResponse
This argument is a callback that, if called but undefined, can be used to:

- simply send an acknowledgement response
- send a single object as response

For example, in a background script...
```
chrome.runtime.onMessage.addListener(respondToMessage);
function respondToMessage(message, sender, sendResponse){
    console.log("Message received:", message);
    sendResponse("Hello from the other side!");
}
```
Here, we see that sendResponse has not been defined anywhere, and takes on some default definition. I am not too sure about the exact mechanism.

## Sending multiple messages
I found that, when trying to send messages from popup script to content script and popup script to background service worker within the same event handler, only the message from popup script to background service worker got a response, no matter whether I first messaged the content script or the background service worker. I need to look into this...

## Making requests to an external domain from the extension
For my mini-project where I tried to make requests and get responses from the web applications of my Django-based localhost server, used the background service worker to make requests, instead of using the popup script itself. This is because when I applied the necessary code for making requests from the popup script, I got the following errors
<br>**ERROR 1**<br>
```
Access to fetch at 'http://127.0.0.1:8000/alpha/name?name=Prani' from origin 'chrome-extension://pehhkdndjcmeebmpmkeofnbaiideooeh' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
```
<br>**ERROR 2**<br>
```
Uncaught (in promise) TypeError: Failed to fetch
```
<br>
The latter error is due to the former. Furthermore, I haven't included a **.catch** function for my **fetch** function call, so errors are 'uncaught' and handled automatically.
<br><br>
From these errors and some reading, I learnt that
-  We can make requests from the popup script if we set the 'mode' option in the **fetch** funtion to 'no-cors'<br><br>(**NOTE**:<br> **fetch** has two main arguments, one being the URL to make the requets to, the other being the set of properties to apply to the request... if none are applied, the request is a simple GET request)
-  Requests we make from the popup script using the above option will return an opaque response only i.e. we cannot
  - read response data
  - check request status (to see if it was successful or not)

The above clearly presents an undesirable situation.

### Apparent cause
To prevent leaks of sensitive information, webpages are generally not allowed to fetch cross-origin data. Unless a valid CORS header is present on the response, the page's request will fail with an error like the one above.
<br><br>
Content scripts are injected into a webpage, hence run from the context of a particular webpage, which means this restriction often applies to request made from content scripts. Popup scripts are included in the popup page, hence run from the context of a particular popup page. While not technically a webpage, the restriction seems to apply to them in this case. This is due to Google Chrome's particular CORS policy, which subsumes Chrome extensions. To circumvent this, we use the service worker to make cross origin requests, since service workers do not run from the context of any webpage.

### Reiteration of key point and side notes
Just to emphasise the point, the extension package and Django-based backend are stored in and run from different domains, hence a request from the extension scripts to the server web application's service is a cross-origin request. When working within the localhost, and when not having published the extension, this difference in domains is simply reflected in the difference in the directories in which the source codes for each are present and run from.

### REFERENCES
- https://www.chromium.org/Home/chromium-security/extension-content-script-fetches/
