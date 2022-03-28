# Message relay from popup to service worker & back
## Project aims
Introducing popups, and understanding how messaging is done from

- popup to content script (in a certain tab)
- popup to background service worker
- content script (in a certain tab) to background service worker

Also, we will see how responses can be sent by the receivers and obtained by the senders.

## Code aims
- Present a popup input
- Based on input, sending message from popup script to
    - Content script injected in the active tab
    - Background service worker
- Getting responses for each
- Displaying responses in the popup
