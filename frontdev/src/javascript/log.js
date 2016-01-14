;(function () {
  var s
  var Watchlog = {
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          csrftoken: window.Cookies.get('csrftoken'),
          wlog_log_url: window.Telly.wlog_log_url,
          wlog_unlog_url: window.Telly.wlog_unlog_url,
          log_btn: $('.log-btn'),
          log_btn_unlogged: $('.log-btn--unlogged'),
          log_btn_logged: $('.log-btn--logged'),
          log_btn_series: $('#log-series')
        }
      }
    },

    init: function () {
      s = this.settings()
    },

    bindUIActions: function () {
      s.log_btn_logged.click(function (event) {
        var kind = $(this).data('kind')
        var id = $(this).data('id')
        Watchlog.rmFromWlog($(this), kind, id)
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

    rmFromWlog: function (button, kind, id) {
      $.ajax({
        url: s.wlog_unlog_url,
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
          Watchlog.viewUnloggedUpdate(button, kind, id)
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
        s.log_btn_unlogged.off('click').removeClass('log-btn--unlogged').addClass('log-btn--logged')
        s.log_btn.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      } else if (kind === 'season') {
        button.off('click').removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      } else if (kind === 'episode') {
        button.off('click').removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      }
      Watchlog.bindUIActions()
    },
    viewUnloggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        s.log_btn_unlogged.off('click').removeClass('log-btn--logged').addClass('log-btn--unlogged')
        s.log_btn.children('i').removeClass('fa-calendar-check-o').addClass('fa-calendar-o')
      } else if (kind === 'season') {
        button.off('click').removeClass('log-btn--logged').addClass('log-btn--unlogged')
        button.children('i').removeClass('fa-calendar-check-o').addClass('fa-calendar-o')
        s.log_btn_series.off('click').removeClass('log-btn--logged').addClass('log-btn--unlogged')
        s.log_btn_series.children('i').removeClass('fa-calendar-check-o').addClass('fa-calendar-o')
      } else if (kind === 'episode') {
        button.off('click').removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.children('i').removeClass('fa-calendar-o').addClass('fa-calendar-check-o')
      }
      Watchlog.bindUIActions()
    }

  }

  $(document).ready(function () {
    if ((window.Telly !== undefined) && window.Telly.wlog_log_url && window.Telly.wlog_unlog_url) {
      Watchlog.init()
      Watchlog.bindUIActions()
    }
  })
})()
