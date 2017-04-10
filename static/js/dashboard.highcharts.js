var HighchartsConfig = {
  handles: {
    tsTotal: 'ts-chart-total',
    tsRpe: 'ts-chart-rpe',
    dwCompletion: 'dw-chart-completion',
    dwTotal: 'dw-chart-total'
  },

  init: function () {
    var tsTotal = this.getValue('tsTotal')
    var dwTotal = this.getValue('dwTotal')

    Highcharts.chart(
      this.handles.tsTotal,
      this.donutChart(tsTotal, this.getTotalCap(tsTotal), 'Sessions', '#F5CB5C', true )
    );

    Highcharts.chart(
      this.handles.tsRpe,
      this.donutChart(this.getValue('tsRpe'), 10, 'Latest RPE', '#F5CB5C', true )
    );

    Highcharts.chart(
      this.handles.dwCompletion,
      this.donutChart(this.getValue('dwCompletion'), 100, 'Completion %', '#F5CB5C', false )
    );

    Highcharts.chart(
      this.handles.dwTotal,
      this.donutChart(dwTotal, this.getTotalCap(dwTotal), 'Total count', '#F5CB5C', false )
    );
  },

  getValue: function(handle) {
    var value = $('#' + this.handles[handle]).data('value')

    return value > 0 ? value : 0
  },

  getTotalCap: function (count) {
    if (count > 52 && count <= 260) {
      return 260
    } else if (count > 260) {
      return 366
    }

    return 52
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
          text: String(value),
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


