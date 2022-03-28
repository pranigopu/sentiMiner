// To demonstrate that the onMessage event from the popup script is not detected by the background script...
console.log("Background service worker, check.");

chrome.runtime.onMessage.addListener(respondToMessage);
function respondToMessage(message, sender, sendResponse){
    console.log("Message received:", message);

    // Sending response back to content.js
    sendResponse("Hello from the background script!");
}