## Extension version & version name
An extension version is the version given to the current form of the extension by the programmer. One to four dot-separated integers (given as a string i.e. within double quotes) can be used to identify the version of this extension. A couple of rules apply to the integers: they must be between 0 and 65535, inclusive, and non-zero integers can't start with 0. For example, 99999 and 032 are both invalid.
<br><br>
Chrome's autoupdate system compares versions to determine whether an installed extension needs to be updated. If the published extension has a newer version string than the installed extension, then the extension is automatically updated. The comparison starts with the leftmost integers. If those integers are equal, the integers to the right are compared, and so on. For example, 1.2.0 is a newer version than 1.1.9.9999. A missing integer is equal to zero. For example, 1.1.9.9999 is newer than 1.1 and 1.1.9.9999 is older than 1.2.
<br><br>
In addition to the version field, which is used for update purposes, version_name can be set to a descriptive version string and will be used for display purposes, if present. Here are some examples of version names:
- "version_name": "1.0 beta"
- "version_name": "build rc2"
- "version_name": "3.1.2.4567"

If no version name is present, the version field will be used for display purposes as well.

### REFERENCES:
- https://developer.chrome.com/docs/extensions/mv2/manifest/version/

## Overriding Chrome pages
Chrome extensions allow you to replace the default chrome pages for bookmarks, history, and new tab. Override pages are a way to substitute an HTML file from your Chrome browser extension for a page that Google Chrome normally provides. In addition to HTML, an override page usually has CSS and JavaScript code. To replace new tab, for example, add the following to manifest.json.
```
"chrome_url_overrides": {
  "newtab": "newtab.html"
}
```
An extension can replace any one of the following pages:
- Bookmark manager
- History
- New tab

### REFERENCES:
- https://developer.chrome.com/docs/extensions/mv3/override/

## Browser action (action in manifest version 3)
A browser action (or simply action in manifest version 3) is a button that your extension adds to the browser's toolbar. The button has an icon, and may optionally have a popup whose content is specified using HTML, CSS, and JavaScript.
<br><br>
Note that browser and page actions can’t access the DOM itself, however, they can communicate with the content script via the chrome “messaging” API. A browser action should have an icon (for the button) as well as a JavaScript file for the code.
<br><br>
When the user clicks the button, it triggers an "onClick" event. Other events cn also be triggered through this event, as we see in JavaScript 'messaging'.
<br><br>
Each extension has only one browser action, which can involve multiple aspects  such as
- Title
- Popup display
- Icon

## Permissions
Permissions of a browser extension includes the aspects of the browser or client device that the extension needs to access and control to some degree for some or all of its functionalities.

## chrome.runtime
Use the chrome.runtime API to retrieve the background page, return details about the manifest, and listen for and respond to events in the app or extension lifecycle. You can also use this API to convert the relative path of URLs to fully-qualified URLs.
<br><br>
The runtime API provides methods to support a number of areas of functionality that your extensions can use, such as the following...

### Message passing
These methods support message passing so that you can communicate with different parts of your extension (such as an extension popup and background scripts), other extensions, or native applications on the user's device. See Message Passing for an overview of the subject. Methods in this category include connect, connectNative, sendMessage, and sendNativeMessage.

#### chrome.runtime.sendMessage
This function sends a single message to event listeners within your extension or a different extension. If sending within your extension, omit the 'extensionId' argument. The 'runtime.onMessage' event will be fired in each page in your extension, except for the frame that called 'runtime.sendMessage'. If sending to a different extension, include the 'extensionId' argument set to the other extension's ID. 'runtime.onMessageExternal' will be fired in the other extension. 'runtime.sendMessage' is an asynchronous function that returns a 'Promise' object.
If one argument is given, it is the message to send, and the message will be sent internally. if two arguments are given, the arguments are interpreted as (message, options), and the message is sent internally, if the second argument is any of the following:
- a valid options object (i.e. an object which contains only the option properties the browser supports)
- null
- undefined

otherwise, the arguments are interpreted as (extensionId, message). The message will be sent to the extension identified by extensionId. If three arguments are given, the arguments are interpreted as (extensionId, message, options). The message will be sent to the extension identified by extensionId.
<br><br>
Extensions cannot send messages to content scripts using this method. To send messages to content scripts, use 'tabs.sendMessage'.
<br><br>
#### REFERENCES:
https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/sendMessage

### Accessing extension and platform metadata
These methods let you retrieve several specific pieces of metadata about the extension and the platform. Methods in this category include getBackgroundPage, getManifest, getPackageDirectoryEntry, and getPlatformInfo.

### Other functionalities
Other options (not relevant to me right now)
- Managing extension lifecycle and options
- Device restart support
- Helper utilities

## Promise
A 'Promise' is an object representing the eventual completion or failure of an asynchronous operation. Essentially, a promise is a returned object to which you attach callbacks, instead of passing callbacks into a function.
<br><br>
**NOTE**: A callback is any reference to executable code that is passed as an argument to other code. In other words, the other code is expected to call back the code at a given time.

### Advantages of using promises
Unlike regular callbacks, a promise comes with some guarantees...

1. Callbacks added with 'then()' will never be invoked before the completion of the current run of the JavaScript event loop.
2. Callbacks will be invoked even if they were added after the success or failure of the asynchronous operation that the promise represents.
3. Multiple callbacks may be attached to the same promise by calling then() several times. They will be invoked one after another, in the order in which they were inserted.
4. Chaining of callbacks can be done, i.e. two or more asynchronous operations can be executed back to back, where each subsequent operation starts when the previous operation succeeds, with the result from the previous step. We accomplish this by creating a promise chain.

#### REFERENCES:
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises

### REFERENCES:
- https://developer.chrome.com/docs/extensions/reference/runtime/

## Content scripts
Content scripts are files that run in the context of web pages. By using the standard Document Object Model (DOM), they are able to read details of the web pages the browser visits, make changes to them, and pass information to their parent extension.

A content script has full access to the DOM of a webpage, so you can do things like alter content, styles, layout, images, anything that is on the page. In other words, a content script deals specifically with the contents of the webpage, and not the browser in general. You can access the DOM in the content script's source code through the 'document' object and its attributes and methods available in JavaScript. For example...
`document.getElementByTagName("h1");`
... will obtain all the "h1" elements of the current webpage (on which the extension is active).
<br><br>
Importantly, the content script is a source code (which can also include and reference CSS) that runs right after the page loads. Hence, when you load or reload a page with the extension active, the content script executes.
<br><br>
The manifest.json file should reference your content script, in the "content_scripts" field. For example:
```
"content_scripts": [
  {
    "js": ["content.js"]
  }
]
```
You also need to specify which URLs the content script should run on. Furthermore, you can use the wildcard * to encompass all paths on a given domain. For example, the following would run the content script on any github.com page:
```
"content_scripts": [
{
  "matches": [
    "http://github.com/*",
    "https://github.com/*",
    "http://*.github.com/*",
    "https://*.github.com/*"
    ],
   "js": ["content.js"]
  }
]
```
For allowing it to run on all URLs, you would add:
```
"content_scripts": [
  {
  "matches": [
    "<all_urls>"
    ],
  "js": ["content.js"]
    }
]
```
Content scripts can access Chrome APIs used by their parent extension by exchanging messages with the extension. They can also access the URL of an extension's file with 'chrome.runtime.getURL()' and use the result the same as other URLs.
<br><br>
Note that 

### REFERENCES:
- https://developer.chrome.com/docs/extensions/mv3/content_scripts/
- https://shiffman.net/a2z/chrome-ext/

## Managing events with service workers
_Service workers => Background scripts in manifest version 2_
<br><br>
Extensions are event-based programs used to modify and enhance the functionalities and features available through a Chrome browser. Events are browser triggers, such as:
- Navigating to a new page
- Removing a bookmark
- Closing a tab
-  Clicking the extension's button
<br><br>
Extensions monitor these events using scripts in their background service workers, which, when loaded, react based on specified instructions. A background service worker is loaded when needed, and unloaded when idle. Examples of scenarios where background service workers would be loaded:
- Extension is first installed or updated to a new version
- The event background script was listening for is dispatched
- A content script or another extension sends a message
- Another view in the extension (such as a popup) cals the function
  runtime.getBackgroundPage
<br><br>
Once loaded, an extensions's service worker generally keeps running as long as it is performing an action, such as calling a Chrome API or issuing a network request. Effective background scripts lay dormant until the event they are listening for fires, which is when they react based on specified instructions, and then unload.

### Registering background service workers
Extensions register their background service workers in the manifest, under the "background" field. This field associates the "service_worker" key to the JavaScript file of the background script. The script for the service worker must be located in your extenstion's root directory.
<br><br>
You can optionally specify an extra key within the "background" field, called "type". For this, if you specify "module" (we will not discuss this here).

### Debug console for background service workers
Note that the debug console of a service worker differs from the webpage debug console (which can show the outputs of the `console.log` commands of the content scripts). Rather, a service worker has a different debug console (which can show the outputs of the `console.log` commands of the service worker's script), that can be accessed through the developer mode in the browser extensions display page (chrome://extensions for Google Chrome), usually by clicking the relevant option on the desired extension's information box, such as _Inspect views service worker_.

### REFERENCES:
- https://developer.chrome.com/docs/extensions/mv3/service_workers/

## Note on content scripts & background service workers
Content script actions refect on the JavaScript console of the active web page. However, background service worker actions do not. This is because the debug console's scope is the contents of the webpage.
<br><br>
Furthermore, a content script cannot detect browser actions. To allow a background service worker to communicate to the content script, we use the messaging services of the chrome.runtime API provided my chrome.
<br><br>
A content script can access the DOM of the webpage that has been loaded (provided the extension is active), but has access to only a limited subset of the browser's (JavaScript) APIs. A background service worker has access to all the browser's (JavaScript) APIs, but cannot directly access the DOM of any webpage. This is why interaction between the content and background service worker is necessary to achieve more functionalities in your browser extension.

### References
- https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Content_scripts

## Console
In JavaScript, the console is an object which provides access to the browser debugging console.

## Anonymous functions in JavaScript
Functions in JavaScript can be anonymous.
```
function() {
  alert('unicorn!');
}
```
And if you put that whole anonymous function in parentheses and then add parentheses after it, it’s a self-executing function. Meaning it’s called the moment it’s defined.
```
(function() {
  alert('unicorn!');
})();
```
If your code is complicated and long it’s often simpler to just put it in another JS file and reference it like so:
```
(function () {
  var script = document.createElement('script');
  script.src = 'someRandomCode.js';
  document.body.appendChild(script);
})();
```
## Messaging in JavaScript
If you want to execute some code in the content script (to manipulate the DOM) whenever the user triggers the browser action, you need to use "messaging". A message is a JavaScript object (of your own design) that you send from the background service worker / background script to the content script. For example:
```
// IN BACKGROUND SCRIPT
function buttonClicked(tab){
  var msg = {
    message: "user clicked!"
  }
  chrome.tabs.sendMessage(tab.id, msg);
}
```
Then, in the content script, you can receive the message and perform an action. Lots of data comes in with the message, but the actual object you send is the one denoted by the request variable. For example:
```
// IN CONTENT SCRIPT
// Listen for messages
chrome.runtime.onMessage.addListener(receiver);

// Callback for when a message is received
function receiver(request, sender, sendResponse) {
  if (request.message === "user clicked!") {
    // Do something!
  }
}
```
SEE ALSO:
- Omnibox

### REFERENCES:
- https://shiffman.net/a2z/chrome-ext/
