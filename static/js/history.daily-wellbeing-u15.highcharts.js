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
    var config = this.config(labels)
    var chartData = []

    for (i = 0; i < data.length; i++) {
      dates.push(data[i][0])
    }

    for (i = 0; i < config.length; i++) {
      var item = config[i]

      chartData.push({
        type: 'line',
        name: labels[item.index],
        yAxis: item.yAxis,
        color: item.color,
        data: []
      })

      for (e = 0; e < data.length; e++) {
        var row = data[e]

        chartData[i].data.push({ x: e, y: parseFloat(row[item.index]) })
      }
    }

    Highcharts.chart('history-container', {
      title: { text: window.chartTitle  },
      subtitle: { text: '' },
      xAxis: { categories: dates },
      plotOptions: {
        line: {
          marker: {
            symbol: 'circle',
            radius: 4
          }
        }
      },

      yAxis: [
        {
          title: { text: 'Ratings' },
          labels: { style: { color: '#666' }, format: '{value}p' }
        },
        { // weight
          title: { text: '' },
          opposite: true,
          labels: { style: { color: '#f5cb5c' }, format: '{value}kg' }
        },
        { // rhr
          title: { text: '' },
          opposite: true,
          labels: { style: { color: '#469648' },
          format: '{value}bpm'}
        },
        { // Hours of sleep
          title: { text: '' },
          opposite: true,
          labels: {style: { color: '#64b4ff'} , format: '{value}h' }
        }
      ],
      credits: { enabled: false },
      series: chartData
    });
  },

  config: function (l) {
    // TODO: get indexes dynamically
    var splitIndex = 8
    var labels = l.slice(0, splitIndex)
    var ratingRows = []

    labels.forEach(function(label, i){
      ratingRows.push({
        key: label,
        index: i,
        yAxis: 0,
        color: '#666'
      })
    });

    var specialRows = [
      {
        key: 'weight',
        index: 8,
        yAxis: 1,
        color: '#f5cb5c'
      },
      {
        key: 'rhr',
        index: 9,
        yAxis: 2,
        color: '#469648'
      },
      {
        key: 'sleepHours',
        index: 10,
        yAxis: 3,
        color: '#64b4ff'
      }
    ]

    return ratingRows.concat(specialRows)
  }
}
