# Learning to make requests to a Django-based backend
## Project aims
Having implemented a simple Django-based website on my own computer (localhost), using an emulated server, I will make requests to particular endpoints (services i.e. view functions) within the server from within a Chrome extension. Functionally, the end product here is simply a Chrome extension that uses functions written in Python using the respective URL's of the functions.

## Code aims
- Make a service i.e. view function in the server that takes the 'name' option's value and returns the vowels in the name
- Make a popup interface in the Chrome extension to allow user input
- Message the user input to the service worker
- Make a request from the service worker using the received name
- Obtain the response and send it in a serialised format as a response to the popup script's messaging call
- Display the results within the popup

## Notes on implementation
I used the background service worker to make requests to my localhost server, instead of using the popup script itself. This is because when I applied the necessary code for making requests from the popup script _(the source code for this is present in the 'extensions' directory as 'popup (INVALID).js')_, I got the following errors<br>
<br>**ERROR 1**<br>
```
Access to fetch at 'http://127.0.0.1:8000/alpha/name?name=Prani' from origin 'chrome-extension://pehhkdndjcmeebmpmkeofnbaiideooeh' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.If an opaque response 
serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
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

### REFERENCES
- https://www.chromium.org/Home/chromium-security/extension-content-script-fetches/
