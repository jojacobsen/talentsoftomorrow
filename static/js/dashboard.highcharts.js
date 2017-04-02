var HighchartsConfig = {
  init: function () {
    Highcharts.chart(
      'ts-chart-total',
      this.donutChart(74, 100, 'Sessions logged', '#F5CB5C' )
    );

    Highcharts.chart(
      'ts-chart-rpe',
      this.donutChart(7, 10, 'Latest RPE', '#F5CB5C' )
    );
  },

  donutChart: function (value, potential, label, color) {
    return {
      chart: {
        type: 'pie',
        height: 220
      },
      tooltip: { enabled: false },
      legend: { enabled: false },
      plotOptions: {
        pie: {
          animation: false,
          dataLabels: { enabled: false },
          colors: [color, '#eee']
        }
      },
      title: {
          text: value,
          align: 'center',
          verticalAlign: 'middle',
          floating: true,
          y: 0,
          style: { fontSize: '30px' }
      },
      subtitle: {
        text: label,
          align: 'center',
          verticalAlign: 'middle',
          floating: true,
          y: 20,
          style: { fontSize: '10px' }
      },
      series: [{
        size: '100%',
        innerSize: '50%',
        data: [['Score', value], ['Potential', (potential - value)]]
      }],
      credits: {
        enabled: false
      }
    }
  }
}


