console.log("Content script, check.");

chrome.runtime.onMessage.addListener(respondToMessage);
function respondToMessage(message, sender, sendResponse){
    console.log("Message received:", message)
    message.sentFrom = "content.js"

    // Sending message to background script...
    chrome.runtime.sendMessage(message);
}