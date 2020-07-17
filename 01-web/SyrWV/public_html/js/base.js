$(document).ready(function () { //begin    

    $(':input')
            .not(':button, :submit, :reset, :hidden')
            .val('')
            .prop('checked', false)
            .prop('selected', false);

    function hasJsonStructure(str) {
        if (typeof str !== 'string')
            return false;
        try {
            const result = JSON.parse(str);
            const type = Object.prototype.toString.call(result);
            return type === '[object Object]'
                    || type === '[object Array]';
        } catch (err) {
            return false;
        }
    }


    $("#gobutton").click(function () {
        $("#results-graph").empty();
        $("#results-graph").addClass("none");
        var iw = $("#inputword").val();
        iw = iw.replace(/\s/g, '');
        console.log("The queried word is " + iw);
        $("#results").removeClass("none");
        $("#results-table").html("<div class='loader'></div");
        $.ajax({
            url: "run.cgi",
            type: "POST",
            async: true,
            data: {'input_word': iw},
            success: function (response) {
                if (hasJsonStructure(response) === true) {
                    console.log("The query result is json");                                        
                    var results = jQuery.parseJSON(response);
                    window.localStorage.setItem("1", response);
                    console.log("The query result is parsed to " + results);
                    var keys = Object.keys(results);
                    var table = document.createElement("table");
                    for (var i = 0; i < keys.length; i++)
                    {
                        var key = keys[i];
                        
                        row = document.createElement("tr");
                        wordcell = document.createElement("td");
                        wordcell.append(key);
                        row.append(wordcell);
                        
                        distance = results[key][2];
                        distancecell = document.createElement("td");
                        distancecell.append(distance);
                        row.append(distancecell);                       
                        
                        table.append(row);                 
                    }

                    $("#results-table").html("<div class='tableinfo'>Top 10 words most similar to " + "<b>" + iw + "</b>" + "</div>");
                    $("#results-table").append(table);
                    $("#results-graph").append('<svg id="graphcanvas" width="800" height="600" class="none"></svg>');
                    $("#results-graph").append('<script src="js/visualize.js"></script>');
                    $("#results-graph").removeClass("none");
                    $("#graphcanvas").removeClass("none");                    
                } else {
                    $("#results-table").html(response);
                }
            },
            error: function (errorlog) {
                $("#results-table").html(errorlog);
            }
        });

    });
});