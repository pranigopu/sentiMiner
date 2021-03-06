document.querySelector("#go").addEventListener("click", makeRequest);
// For querying ID, we use '#'. For querying classes, we would use '.'.
//================================================
function getScrapeBy(){
    let scrapeby = document.querySelector("#scrapeby").value;
    switch(scrapeby){
        case "Paragraph": return "p";
        case "Sentence": return "sentence";
        default: return scrapeby
    }
}
function makeRequest(){
    //------------------------------------
    // Checking if the command input is valid
    // Object relating commands to numbers (allows switch-case based on command later on)
    let commands = {
        "scrape": [],
        "format": [],
        "clean": [],
        "normalize": [],
        "summarize": ["wordcloud", "freqdist", "*"],
        "analyze": ["bipolar", "finegrained", "*"]};
    let usercmd = document.querySelector("#command").value;

    // Displaying whether the command is valid or not
    document.querySelector("#blank").innerHTML = " ";
    if(!(Object.keys(commands).includes(usercmd))){
        // Displaying that the given command invalid
        document.querySelector("#blank").innerHTML = "Invalid command";
        // Terminating callback
        return;
    }
    //------------------------------------
    // Creating and sending message (if command is valid)
    //________________________
    // Obtaining the URL of the current page
    /*
    To do this, we will acquire the information on the current tab
    using chrome.tabs.query. The message will be sent to the background script
    from the callback of this API call.
    */
    chrome.tabs.query(
        {active: true, currentWindow: true},
        function(tabs){
            // Obtaining current tab URL
            console.log("Current tab URL:", tabs[0].url);

            // Creating message
            // Backend address provided
            let backendaddress = document.querySelector("#backendaddress").value;
            // "Scrape by" input
            let scrapeby = getScrapeBy();
            let message = {
                "operation": usercmd,
                "scrapeby": scrapeby,
                "targeturl": tabs[0].url,
                "backendaddress": backendaddress
            }

            // Displaying a statement indicating that the extension is waiting for a response
            document.querySelector("#blank").innerHTML = "Waiting for response..."
            chrome.runtime.sendMessage(
                message,
                function(response){
                    console.log("Response received:", response);
                    /*
                    The response's expected structure is
                    {
                        'operation': <text>,
                        'report': <text>,
                        'data': <any>,
                    }
                    Using this, we do the following...
                    */
                    //------------------------------------
                    // Displaying response report
                    document.querySelector("#blank").innerHTML = response.report;
                    //------------------------------------
                    // Clearing the "scrapeby" value
                    /*
                    This is done so that if you want to perform another command
                    on the scraped data, you don't have to manually remove the
                    "scrapeby" value, and can simply enter the next command.
                    */
                    document.querySelector("#scrapeby").value = " "
                    //------------------------------------
                    // Terminating the function if response data is empty
                    if(response.data.length == 0){return}
                    //------------------------------------
                    // If data is non-empty, then acting based on response operation and user-given option
                    
                    // Checking for "scrapeby" value's options (that offer functionalities on top of the respective command)
                    /*
                    The full intended format of an option is
                    <option name>, <parameter1>, <parameter2>...
                    There can be no parameters as well.
                    Hence, we shall split the option string.
                    */
                    let useropt = document.querySelector("#option").value + ", ";
                    // Appending ", " to the option string helps us identify the last parameter more easily.
                    // It also ensures that there will always at least two elements in the split option string.
                    // This removes need for array out of bounds exception handling, in some of the cases.

                    // Obtaining and trimming all parameters
                    useropt = useropt.split(",");
                    // Now, useropt is a list of strings.
                    for(i=0; i<useropt.length; i++){
                        useropt[i] = useropt[i].trim();
                    }

                    // If option is empty, change it to '*' i.e. "all"
                    if((useropt[0] == null) || (useropt[0].length == 0)){useropt = "*";}

                    // Acting based on command
                    // (Note that in JavaScript, switch-case works with strings as well)
                    switch(response.operation){
                        case "summarize":
                            // If option does not exist in options list for the command
                            if(!(commands[response.operation].includes(useropt[0]))){
                                // Displaying that the given command invalid
                                document.querySelector("#blank").innerHTML = "Invalid option";
                                // Terminating callback
                                return;
                            }
                            // Act based on option
                            // (Below function defined in 'popup_helpersFor_summarize.js')
                            performSummaryOption(useropt, response);
                            break;
                        
                        case "analyze":
                            if(!(commands[response.operation].includes(useropt[0]))){
                                // Displaying that the given command invalid
                                document.querySelector("#blank").innerHTML = "Invalid option";
                                // Terminating callback
                                return;
                            }
                            // Act based on option
                            // (Below function defined in 'popup_helpersFor_analyze.js')
                            performAnalyzeOption(useropt, response);
                            break;
                    }
                });
        })
}
