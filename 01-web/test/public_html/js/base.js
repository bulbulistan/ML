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
        $("#results-graph").append('<svg id="graphcanvas" width="800" height="600" class="none"></svg>');
        $("#results-graph").append('<script src="js/visualize.js"></script>');
        $("#results-graph").removeClass("none");
        $("#graphcanvas").removeClass("none");                           

    });
});