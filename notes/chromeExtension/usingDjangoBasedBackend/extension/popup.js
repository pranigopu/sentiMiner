document.querySelector("#submit").addEventListener("click", react);
// For querying ID, we use '#'. For querying classes, we would use '.'.

function react(){
    //====================================
    // Creating message
    let userinput = document.querySelector("#name").value;
    // Making the message in a generalised format
    message = {
        "name": userinput
    }
    // The above is not necessary for this project, but is a good practice
    //====================================
    // Sending message to the service worker & getting response
    chrome.runtime.sendMessage(
        message,
        getResponse);
    function getResponse(response){
        console.log(response);
        /*
        NOTE ON INTENDED RESPONSE'S STRUCTURE
        The structure of the JSON response (return value)
        of the view function in question
        (defined in the website's (backend's) source code) is
        
        {
            "name": <name>,
            "vowels": <vowel list>
        }
        
        Keeping this in mind, we can access the vowel list using
        response.vowels
        */
        document.querySelector("#blank").innerHTML = "Vowels: " + response.vowels;
    }
}