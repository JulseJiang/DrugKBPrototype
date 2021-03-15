function show(array)
{
    const cy = window.cy = cytoscape({
        container: document.getElementById('cy'),
        boxSelectionEnabled: false,
        autounselectify: true,
    style: [
        {
          selector: 'node[group=\"attr\"]',
          style: {
            'content': 'data(name)',
			"width": "80px",
			"height": "80px",
			"font-size": "40px",
			"text-valign": "center",
			"text-halign": "center",
			"background-color": "#0966ab",
			"text-outline-color": "#0966ab",
			"text-outline-width": "6px",
			"color": "#fff",
			"overlay-padding": "6px",
			"z-index": "10"
          }
        },
		  {
          selector: 'node[group=\"core\"]',
          style: {
            'content': 'data(name)',
			"width": "160px",
			"height": "160px",
			"font-size": "60px",
			"text-valign": "center",
			"text-halign": "center",
			"background-color": "#793c39",
			"text-outline-color": "#793c39",
			"text-outline-width": "6px",
			"color": "#fff",
			"overlay-padding": "6px",
			"z-index": "10"
          }
        },

        {
          selector: 'edge',
          style: {
            'curve-style': 'haystack',
            'haystack-radius': 0,
            'width': 1,
            'line-color': '	#ffcc33'
          }
        }
      ],
    });
    for (var i=0; i < array.length; i++)
    {
	    cy.add(array[i]);
    }
var layout = cy.layout({
  name: 'concentric',
  fit: true, // whether to fit the viewport to the graph
  padding: 30, // the padding on fit
  startAngle: 3 / 2 * Math.PI, // where nodes start in radians
  sweep: undefined, // how many radians should be between the first and last node (defaults to full circle)
  clockwise: true, // whether the layout should go clockwise (true) or counterclockwise/anticlockwise (false)
  equidistant: false, // whether levels have an equal radial distance betwen them, may cause bounding box overflow
  minNodeSpacing: 10, // min spacing between outside of nodes (used for radius adjustment)
  boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
  nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
  height: undefined, // height of layout area (overrides container height)
  width: undefined, // width of layout area (overrides container width)
  spacingFactor: undefined, // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
  concentric: function( node ){ // returns numeric value for each node, placing higher nodes in levels towards the centre
  return node.degree();
  },
  levelWidth: function( nodes ){ // the letiation of concentric values in each level
  return nodes.maxDegree() / 4;
  },
  animate: false, // whether to transition the node positions
  animationDuration: 500, // duration of animation in ms if enabled
  animationEasing: undefined, // easing of animation if enabled
  animateFilter: function ( node, i ){ return true; }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
  ready: undefined, // callback on layoutready
  stop: undefined, // callback on layoutstop
  transform: function (node, position ){ return position; }
 });
layout.run();
cy.on('tap', 'node', function(){
  try { // your browser may block popups
    window.open( this.data('href') );
  } catch(e){ // fall back on url change
    window.location.href = this.data('href');
  }
});

}

