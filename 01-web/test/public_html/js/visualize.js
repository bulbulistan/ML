var words =
        '{"\u0715\u072b\u0712\u072c\u0710": [22.970568, -55.150795, 0.8438752293586731], "\u0720\u0720\u071d\u0710": [22.54365, -55.390007, 0.8229877352714539], "\u0715\u071d\u0718\u0721\u0710": [22.774284, -55.03659, 0.786860466003418], "\u0712\u071d\u0718\u0721\u0710": [22.899626, -55.505302, 0.7759663462638855], "\u0710\u071d\u0721\u0721\u0710": [22.54992, -55.227203, 0.7568687200546265], "\u072a\u0721\u072b\u0710": [22.600311, -55.212658, 0.7558534145355225], "\u0719\u0725\u0718\u072a\u0710": [17.882496, -48.463985, 0.7196277379989624], "\u0725\u0715\u0722\u0710": [18.237576, -48.52058, 0.7174093127250671], "\u0720\u071d\u0718\u0721\u0710": [49.5275, -9.709123, 0.7167130708694458], "\u0718\u0720\u0720\u071d\u0710": [21.848179, -51.4507, 0.7158464789390564]}';
// this is the main data
// list of three-piece list - x, y, label

//https://www.tutorialsteacher.com/d3js/loading-data-from-file-in-d3js
var max = 75; // maximum of x and y    
var min = 0 - max;

// dimensions and margins
var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        width = 0.8 * width;
height = 0.8 * height;
var margin = {top: (0.1 * width), right: (0.1 * width), bottom: (0.1 * width), left: (0.1 * width)};

// create a clipping region 
svg.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);

// create scale objects
var xScale = d3.scaleLinear()
        .domain([min, max])
        .range([min, width]);
var yScale = d3.scaleLinear()
        .domain([min, max])
        .range([height, min]);
// create axis objects
var xAxis = d3.axisBottom(xScale)
        .ticks(20, "s");
var yAxis = d3.axisLeft(yScale)
        .ticks(20, "s");
// Draw Axis
var gX = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + (margin.top + height) + ')')
        .call(xAxis);
var gY = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(yAxis);

// Draw Datapoints
var points_g = svg.append("g")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .attr("clip-path", "url(#clip)")
        .classed("points_g", true);


// get data
var xdata = [];

// process data
var processedWords = jQuery.parseJSON(words);
var coordkeys = Object.keys(processedWords);

for (var u = 0; u < coordkeys.length; u++)
{
    coordkey = coordkeys[u];
    console.log(coordkey);
    xdatapoint = {};
    xdatapoint["x"] = processedWords[coordkey][0];
    xdatapoint["y"] = processedWords[coordkey][1];
    xdatapoint["label"] = coordkey;
    xdata.push(xdatapoint);
}

var points_all = []; //node
var data = [];
var labels_all = []; //label

// http://bl.ocks.org/MoritzStefaner/1377729
var labelDistance = 0;

var points = points_g.selectAll("circle")
        .data(xdata)
        .enter()
        .append("circle")
        .attr('cx', function (d) {
            return xScale(d.x);
        })
        .attr('cy', function (d) {
            return yScale(d.y);
        })
        .attr('r', 3)
        .attr("fill", "red");

var labels = points_g.selectAll("text")
        .data(xdata)
        .enter()
        .append("text")
        .text(function (d) {
            return d.label;
        })
        .attr("x", function (d) {
            return xScale(d.x) + 3;
        })
        .attr("y", function (d) {
            return yScale(d.y);
        })
        .attr("font-size", "22px")
        .attr("class", "text");


points_all = points;
labels_all = labels;
data = xdata;
//console.log(Object.values(labels));

// Pan and zoom
var zoom = d3.zoom()
        .scaleExtent([.5, 300])
        .extent([[0, 0], [width, height]])
        .on("zoom", zoomed);

svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(zoom);

function zoomed() {
    // create new scale ojects based on event
    var new_xScale = d3.event.transform.rescaleX(xScale);
    var new_yScale = d3.event.transform.rescaleY(yScale);
    // update axes
    gX.call(xAxis.scale(new_xScale));
    gY.call(yAxis.scale(new_yScale));
    points_all.data(data)
            .attr('cx', function (d) {
                return new_xScale(d.x);
            })
            .attr('cy', function (d) {
                return new_yScale(d.y);
            });
    labels_all.data(data)
            .attr('x', function (d) {
                return new_xScale(d.x) + 3;
            })
            .attr('y', function (d) {
                return new_yScale(d.y);
            });
}