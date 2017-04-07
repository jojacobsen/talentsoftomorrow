var HighchartsConfig = {
  init: function () {
    var data = window.chartData
    var labels = window.chartLabels

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

    console.log(labels)

    for (i = 0; i < data.length; i++) {
      dates.push(data[i][0])

      duration.data.push({
        x: i,
        y: parseFloat(data[i][1]), // duration column
        description: data[i][3]
      })

      rpe.data.push({
        x: i,
        y: parseFloat(data[i][2]), // rpe column
        description: data[i][3]
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
      series: [rpe, duration]
    });
  }

}
