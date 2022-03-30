// Defining the server address
let serverhost = "http://127.0.0.1:8000/" // localhost address
// NOTE: localhost => my own computer

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
    // Defining endpoint URL
    /*
    Accessing the URL of the
    Django web framework designed
    backend's
    app's
    'getName' view function
    (giving the user's input as the name option in the request)

    NOTE: For this URL to work, the server should be running!
    */
    let url = serverhost + "alpha/name?name=" + message.name
    // Viewing the URL for confirmation in the console
    console.log(url)
    //====================================
    // Sending response back to content.js
    fetch(url)
    .then(function(response){
        res = response.json();
        // Inspecting res in console
        console.log(res);
        /*
        We see that res i.e. the return value of response.json()
        is a promise object, that is in the 'pending' state.
        To resolve this promise object, we use the following .then call.
        */

        // Returning this promise object makes it accessible outside the current scope
        // Hence we can apply the following .then call
        return res;
    })
    .then(d => {
        console.log(d);
        document.querySelector("#blank").innerHTML = "Vowels: " + d['vowels'];
    });
    /*
    SIDE NOTE
    // Alternate codes for...
    .then(function(response){
        return response.json();
    })
    //____________
    //1.
    .then(response => {return response.json()})
    //____________
    //2.
    .then(response => response.json())
    */
    return true;
}
