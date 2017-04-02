var HighchartsConfig = {
  init: function () {
    var data = window.chartData;
    var labels = window.chartLabels;
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
        y: parseFloat(data[i][4]),
        description: data[i][3]
      })

      rpe.data.push({
        x: i,
        y: parseFloat(data[i][1]),
        description: data[i][3]
      })
    }

    Highcharts.chart('history-container', {
      title: { text: window.chartTitle  },
      subtitle: { text: '' },
      xAxis: { categories: dates },
      yAxis: [
        { title: { text: labels[1] }},
        { title: { text: labels[3] }, opposite: true},
      ],
      credits: { enabled: false },
      series: [rpe, duration]
    });
  }
}
