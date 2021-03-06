var HighchartsConfig = {
  init: function () {
    var data = window.chartData.reverse()
    var labels = window.chartLabels.reverse()

    if(data.length && labels.length) {
      this.printChart(data, labels)
    }

  },
  printChart: function (data, labels) {

    var dates = [];
    var duration = {
      type: 'line',
      name: labels[1],
      yAxis: 1,
      data: []
    };
    var rpe = {
      type: 'line',
      name: labels[2],
      yAxis: 0,
      data: []
    };

    for (i = 0; i < data.length; i++) {
      dates.push(data[i][0])

      duration.data.push({
        x: i,
        y: parseFloat(data[i][1]), // duration column
        description: data[i][3],
        name: labels[1]
      })

      rpe.data.push({
        x: i,
        y: parseFloat(data[i][2]), // rpe column
        description: data[i][3],
        name: labels[2]
      })
    }

    Highcharts.chart('history-container', {
      title: { text: window.chartTitle  },
      subtitle: { text: '' },
      xAxis: { categories: dates },
      yAxis: [
        {
          title: { text: labels[2] },
          tickInterval:1
        },
        {
          title: { text: labels[1] },
          opposite: true
        },
      ],
      credits: { enabled: false },
      series: [rpe, duration],
      tooltip: {
        useHTML: true,
        headerFormat: '<div class="history-chart-tooltip">',
        pointFormat: '<div><strong>{point.name}</strong>: {point.y}</div>',
        followPointer: true
      }
    });
  }

}
