// POPUP GRAPHICS FUNCTIONS
/*
1. createWordCloud
2. createBarChart
3. createPieChart
*/
//====================================
// Small cosmetic helper function to add headings to the graphs
function addHeading(tag, text){
    // Creating some space before
    spacing = document.createElement("p")
    spacing.innerHTML = "<br><br>"
    document.body.appendChild(spacing);

    // Creating heading
    heading = document.createElement(tag);
    heading.innerHTML = text;
    document.body.appendChild(heading);
}
//====================================
// Function to create word cloud
function createWordCloud(dataset){
    // Extracting heading and data
     let heading = dataset.metadata;
     let data = dataset.data;

    // Creating a wordcloud using '.wordcloud/wordcloud2.js'
    // The above script file is included before this popup script in the 'popup.html' file.
    // Hence, we can access the required functions when the popup page is running.
    
    // Creating a canvas object within 'popup.html'
    // (And adding it to the popup page DOM)
    // First we check if the element with the required ID already exists
    let canvas = document.getElementById("wordcloud");
    // Adding the required canvas element if it doesn't already exist
    if(canvas == null){
        // Adding heading first
        addHeading("h2", heading);

        // Now creating the canvas
        canvas = document.createElement("canvas");
        canvas.id = "wordcloud";
        document.body.appendChild(canvas);
    }
    
    // Creating wordcloud within above canvas
    WordCloud(canvas, {list: data});
    /*
    ALTERNATE CODE FOR CONCEPTUAL CLARITY:
    WordCloud(document.getElementById('wordcloud'), {list: message.report});
    */
}
//====================================
// Function to create bar chart for word frequencies
// Reference: https://www.educative.io/edpresso/chartjs---create-a-histogram
function createBarChart(dataset, n){
    // Extracting canvas ID, heading and data
    let canvasid = dataset.metadata[0];
    let heading = dataset.metadata[1];
    let labels = dataset.data[0];
    let values = dataset.data[1];

    // Data object
    let data = {
        "labels": labels,
        "datasets": [{
                "backgroundColor": ['rgb(255, 0, 255)'],
                "data": values
            }]};
    
    // Options object
    let options = {"plugins" : {"legend": {"display": false}}}
    // "plugins" : {"legend": {"display": false} hides chart label.
    
    // Configuration object
    let config = {
        "type": 'bar',
        "data": data,
        "options": options};
    //------------------------
    // Creating a bar chart using '.chart/chart.js'
    // The above script file is included before this popup script in the 'popup.html' file.
    // Hence, we can access the required functions when the popup page is running.
    
    // Creating a canvas object within 'popup.html'
    // (And adding it to the popup page DOM)
    // First we check if the element with the required ID already exists
    let canvas = document.getElementById(canvasid);
    // Adding the required canvas element if it doesn't already exist
    if(canvas == null){
        // Adding heading first
        addHeading("h2", heading);

        // Now creating the canvas
        canvas = document.createElement("canvas");
        canvas.id = canvasid;
        document.body.appendChild(canvas);
    } else{
        // In this case, canvas element already exists...
        // Destroying previous Chart instances (if any) created for the canvas element
        previousChart = Chart.getChart(canvas);
        
        // If previous chart exists i.e. is not undefined, destroy it...
        if (previousChart != undefined){
            previousChart.destroy();
        }
    }
    /*
    NOTE ON Chart.js AND REUSING CANVAS ELEMENT
    Reference: https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas
    
    Unlike the word cloud function we used, we cannot simply add the new chart
    to the same canvas element if we had already added an instance to it.
    This is because the canvas element for which the chart object
    was created acts as a unique key for the chart object, hence preventing other chart
    objects from using the same key i.e. canvas element.
    
    Applying .destroy to a chart object destroys a created chart instance.
    This will clean up any references stored in the chart object,
    along with any associated event listeners attached to the JavaScript code
    by the 'Chart.js' library. This must be called before the canvas is reused for a new chart.

    To obtain the previous chart object created for the given canvas element,
    we shall use the function 'getChart' defined in the 'chart.js' module, called as

    Chart.getChart(key)
    
    Here, key refers to the canvas element. It can be any one of the following:
    - String denoting the ID of the canvas element
    - HTML DOM element object (HTMLElement)
    - CanvasRenderingContext2D object
    */
    
    // Creating new bar chart within above canvas
    chart = new Chart(canvas, config);
}
//====================================
// Function to create binary pie chart
function createPieChart(dataset){
    // Extracting canvas ID, heading and data
    let canvasid = dataset.metadata[0];
    let heading = dataset.metadata[1];
    let labels = dataset.data[0];
    let values = dataset.data[1];

    // Data object
    let data = {
        "labels": labels,
        "datasets": [{
                "backgroundColor": ['rgb(0, 0, 255)', 'rgb(255, 0, 0)', 'rgb(0, 255, 0)'],
                "data": values
            }]};
    
    // Configuration object
    let config = {
        "type": 'pie',
        "data": data,
        "options": {}};

    // Creating a pie chart using '.chart/chart.js'
    // The above script file is included before this popup script in the 'popup.html' file.
    // Hence, we can access the required functions when the popup page is running.
    
    // Creating a canvas object within 'popup.html'
    // (And adding it to the popup page DOM)
    // First we check if the element with the required ID already exists
    let canvas = document.getElementById(canvasid);
    // Adding the required canvas element if it doesn't already exist
    if(canvas == null){
        // Adding heading first
        addHeading("h2", heading);

        // Now creating the canvas
        canvas = document.createElement("canvas");
        canvas.id = canvasid;
        document.body.appendChild(canvas);
    } else{
        // In this case, canvas element already exists...
        // Destroying previous Chart instances (if any) created for the canvas element
        previousChart = Chart.getChart(canvas);
        
        // If previous chart exists i.e. is not undefined, destroy it...
        if (previousChart != undefined){
            previousChart.destroy();
        }
    }
    /*
    NOTE ON Chart.js AND REUSING CANVAS ELEMENT
    Reference: https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas

    Discussed in detail for the previous function.
    */
    
    // Creating new bar chart within above canvas
    chart = new Chart(canvas, config);
}