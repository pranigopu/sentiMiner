// Processing data for bipolar sentiment analysis
function processDataFor_analyze_bipolar(response, noneutral){
    // Processing data
    /*
    The data we in the response is in the format
    [[<text1>, <text2>...], [<sentiment1>, <sentiment2>...]]
    
    We will keep this in mind when performing the operations below.
    This function will classify the sentiments as neutral, positive or negative,
    and create labels accordingly. For this, we will only iterate through the second list...
    */

    // Should we include neutral sentiment values?
    if(noneutral == "noneutral"){
        noneutral = 0; // No, exclude neutrals
    } else{
        noneutral = 1; // Yes, include neutrals
    }

    let labels = ["positive", "negative"];
    let values = [0, 0];

    // If noneutral is 1 i.e. we are including neutral values
    if(noneutral == 1){
        labels.push("neutral");
        values.push(0, 0, 0);
    }
    
    let sentiment = 0;
    for(i=0; i<response.data.length; i++){
        sentiment = response.data[i][1];
        if(sentiment > 0){
            // Positive sentiment count
            values[0]++;
        } else if(sentiment < 0){
            // Negative sentiment count
            values[1]++;
        } else{
            // Neutral sentiment count
            values[2] += 1*noneutral;
        }
    }

    // Creating canvas ID and heading for the graph
    let canvasid = "analyze-bipolar"
    let heading = "Bipolar sentiment analysis<br>";
    
    // Return value
    return {
        "data": [labels, values],
        "metadata": [canvasid, heading]};
}
//====================================
// Processing data for fine-grained sentiment analysis
function processDataFor_analyze_finegrained(response, n){
    // Processing n (desired number of class intervals)
    n = parseInt(n);
    if(isNaN(n)){
        n = 4;
    } else if(n <= 0){
        n = -n;
    }

    // Processing data
    /*
    The data we in the response is in the format
    [[<text1>, <text2>...], [<sentiment1>, <sentiment2>...]]
    
    We will keep this in mind when performing the operations below.
    This function will classify the sentiments into various class intervals.
    */
    let interval = 2/n;
    // Range of sentiment coefficient is -1 to 1, hence the size of the range is 2.

    let labels = [];
    let values = [];
    // Adding class intervals
    for(i=-1; i<1; i+=interval){
        labels.push(i);
        values.push(0);
    }
    labels.push(1);
    values.push(0);

    // Iterating through and classifying sentiments
    let sentiment = 0;
    for(i=0; i<response.data.length; i++){
        sentiment = response.data[i][1];
        
        // Checking which class interval the sentiment value belongs to
        /*
        Checking starts from the 2nd lowest interval point.
        If sentiment < current interval point, it belongs to previous interval.
        */
        for(j=1; j<labels.length; j++){
            if(sentiment < labels[j]){
                values[j-1]++;
                break;
            }
        }
    }
    
    // Converting labels into strings with fixed precision
    // (so it looks better on the graph)
    for(i=0; i<labels.length; i++){
        labels[i] = labels[i].toFixed(2);
    }

    // Creating canvas ID and heading for the graph
    canvasid = "analyze-finegrained"
    heading = "Finegrained analysis<br>";
    
    // Return value
    return {
        "data": [labels, values],
        "metadata": [canvasid, heading]};
}
//====================================
// Processing user option
function performAnalyzeOption(useropt, response){
    switch(useropt[0]){
        case "bipolar":
            createPieChart(processDataFor_analyze_bipolar(response, useropt[1]));
            break;
        
        case "finegrained":
            createBarChart(processDataFor_analyze_finegrained(response, useropt[1]));
            break;
        
        case "*":
            createPieChart(processDataFor_analyze_bipolar(response, useropt[1]));
            createBarChart(processDataFor_analyze_finegrained(response, useropt[1]));
            break;

    }
}