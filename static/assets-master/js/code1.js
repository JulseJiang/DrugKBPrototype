function show(array)
{
    alert("成功调用show方法！");
    const cy = window.cy = cytoscape({
        container: document.getElementById('cy'),
        boxSelectionEnabled: false,
        autounselectify: true,
        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(id)',
                    'font-size': 8,
                    'background-color': '#ea8a31'
                }
            },

            {
                selector: 'edge',
                style: {
                    'curve-style': 'haystack',
                    'haystack-radius': 0,
                    'width': 3,
                    'line-color': '#fcc694'
                }
            }
        ],
    });
    for (var i=0; i < array.length; i++)
{
	cy.add(array[i])
}
var layout = cy.layout({
name: 'circle',
   fit: true,
   ready: undefined,
   stop: undefined,
   rStepSize: 10,
   padding: 30,
   startAngle: 3/2 * Math.PI,
   counterclockwise: false

 });
layout.run();
}
