/*
Author:        Samantha
Last modified: 5.1.2020 by sjc
Status:        In progress
*/

// recommendations
var inverted_index;
var cluster_recommendations;

// activity information
var merged_location_data = [];

// adjectives and locations
var adjectives = [];
var adjectives_ext = [];
var locations = [];


/*
loadFile
loads files
*/
function loadFile(filename, callback) {
    var xobj = new XMLHttpRequest();

    xobj.overrideMimeType("application/json");
    xobj.open("GET", "../../"+filename, true);
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
        var comma_response = str_response.split(",");
        for(var i=0; i<comma_response.length; i++){
            var objs = comma_response[i].split("\n");
            for (var j=0; j<objs.length; j++){
                adjectives_ext.push(objs[j].replace(/ /g, ""));

            }
        }
        console.log(adjectives_ext);
    });
    // load adjectives
    loadFile("scrapers/adjectives.txt", function(response) {
        var str_response = String(response);
        var comma_response = str_response.split("\n");
        for(var i=0; i<comma_response.length; i++){
            adjectives.push(comma_response[i].replace(/ /g, ""));
        }
        console.log(adjectives);
    });
    // load locations
    loadFile("scrapers/locations.txt", function(response) {
        var str_response = String(response);
        var comma_response = str_response.split("\n");
        for(var i=0; i<comma_response.length; i++){
            locations.push(comma_response[i].replace(/ /g, ""));
        }
        console.log(locations);
    });

    // load the inverted index
    loadFile("data/Cluster/neighbors.json", function(response) {
        cluster_recommendations = JSON.parse(response);
    });

    // load clustering recommendations
    loadFile("data/InvertedIndex/inverted_index.json", function(response) {
        inverted_index = JSON.parse(response);
    });

    // load location data TODO
    var i = 0;
    /* loadFile("data/InvertedIndex/inverted_index.json", function(response) {
        inverted_index = JSON.parse(response);
    }); */

}


loadData()