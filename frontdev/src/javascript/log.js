;(function () {
  var s
  var Watchlog = {
    settings: {
      csrftoken: window.Cookies.get('csrftoken'),
      wlog_log_url: window.Telly.wlog_log_url,
      wlog_unlog_url: window.Telly.wlog_unlog_url,
      log_btn: $('.log-btn'),
      log_btn_unlogged: $('.log-btn--unlogged'),
      log_btn_logged: $('.log-btn--logged')
    },

    init: function ($) {
      s = this.settings
    },

    bindUIActions: function () {
      s.log_btn_logged.click(function (event) {
        /* Act on the event */
      })
      s.log_btn_unlogged.click(function (event) {
        var kind = $(this).data('kind')
        var id = $(this).data('id')
        Watchlog.addToWlog($(this), kind, id)
      })
    },

    addToWlog: function (button, kind, id) {
      $.ajax({
        url: s.wlog_log_url,
        type: 'POST',
        dataType: 'json',
        data: {
          kind: kind,
          id: id
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (!data.error) {
            Watchlog.viewLoggedUpdate(button, kind, id)
          }
        })
        .fail(function () {
          console.log('error')
        })
        .always(function () {
          console.log('complete')
        })
    },

    viewLoggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        s.log_btn.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        s.log_btn.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      } else if (kind === 'season') {
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      }
    }

  }

  $(document).ready(function ($) {
    if (window.Telly.wlog_log_url && window.Telly.wlog_unlog_url) {
      Watchlog.init()
      Watchlog.bindUIActions()
    }
  })
})()
