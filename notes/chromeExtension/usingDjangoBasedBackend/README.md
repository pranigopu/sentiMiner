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
