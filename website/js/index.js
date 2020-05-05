/*
Author:        Samantha
Last modified: 5.5.2020 by sjc
Status:        In progressa
*/

// recommendations
var inverted_index;
var cluster_recommendations;

// activity information
var merged_location_data = []; // {location:activities}

// adjectives and locations
var adjectives = new Array();
var adjectives_ext = {}; // {mainadj:synonyms}
var locations = new Array();

// user specific
var USERdestination;
var USERadjectives;
var USERitinerary = [];
var USERrecommendations;

/*
loadFile
loads files
*/
function loadFile(filename, callback) {
    var xobj = new XMLHttpRequest();

    xobj.overrideMimeType("application/json");
    xobj.open("GET", "../../"+filename, true); // change to ../../ for local https://sjcomeau43543.github.io/TravelDome/ for online
    xobj.onreadystatechange = function () {
        if(xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }

    };
    xobj.send(null);
}

/*
loadData
loads all the data for the recommender
*/
function loadData() {
    // load adjectives_ext
    loadFile("scrapers/adjectives_extended.txt", function(response) {
        var str_response = String(response);
        var comma_response = str_response.split("\n");
        for(var i=0; i<comma_response.length; i++){
            var objs = comma_response[i].split(",");
            adjectives_ext[objs[0].replace(/ /g, "")] = [];
            for (var j=1; j<objs.length; j++){
                adjectives_ext[objs[0].replace(/ /g, "")].push(objs[j].replace(/ /g, ""));

            }
        }
    });
    // load adjectives
    loadFile("scrapers/adjectives.txt", function(response) {
        var str_response = String(response);
        var comma_response = str_response.split("\n");
        for(var i=0; i<comma_response.length; i++){
            adjectives.push(comma_response[i].replace(/ /g, ""));
        }
    });
    // load locations
    var done_locations=0;
    loadFile("scrapers/locations.txt", function(response) {
        var str_response = String(response);
        var comma_response = str_response.split("\n");
        for(var i=0; i<comma_response.length; i++){
            locations.push(comma_response[i].replace(/ /g, "").replace(/,/g, ""));
        }
        var timeout = setInterval(function(){
            clearInterval(timeout);
            done_locations=1;
        }, 500);
    });

    // load clustering recommendations
    loadFile("data/Cluster/neighbors.json", function(response) {
        cluster_recommendations = JSON.parse(response);
    });

    // load the inverted index
    loadFile("data/InvertedIndex/inverted_index.json", function(response) {
        inverted_index = JSON.parse(response);
    });

    // load location data
    // wait for location data to be loaded
    var timeout = setInterval(function(){
        if(done_locations){
            clearInterval(timeout);

            // get data
            for(var i=0; i<locations.length; i++){
                loadFile("data/Merged/"+locations[i].replace(/,/g, "")+".json", function(response) {
                    merged_location_data.push(JSON.parse(response));
                });
            }

        }
    }, 100); 

}

/*
loadAdjectives
loads the adjectives into the selectors
*/
function loadAdjectives(){
    // place to add them
    var container = document.getElementById("adjectivesContainer");

    

    // add the elements
    var l;
    for(l=0; l<adjectives.length; l++){
        var input = document.createElement("input");
        input.setAttribute("class", "activity_input");
        input.setAttribute("type", "checkbox");
        input.setAttribute("id", "checkbox"+adjectives[l]);

        var label = document.createElement("label");
        label.setAttribute("class", "form-check-label");
        label.setAttribute("for", "checkbox"+adjectives[l]);

        var newp = document.createTextNode(adjectives[l]);
        label.appendChild(newp);

        container.appendChild(input);
        container.appendChild(label);
        container.appendChild(document.createElement("BR"));
    }
}

/* 
loadLocations
loads the locations into the auto complete filler

adapted from w3schools tutorial
*/
function loadLocations(){
    // closes the list
    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != container) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    // removes active class from items    
    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    // adds active class
    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    // place to add them
    var container = document.getElementById("locationContainer");

    // event listener on input by user
    container.addEventListener("input", function(e) {
        var a, b, i, val = this.value;

        closeAllLists();

        currentFocus = -1;/*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(a);
        for (i = 0; i < locations.length; i++) {
          if (locations[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            b = document.createElement("DIV");
            b.innerHTML = "<strong>" + locations[i].substr(0, val.length) + "</strong>";
            b.innerHTML += locations[i].substr(val.length);
            b.innerHTML += "<input type='hidden' value='" + locations[i] + "'>";
                b.addEventListener("click", function(e) {
                container.value = this.getElementsByTagName("input")[0].value;
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });

    // event listener on arrow by user
    container.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) { // UP
          currentFocus++;
          addActive(x);
        } else if (e.keyCode == 38) { // DOWN
          currentFocus--;
          addActive(x);
        } else if (e.keyCode == 13) { // ENTER
          e.preventDefault();
          if (currentFocus > -1) {
            if (x) x[currentFocus].click();
          } 
        } else if (e.keyCode == 8) { // BACKSPACE
            // refresh
        }
    });

    // event listener on document by user
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });

}



function main(){
    // load form content
    var page = document.getElementById("pageContainerMain");
    loadFile("website/form.html", function(response) {
        page.innerHTML = response;
    });

    // load our data
    loadData();

    // wait for data to be loaded
    var timeout = setInterval(function(){
        if(adjectives.length){
            clearInterval(timeout);
            
            // load the UI
            loadAdjectives();
            loadLocations();

        }
    }, 100); 
}

main();

/*
queryCluster
gets recommendations from the cluster
*/
function queryCluster(originalActivity){
    var recommendations_scored = cluster_recommendations[originalActivity];

    var recommendations = [];
    var index = locations.indexOf(USERdestination);

    // get recommendation names
    for(var i=0; i<recommendations_scored.length; i++){
        for(var j=0; j<merged_location_data[index].length; j++){
            if (recommendations_scored[i][0] == merged_location_data[index][j].name){
                recommendations.push(merged_location_data[index][j]);
                break;
            }
        }
    }

    return recommendations;
}

/* 
queryII
queries the inverted index with the personality adjectives, combines the lists, and filters on location
*/
function queryII(destination, personality) {
    // inverted index stores all adjectives
    var query_terms = [];

    // handle synonyms
    for(var i=0; i<personality.length; i++) {
        // add it
        query_terms.push(personality[i]);

        // synonyms
        for(var j=0; j<adjectives_ext[personality[i]].length; j++){
            query_terms.push(adjectives_ext[personality[i]][j]);
        }

    }

    // get inverted index recommendations
    var activities_ii = [];

    for(var k=0; k<query_terms.length; k++){
        a_intermediate = inverted_index[query_terms[k]];
        for(var a=0; a<a_intermediate.length; a++){
            activities_ii.push(a_intermediate[a]);
        }
    }

    // filter on location
    var index = locations.indexOf(destination);
    var activities_results = [];
    for(var i=0; i<activities_ii.length; i++){
        for(var j=0; j<merged_location_data[index].length; j++){
            if (activities_ii[i] == merged_location_data[index][j].name){
                activities_results.push(merged_location_data[index][j]);
                break;
            }
        }
    }

    // remove duplicates
    // location.tags: fun, funny, this would return this location twice
    var activities_results_cleaned = [];
    for(var i=0; i<activities_results.length; i++){
        if(activities_results_cleaned.indexOf(activities_results[i]) === -1){
            // does not exist yet
            activities_results_cleaned.push(activities_results[i]);
        }
    }

    return activities_results_cleaned;
}

/* 
generateRecommendations
loads the recommendations into the new site and queries ii
*/
function generateRecommendations(){
    // get form information
    var form = document.getElementById("form");

    var destination = form[0].value.replace(/,/g,"");
    USERdestination = destination;

    var personality = [];
    for(var i=1; i<adjectives.length+1; i++){
        if(form[i].checked){
            personality.push(adjectives[i-1]);
        }
    }
    USERadjectives = personality;

    // load new page
    var page = document.getElementById("pageContainerMain");
    var page_loaded = false;
    loadFile("website/results.html", function(response) {
        page.innerHTML = response;
        page_loaded = true;
    });

    // get activities
    var recommendations = queryII(destination, personality);
    USERrecommendations = recommendations;

    // wait for page to be loaded
    var timeout = setInterval(function(){
        if(page_loaded){
            clearInterval(timeout);
            
            // load the UI
            // put results from II in
            var container = document.getElementById("resultsContainer");
            for (var r=0; r<recommendations.length; r++){
                var div = document.createElement("div");
                div.setAttribute("onClick", "generateSecondaryRecommendations('"+recommendations[r].name+"')");
                div.setAttribute("id", "results"+recommendations[r].name);

                var newp = document.createTextNode(recommendations[r].name);
                div.appendChild(newp);

                container.appendChild(div);
                container.appendChild(document.createElement("BR"));
            }

        }
    }, 100); 

    
}

/*
generateSecondaryRecommendations
loads cluster recommendations using positive feedback
also adds the chosen activity to the list
*/
function generateSecondaryRecommendations(originalActivity){
    // add to itinerary
    for(var i=0; i<USERrecommendations.length; i++){
        if(USERrecommendations[i].name === originalActivity) {
            // TODO is it already in the itinerary?
            USERitinerary.push(USERrecommendations[i]);
            break;
        }
    }

    // get activities
    var recommendations = queryCluster(originalActivity);
    var cleaned_recommendations = [];

    // remove duplicates
    for(var i = 0; i < recommendations.length; i++){
        for(var j=0; j < USERrecommendations.length; j++){
            if(USERrecommendations[j].name === recommendations[i].name) {
                // has already been recommended
                break;
            } else if (USERrecommendations.length === (j+1)) {
                // being recommended now
                USERrecommendations.push(recommendations[i]);
                cleaned_recommendations.push(recommendations[i]);
                break;
            }
        }
        
    }

    
    // put results from clusters in
    var container = document.getElementById("resultsContainer");
    for (var r=0; r<cleaned_recommendations.length; r++){
        var div = document.createElement("div");
        div.setAttribute("onClick", "generateSecondaryRecommendations('"+cleaned_recommendations[r].name+"')");
        div.setAttribute("id", "results"+cleaned_recommendations[r].name);

        var newp = document.createTextNode(cleaned_recommendations[r].name);
        div.appendChild(newp);

        container.appendChild(div);
        container.appendChild(document.createElement("BR"));
    } 
}

/*
generateItinerary
generates the itinerary
*/
function generateItinerary(){
    console.log(USERitinerary);
    return; // TODO
}

/*
backToForm
goes back to the form for the user without removing the results
*/
function backToForm(){
    var loaded = 0;
    // load form page
    var page = document.getElementById("pageContainerMain");
    loadFile("website/form.html", function(response) {
        page.innerHTML = response;
        loaded = 1;
    });

    var timeout = setInterval(function(){
        if(loaded){
            clearInterval(timeout);

            // load the UI
            loadAdjectives();
            loadLocations();

        }
    }, 100); 
}