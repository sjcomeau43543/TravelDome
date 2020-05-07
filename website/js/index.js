/*
Author:        Samantha
Last modified: 5.5.2020 by sjc
Status:        In progress

TODO
format activities
format itinerary
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
var USERadjectives = [];
var USERitinerary = [];
var USERrecommendations;

// page state
var page_state = 1; // 1: search, 2: results, 3: itinerary


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
selectAdjective
add adjective to the list and fixes styling
*/
function selectAdjective(adjective){
    // formatting
    var li = document.getElementById("listitem"+adjective);
    if(li.classList.contains("sams-adjectives-active")){
        // removing adjective
        li.classList.remove("sams-adjectives-active");
        for(var i=0; i<USERadjectives.length; i++){
            if(USERadjectives[i] === adjective) {
                USERadjectives.splice(i, 1);
                break;
            }
        }
    } else {
        // adding adjective
        li.classList.add("sams-adjectives-active");
        USERadjectives.push(adjective);
    }
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
        var li = document.createElement("li");
        li.setAttribute("class", "list-group-item sams-adjectives");
        li.setAttribute("id", "listitem"+adjectives[l]);
        li.setAttribute("onclick", "selectAdjective('"+adjectives[l]+"')");

        var newp = document.createTextNode(adjectives[l]);
        li.appendChild(newp);

        container.appendChild(li);
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

        // add
        USERdestination = x[currentFocus].value;
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

                        // add
                        USERdestination = container.value;
                    });
                
                    b.setAttribute("class", "sams-input-dropdown");
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
    console.log("helloooo");
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
    var temp = {};
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
activityDiv
returns a div element with the activity information embedded
*/
function activityDiv(activity, plusminus) {
    var div = document.createElement("div");
    div.setAttribute("class", "sams-activity-div");

    // nodes
    var container = document.createElement("div");
    container.setAttribute("class", "container");
    
    // row1 holds the title
    var row1 = document.createElement("div");
    row1.setAttribute("class", "row");

    // row2 holds 2 columns
    var row2 = document.createElement("div");
    row2.setAttribute("class", "row");

    // col holds the edit buttons
    var col = document.createElement("div");
    col.setAttribute("class", "col-2");

    // col1 holds the photo album
    var col1 = document.createElement("div");
    col1.setAttribute("class", "col");

    // col2 holds the information
    var col2 = document.createElement("div");
    col2.setAttribute("class", "col");

    // title
    var title = document.createElement("h3");
    var titletext = document.createTextNode(activity.name);
    title.appendChild(titletext);
    row1.appendChild(title);

    // + - buttons
    if(plusminus){
        var add = true;
        for(var i=0; i<USERitinerary.length; i++){
            if(USERitinerary[i].name === activity.name){
                add = false;
            }
        }
        var plus = document.createElement("div");
        if (add) {
            plus.setAttribute("class", "sams-icons sams-plus");
        } else {
            plus.setAttribute("class", "sams-icons sams-minus");
        }
        plus.setAttribute("id", "plus"+activity.name);
        plus.setAttribute("onclick", "addActivity('"+activity.name+"')");
    
        col.appendChild(plus);
    } else {
        var category = document.createElement("div");
        var counts = {};
        var max = 0;
        for (var t=0; t<adjectives.length; t++){
            counts[adjectives[t]] = 0;
        }
        for (var t=0; t<activity.tags.length; t++){
            if(adjectives.indexOf(activity.tags[t]) === -1){
                // synonym
                for (var z=0; z<adjectives.length; z++){
                    if (adjectives_ext[adjectives[z]].indexOf(activity.tags[t]) !== -1){
                        counts[adjectives[z]] = counts[adjectives[z]] + 1;
                        console.log(adjectives[z]);
                    }
                }
            } else {
                counts[activity.tags[t]] = counts[activity.tags[t]] + 1;
                console.log(activity.tags[t]);
            }
        }
        for (var t=0; t<adjectives.length; t++){
            if (counts[adjectives[t]] > max) {
                max = adjectives[t];
            }
        }
        category.setAttribute("class", "sams-categories sams-categories-"+max);
        col.appendChild(category);
    }

    // photo
    for(var i=0; i<activity.photo_location.length; i++){
        var photo = document.createElement("img");
        photo.setAttribute("class", "sams-photoalbum");
        photo.setAttribute("id", "photo"+activity.name);
        if(activity.photo_location[i].includes("http")){
            // url
            photo.setAttribute("src", activity.photo_location[i]);
        } else {
            // downloaded
            photo.setAttribute("src", "Photographs/"+activity.photo_location[i]);
        }
        col1.appendChild(photo);
    }

    // address
    var irow = document.createElement("div");
    irow.setAttribute("class", "row");
    var icon = document.createElement("div");
    icon.setAttribute("class", "sams-icons sams-address");
    irow.appendChild(icon);
    var address = document.createElement("div");
    address.setAttribute("class", "sams-info");
    var address_t = document.createTextNode(activity.address);
    address.appendChild(address_t);
    irow.appendChild(address);
    col2.appendChild(irow);

    // tags
    var irow = document.createElement("div");
    irow.setAttribute("class", "row");
    var icon = document.createElement("div");
    icon.setAttribute("class", "sams-icons sams-menu");
    irow.appendChild(icon);
    var tags = document.createElement("div");
    tags.setAttribute("class", "sams-info");
    var completed = [];
    for(var t = 0; t<activity.tags.length; t++){
        var done = false;
        for(var j=0; j<completed.length; j++){
            if(completed[j] === activity.tags[t]){
                done = true;
            }
        }
        if (done === false){
            var tag = document.createTextNode(activity.tags[t]+" ");
            tags.appendChild(tag);
            completed.push(activity.tags[t]);

        }
    }
    irow.appendChild(tags);
    col2.appendChild(irow);

    // rating
    var irow = document.createElement("div");
    irow.setAttribute("class", "row");
    var icon = document.createElement("div");
    icon.setAttribute("class", "sams-icons sams-stars");
    irow.appendChild(icon);
    var rating = document.createElement("div");
    rating.setAttribute("class", "sams-info");
    var rating_t = document.createTextNode(activity.avg_visitor_review);
    rating.appendChild(rating_t);
    irow.appendChild(rating);
    col2.appendChild(irow);

    // source
    var irow = document.createElement("div");
    irow.setAttribute("class", "row");
    var icon = document.createElement("div");
    icon.setAttribute("class", "sams-icons sams-link");
    irow.appendChild(icon);
    var src = document.createElement("div");
    src.setAttribute("class", "sams-info");
    var src_t = document.createTextNode(activity.source);
    src.appendChild(src_t);
    irow.appendChild(src);
    col2.appendChild(irow);

    // fix nodes
    row2.appendChild(col);
    row2.appendChild(col1);
    row2.appendChild(col2);

    container.appendChild(row1);
    container.appendChild(row2);
    
    div.appendChild(container);

    return div;
}

/* 
generateRecommendations
loads the recommendations into the new site and queries ii
*/
function generateRecommendations(){
    // TODO do we have input?
    if(USERdestination === "" || USERadjectives.length === 0){
        document.getElementById("errormsg").innerHTML = "You need to select a destination and at least one adjective to describe yourself.";
    } else {
        page_state = 2;

        // load new page
        var page = document.getElementById("pageContainerMain");
        var page_loaded = false;
        loadFile("website/results.html", function(response) {
            page.innerHTML = response;
            page_loaded = true;
        });

        // get activities
        var recommendations = queryII(USERdestination, USERadjectives);
        USERrecommendations = recommendations;

        // wait for page to be loaded
        var timeout = setInterval(function(){
            if(page_loaded){
                clearInterval(timeout);
                
                // load the UI
                // put results from II in
                var container = document.getElementById("resultsContainer");
                for (var r=0; r<recommendations.length; r++){
                    var div = activityDiv(recommendations[r], true);

                    container.appendChild(div);
                    container.appendChild(document.createElement("BR"));
                }

            }
        }, 100); 
            
    }

    
}

/*
generateSecondaryRecommendations
loads cluster recommendations using positive feedback
also adds the chosen activity to the list
*/
function generateSecondaryRecommendations(originalActivity){

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
        var div = activityDiv(cleaned_recommendations[r], true);

        container.appendChild(div);
        container.appendChild(document.createElement("BR"));
    } 
}

/*
addActivity
1adds and activity to the itinerary
2changes icon
3generates secondary recommendations
*/
function addActivity(originalActivity){
    // add or remove
    var add = true;
    for(var i=0; i<USERitinerary.length; i++){
        if(USERitinerary[i].name === originalActivity) {
            add = false;
            break;
        }
    }

    
    // edit itinerary
    if(add) {
        for(var i=0; i<USERrecommendations.length; i++){
            if(USERrecommendations[i].name === originalActivity) {
                USERitinerary.push(USERrecommendations[i]);
                break;
            }
        }
    } else {
        for(var i=0; i<USERitinerary.length; i++){
            if(USERitinerary[i].name === originalActivity) {
                USERitinerary.splice(i, 1);
                break;
            }
        }
    }

    // icon
    var icon = document.getElementById("plus"+originalActivity);

    if(add) {
        icon.setAttribute("class", "sams-icons sams-minus");
    } else {
        icon.setAttribute("class", "sams-icons sams-plus");
    }

    // add recommendations
    generateSecondaryRecommendations(originalActivity);

}


/*
generateItinerary
generates the itinerary
*/
function generateItinerary(){
    if(USERdestination === "" || USERadjectives.length === 0){
        document.getElementById("errormsg").innerHTML = "You need to select a destination and at least one adjective to describe yourself.";
    } else {
        // load new page
        var page = document.getElementById("pageContainerMain");
        var page_loaded = false;
        loadFile("website/itinerary.html", function(response) {
            page.innerHTML = response;
            page_loaded = true;        
            page_state = 3;
        });

        // wait for page to be loaded
        var timeout = setInterval(function(){
            if(page_loaded){
                clearInterval(timeout);
                
                // load the UI
                // put the itinerary in
                var container = document.getElementById("itineraryContainer");
                for (var r=0; r<USERitinerary.length; r++){
                    var div = activityDiv(USERitinerary[r], false);

                    container.appendChild(div);
                    container.appendChild(document.createElement("BR"));
                }

            }
        }, 100); 
    }
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

            // load the current stuff
            if(USERdestination !== ""){

                document.getElementById("locationContainer").value = USERdestination;

                var list_of = document.getElementById("adjectivesContainer").childNodes;
                for(var c=0; c<list_of.length; c++){
                    for (var d=0; d<USERadjectives.length; d++){
                        if("listitem"+USERadjectives[d] === list_of[c].id){
                            list_of[c].classList.add("sams-adjectives-active");
                        }
                    }
                }
            }

        }
    }, 100); 
}
/*
backToResults
goes back to the results page
*/
function backToResults(){
    if(USERdestination === "" || USERadjectives.length === 0){
        document.getElementById("errormsg").innerHTML = "You need to select a destination and at least one adjective to describe yourself.";
    } else {
        // load new page
        var page = document.getElementById("pageContainerMain");
        var page_loaded = false;
        loadFile("website/results.html", function(response) {
            page.innerHTML = response;
            page_loaded = true;
        });

        // get activities
        console.log(USERadjectives);
        var recommendations = queryII(USERdestination, USERadjectives);
        USERrecommendations = recommendations;

        // wait for page to be loaded
        var timeout = setInterval(function(){
            if(page_loaded){
                clearInterval(timeout);
                
                // load the UI
                // put results from II in
                var container = document.getElementById("resultsContainer");
                for (var r=0; r<recommendations.length; r++){
                    var div = activityDiv(recommendations[r], true);

                    container.appendChild(div);
                    container.appendChild(document.createElement("BR"));
                }

            }
        }, 100);

    } 
}

/*
saveItinerary
downloads PDF version

TODO maybe
*/
function saveItinerary(){

}

/* 
restart
removes all data
*/
function restart() {
    USERdestination = "";
    USERadjectives = [];
    USERitinerary = [];

    backToForm();
}