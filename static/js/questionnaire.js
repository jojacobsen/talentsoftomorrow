var Questionnaire = {
  init: function () {
    var system = $('.js-measurement-system').data('id')
    var $target = $('.js-label-weight')
    var label = $target.text().split('*')[0].trim()
    var unit = system === 'SI' ? 'kg' : 'lb'

    $target.html(label = label + ' (' + unit + ')*')
  }
}
