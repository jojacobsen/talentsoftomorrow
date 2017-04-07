var HighchartsConfig = {
  init: function () {
    Highcharts.chart(
      'ts-chart-total',
      this.donutChart(74, 100, 'Sessions', '#F5CB5C', false )
    );

    Highcharts.chart(
      'ts-chart-rpe',
      this.donutChart(7, 10, 'Latest RPE', '#F5CB5C', false )
    );

    Highcharts.chart(
      'dw-chart-completion',
      this.donutChart(8, 10, 'Completion %', '#F5CB5C', true )
    );

    Highcharts.chart(
      'dw-chart-total',
      this.donutChart(31, 310, 'Total count', '#F5CB5C', true )
    );
  },

  donutChart: function (value, potential, label, color, inverted) {
    var textColor = inverted ? '#fff' : '#000'

    return {
      chart: {
        type: 'pie',
        height: 220,
        backgroundColor: 'transparent'
      },
      tooltip: { enabled: false },
      legend: { enabled: false },
      plotOptions: {
        pie: {
          animation: false,
          dataLabels: { enabled: false },
          colors: [color, '#eee'],
          borderWidth: 0
        }
      },
      title: {
          text: value,
          align: 'center',
          verticalAlign: 'middle',
          floating: true,
          y: 0,
          style: { fontSize: '30px', color: textColor }
      },
      subtitle: {
        text: label,
          align: 'center',
          verticalAlign: 'middle',
          floating: true,
          y: 20,
          style: { fontSize: '10px', color: textColor }
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


