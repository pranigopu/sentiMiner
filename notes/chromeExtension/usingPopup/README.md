# Extension using popups
## Project aims
Understand the usage, properties and debugging methods for a popup of a Chrome extension, and understand how to pass messages to and from the content script and popup script.
<br><br>
We are doing this because to communicate with the background script, the popup script must use the content script as the intermediate, since the background script only listens to browser actions and events from the content script.

## Code aims
- Show a popup that asks for input of name
- Pass the name as a message to the content script
- Print the message in the content script's debug console _(which is the same as the active tab's debug console)_
