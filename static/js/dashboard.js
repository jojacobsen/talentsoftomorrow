var Dashboard = {
  init: function () {
    $(document).on('click', '.js-close-hero', function(){
      $('.js-dashboard-hero').hide();
      Cookies.set('hide-hero', 'true', { expires: 365 });
    })

    $(document).on('ready', function() {
      if(!Cookies.get('hide-hero')) {
        $('.js-dashboard-hero').removeClass('is-hidden');
      }
    })
  }
}


