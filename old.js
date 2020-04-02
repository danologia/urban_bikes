function set_view_force_dynamic() {
    var i = 0;
    function ticked() {
        i = i+1
        console.log(i)

        if (i==100) {
            downloadObjectAsJson(nodes, "nodes.json")
        }
        
        nodes
            .style("fill","#95DACF")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("r", 3);

        edges
            .style("stroke-width",d => 0.3*Math.log(d.weight))
            .style("stroke", d => "#E82127" + Math.floor(254*d.weight/1978 + 1).toString(16).padStart(2, "0"))
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);
    }

    var simulation = d3.forceSimulation(nodes_data)
            .force('link', d3.forceLink().id(d => d.id).links(edges_data).strength(d => d.weight/300))
            .force('charge', d3.forceManyBody().strength(d => -0.03 * Math.pow(d.betweenness, 2)))
            .force('center', d3.forceCenter(1920 / 2, 1080 / 2))
            .on('tick', ticked);
}

function reset_view_force_dynamic() {
    min_x = Infinity
    min_y = Infinity
    max_x = 0
    max_y = 0

    for (station of nodes_data) {
        x = station.x
        y = station.y

        min_x = Math.min(x, min_x)
        min_y = Math.min(y, min_y)

        max_x = Math.max(x, max_x)
        max_y = Math.max(y, max_y)
    }

    svg .attr("width", (max_x - min_x))
        .attr("height", (max_y - min_y))
        .style("left", min_x)
        .style("top", min_y);

    g.attr("transform", "translate(" + -min_x + "," + -min_y + ")");

    set_view_force_dynamic()
}

function reset_view_map() {
    let x_func = d => map.latLngToLayerPoint(new L.LatLng(d.lat, d.lng)).x
    let y_func = d => map.latLngToLayerPoint(new L.LatLng(d.lat, d.lng)).y    
    let x1_func = d => map.latLngToLayerPoint(new L.LatLng(d.source_node.lat, d.source_node.lng)).x
    let y1_func = d => map.latLngToLayerPoint(new L.LatLng(d.source_node.lat, d.source_node.lng)).y    
    let x2_func = d => map.latLngToLayerPoint(new L.LatLng(d.source_node.lat, d.source_node.lng)).x
    let y2_func = d => map.latLngToLayerPoint(new L.LatLng(d.source_node.lat, d.source_node.lng)).y    

    min_x = Infinity
    min_y = Infinity
    max_x = 0
    max_y = 0

    for (station of nodes_data) {
        x = x_func(station)
        y = y_func(station)

        min_x = Math.min(x, min_x)
        min_y = Math.min(y, min_y)

        max_x = Math.max(x, max_x)
        max_y = Math.max(y, max_y)
    }

    svg .attr("width", (max_x - min_x))
        .attr("height", (max_y - min_y))
        .style("left", min_x)
        .style("top", min_y);


    g.attr("transform", "translate(" + -min_x + "," + -min_y + ")");

    edges
        .attr("x1", x1_func)
        .attr("y1", y1_func)
        .attr("x2", x2_func)
        .attr("y2", y2_func);

    nodes
        .attr("cx", x_func)
        .attr("cy", y_func);
}