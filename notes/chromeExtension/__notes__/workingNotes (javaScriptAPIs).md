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

### Sending multiple messages
I found that, when trying to send messages from popup script to content script and popup script to background service worker within the same event handler, only the message from popup script to background service worker got a response, no matter whether I first messaged the content script or the background service worker. I need to look into this...