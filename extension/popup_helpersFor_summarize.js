// Processing data for wordcloud
function processDataFor_summarize_wordcloud(response){
    // Processing data
    /*
    The data we in the response is in the format
    [
        [<word1>, <freq1>],
        [<word2>, <freq2>]
        ...
    ]
    We will keep this in mind when performing the operations below.
    Note that this function finds the proportion of times that a word appears,
    rather the actual frequencies. Such data is useful in word cloud graphs
    that do not scale the words based on proportional frequency (such as the one I'm using),
    since such scaled data ensures a more or less constant size for the word cloud,
    while visual accuracy is mostly maintained.
    */
    let data = JSON.parse(JSON.stringify(response.data));
    let totalWordCount = data.length;
    for(i=0; i<totalWordCount; i++){
        // Converting the tuple pair to list pair to make it mutable
        data[i][1] = 3000 * data[i][1] / totalWordCount;
    }
    
    // Creating canvas ID and heading for the graph
    let canvasid = "summarize-wordcloud";
    let heading = "Word cloud";

    // Return value
    return {
        "data": data,
        "metadata": heading};
}
//====================================
function processDataFor_summarize_freqdist(response, n){
    // Processing n (desired number of bar chart labels)
    n = parseInt(n);
    if(isNaN(n)){
        n = 10;
    } else if(n <= 0){
        n = -n;
    }

    // Processing the data
    /*
    The data we in the response is in the format
    [
        [<word1>, <freq1>],
        [<word2>, <freq2>]
        ...
    ]
    But for Chart.js, we need
    [<word1>, <word2> ...]
    [<freq1>, <freq2> ...]
    */
    let labels = [];
    let values = []
    for(i=0; i<n; i++){
        labels.push(response.data[i][0]);
        values.push(response.data[i][1]);
    }
    
    // Creating heading for the graph
    

    // Creating canvas ID and heading for the graph
    let canvasid = "summarize-freqdist";
    let heading = "Word frequency distribution<br>";

    // Return value
    return {
        "data": [labels, values],
        "metadata": [canvasid, heading]};
}
//====================================
// Processing user option
function performSummaryOption(useropt, response){
    switch(useropt[0]){
        case "wordcloud":
            createWordCloud(processDataFor_summarize_wordcloud(response));
            break;
        
        case "freqdist":
            createBarChart(processDataFor_summarize_freqdist(response, useropt[1]));
            break;
        
        case "*":
            createWordCloud(processDataFor_summarize_wordcloud(response));
            createBarChart(processDataFor_summarize_freqdist(response, useropt[1]));
            break;

    }
}