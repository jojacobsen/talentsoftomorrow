var History = {
  init: function () {
    var data = window.chartData.reverse()
    var self = this
    var likerts = []

    data[0].questions.forEach(function(item) {
      switch(item.slug) {
        case 'weight':
          self.writeHighlights('weight', item)
          break;
        case 'sleep':
          self.writeHighlights('sleep-hours', item)
          break;
        case 'resting-heart-rate':
          self.writeHighlights('heart-rate', item)
          break;
        case 'session-duration':
          self.writeHighlights('duration', item)
          break;
        case 'training-description':
          $('.js-history-latest-description').html(item.answer)
          break;
        default:
          likerts.push(item)
      }
    })

    this.writeLikerts(likerts)
  },

  writeHighlights: function (handle, item) {
    $('.js-' + handle + '-result').html(item.answer)
    $('.js-' + handle + '-label').html(item.label)
  },

  writeLikerts: function (likerts) {
    var template = ''

    likerts.forEach(function(item){
      var answer = parseInt(item.answer) * 10

      template = template + '<li>' +
        '<div class="tpl-answer" style="width: ' + answer + '%;"></div>'+
        '<div class="tpl-label">' + item.label + '</div>' +
        ' </li>'
    })

    $('.js-history-likerts').html(template)
  }
}
