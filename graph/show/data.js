/*
 * @Author: Logic
 * @Date: 2022-04-27 10:42:29
 * @LastEditTime: 2022-04-27 16:26:59
 * @FilePath: \pyFuncs\graph\show\data.js
 * @Description:
 */
// Add the nodes option through an event call. We want to start with the parent
// item and apply separate colors to each child element, then the same color to
// grandchildren.
Highcharts.addEvent(
  Highcharts.seriesTypes.networkgraph,
  "afterSetOptions",
  function (e) {
    var colors = Highcharts.getOptions().colors,
      i = 0,
      nodes = {};
    e.options.data.forEach(function (link) {
      // if (link[0] === "Proto Indo-European") {
      //   nodes["Proto Indo-European"] = {
      //     id: "Proto Indo-European",
      //     marker: {
      //       radius: 20,
      //     },
      //   };
      //   nodes[link[1]] = {
      //     id: link[1],
      //     marker: {
      //       radius: 10,
      //     },
      //     color: colors[i++],
      //   };
      // } else
      if (nodes[link[0]] && nodes[link[0]].color) {
        nodes[link[1]] = {
          id: link[1],
          color: nodes[link[0]].color,
        };
      }
    });
    e.options.nodes = Object.keys(nodes).map(function (id) {
      return nodes[id];
    });
  }
);

base_url = "http://127.0.0.1:1235";
graph = {};

$.ajax({
  type: "POST",
  url: base_url + "/graph",
  contentType: "application/x-www-form-urlencoded; charset=UTF-8",
  //   data: JSON.stringify(j),
  async: false,
  dataType: "json",
  success: function (result) {
    graph = result;
  },
});
datas = [];
for (i in graph.edges) {
  edge = graph.edges[i];
  datas.push({
    from: edge.fromKey,
    to: edge.toKey,
    id: null,
    marker: {
      radius: 20,
    },
  });
}

Highcharts.chart("container", {
  chart: {
    type: "networkgraph",
    height: "100%",
  },
  title: {
    text: graph.name,
  },
  plotOptions: {
    networkgraph: {
      // keys: ["from", "to"],
      layoutAlgorithm: {
        enableSimulation: true,
      },
    },
  },
  series: [
    {
      dataLabels: {
        enabled: true,
        linkFormat: "",
      },
      data: datas,
    },
  ],
});
