# CONCEPT NOTES
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
<br><br>
For example, "activeTab" allows access to the current (active) tab that the user is on. "tabs" alows access to all open tabs in the browser.

## chrome.runtime
Use the chrome.runtime API to retrieve the background page, return details about the manifest, and listen for and respond to events in the app or extension lifecycle. You can also use this API to convert the relative path of URLs to fully-qualified URLs.
<br><br>
The runtime API provides methods to support a number of areas of functionality that your extensions can use, such as...

### Message passing
`chrome.runtime.sendMessage` sends a single message to event listeners within your extension or a different extension. If sending within your extension, omit the 'extensionId' argument. The 'runtime.onMessage' event will be fired in each page in your extension, except for the frame that called 'runtime.sendMessage'. If sending to a different extension, include the 'extensionId' argument set to the other extension's ID. 'runtime.onMessageExternal' will be fired in the other extension. 'runtime.sendMessage' is an asynchronous function that returns a 'Promise' object.
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

## Message passing
These methods support message passing so that you can communicate with different parts of your extension (such as an extension popup and background scripts), other extensions, or native applications on the user's device. Methods in this category include connect, connectNative, sendMessage, and sendNativeMessage.
<br><br>
**NOTE**: The API used to send or receive a message from a non-tab context (ex. from a background service worker or a popup) to content scripts (that operate within a tab's context) differs from the API used to send or receive a message from a tab's context (i.e. from the content script) to a non-tab context, specifically the background service worker. For the former, we use `chrome.tabs`, for the latter, we use `chrome.runtime`. Both APIs provide the `sendMessage` service.
<br><br>
This helps understand why we use listen for the `chrome.runtime.onMessage` event when listening for messages from the background service worker in the content script. This also helps understand why we need to send a message to a particular tab ID  using `chrome.tabs.sendMessage` when sending from background service worker to content script, since content script has separate instances running on each open tab.


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
<br><br>
For each open tab, a separate instance of the content script (i.e. separate process based on the content script source code) is created (provided the browser extension is active). Content scripts are **injected** into a tab, either through the **manifest.json** file (under the **content_script** field) or through the background service worker.
<br><br>
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
- Another view in the extension (such as a popup) calls the function
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

## Console
In JavaScript, the console is an object which provides access to the browser debugging console.

## Browser extension pop-up
A browser action (typically clicking the extension icon) can also trigger the appearance of a pop-up (which is simply an HTML page. which possibly uses JavaScript and CSS elements). To do this, reference the pop-up HTML file in manifest.json as follows:
```
"browser_action": {
  "default_title": "Hello there!",
  "default_popup": "popup.html"
}
```

The pop-up can also communicate with the content script via messaging. Note that pop-up cannot directly message a background script, and must use the content script as an intermediate.
<br><br>
Also note that a pop-up's script starts to execute only when the browser action is performed. In other words, it does not keep running in the background, and only runs when viewed.

### REFERENCES
- https://shiffman.net/a2z/chrome-ext/

## Scopes of the content, service worker and popup scripts
The scopes of these scripts are separate.
<br><br>
The scope of content script is the DOM of the current webpage. Only the content script can access and manipulate the DOM of the current webpage. The script is run as soon as the webpage is loaded.
<br><br>
The scope of the background service worker is browser actions. Only the background script can detect and respond to browser actions. The script is only run upon the firing of an event it is listening for.
<br><br>
The scope of the popup script is the extension popup alone. Only the popup script can access and manipulate the DOM of the popup of the extension. The script is only run when the popup is loaded on screen.

## Inline script vs. external script
Inline script is simply script that is provided within the HTML document. Furthermore, when the DOM is created using the HTML document, references to an external script within HTML elements, such as
- `onclick` option for submit buttons
- `action` option for form elements

become inline code within the DOM.
<br><br>
External script is simply script that is provided in another document and included in the HTML document through the script tag.
<br><br>
Similarly, we also have inline styles and external styles.

## CSS selector
A CSS selector selects the HTML element, using the CSS (cascading style sheets) format. They are used to find select the elements that you want to

- style
- listen (for events, such as `onclick` for a button)
- simply access and modify

We can divide CSS selectors into five categories:

- Simple selectors (select elements based on name, id, class)
- Combinator selectors (select elements based on a specific relationship between them)
- Pseudo-class selectors (select elements based on a certain state)
- Pseudo-elements selectors (select and style a part of an element)
- Attribute selectors (select elements based on an attribute or attribute value)

(For this project, we are only concerned with simple selectors).

### Simple selectors
- CSS element selector (HTML element name, ex. 'p')
- CSS ID selector _(ID prefixed with '#', ex. '#xyz')_
- CSS class selector _(class prefixed with '.', ex. '.xyz')_
- CSS element class selector _(element name follows by class, ex. 'p.xyz' (p is the element, xyz is the class))_
- CSS universal selector _(all elements, denoted by '*')_
- CSS grouping selector _(multiple selectors separated by comma, ex. 'h1, h2, p')_

## document.querySelector
### Description
`querySelector` is a function that is an attribute of the DOM object of an HTML page. It returns the first element that matches a given CSS selector.

### Syntax and return value
`document.querySelector(<CSS selector>, <callback>)`... The return value is a NodeList (there can be multiple document nodes if CSS group selectors are used... otherwise, there may be a single document node). If no matches are found, `null` is returned.

#### NodeList vs. HTMLCollection
A node list is similar to an HTMLCollection, except that HTMLCollection elements can only be HTML elements, whereas NodeList elements are document nodes (ex. element nodes, attribute nodes, and text nodes), which can be similar to HTML elements if the match happens to be an HTML element.
<br><br>
Furthermore, An HTML collection is always a live collection that dynamically reflects changes to the DOM. However, a NodeList is a static collection. The nature of the return value is the main thing that separates `getElementBy...` functions and `querySelector...` functions.

### Notes on related functions
`querySelectorAll()` is similar to `querySelector()`, except that instead of stopping at the first match, it returns all possible matches in a NodeList. Also like `querySelector()`, its return value is a static collection.

### REFERENCES:
- https://www.w3schools.com/jsref/met_document_queryselector.asp
