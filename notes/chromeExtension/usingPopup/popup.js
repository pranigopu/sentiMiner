document.querySelector("#submit").addEventListener("click", react);
// For querying ID, we use '#'. For querying classes, we would use '.'.

function react(){
    /*
    To get current tab, since popup is running in a non-tab context, we use chrome.tabs.query.
    The main arguments are chrome.tabs.query(object queryInfo, function callback).
    Returns object with info on the tabs selected based on properties specified in queryInfo.
    If no properties are specified, info on all open tabs are returned.
    */
    properties = {
        active: true, // Must be active tab
        currentWindow: true // Tab must be from current window
    }
    chrome.tabs.query(properties, getTabs); // getTabs defined below
    /*
    The callback of this query accepts the info of tabs as an argument.
    Through this, the required object containing tab info can be obtained within the callback.
    Note that the argument's scope is within the function, and you cannot use it outside.
    */
    function getTabs(tabs){
        console.log("Getting tabs...");
        console.log(tabs)
        // Sending message (in our case, it is simply the entered name)
        var userinput = document.querySelector("#name").value;
        let message = {
            "name": userinput,
            "activeTab": tabs[0].id,
            "sentFrom": "popup.js"
        };
        chrome.tabs.sendMessage(tabs[0].id, message);
    }
}