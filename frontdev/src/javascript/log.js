;(function () {
  var s
  var Watchlog = {
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          csrftoken: window.Cookies.get('csrftoken'),
          wlog_log_url: window.Telly.wlog_log_url,
          wlog_unlog_url: window.Telly.wlog_unlog_url,
          log_btn: '.log-btn',
          log_btn_unlogged: '.log-btn--unlogged',
          log_btn_logged: '.log-btn--logged',
          log_btn_series: '.log-btn--series',
          log_btn_seasons: '.log-btn--season',
          logged_icon: 'fa-eye',
          unlogged_icon: 'fa-eye-slash',
          log_season_str: 'Log the whole season',
          unlog_season_str: 'Unlog the whole season',
          log_series_str: 'Log the whole series',
          unlog_series_str: 'Unlog the whole series',
          log_episode_str: 'Log this episode',
          unlog_episode_str: 'Unlog this episode'
        }
      }
    },

    init: function () {
      s = this.settings()
    },

    bindUIActions: function () {
      $(s.log_btn_logged).off('click').click(function (event) {
        var kind = $(this).data('kind')
        var id = $(this).data('id')
        Watchlog.rmFromWlog($(this), kind, id)
      })
      $(s.log_btn_unlogged).off('click').click(function (event) {
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
          if (!data.error) {
            Watchlog.viewUnloggedUpdate(button, kind, id)
          }
        })
    },
    viewLoggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        $(s.log_btn_unlogged).each(function () {
          var obj_kind = $(this).data('kind')
          if (obj_kind === 'series') {
            $(this).prop('title', s.unlog_series_str)
          } else if (obj_kind === 'season') {
            $(this).prop('title', s.unlog_season_str)
          } else if (obj_kind === 'episode') {
            $(this).prop('title', s.unlog_episode_str)
          }
          $(this).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          $(this).removeClass('log-btn--unlogged').addClass('log-btn--logged')
        })
      } else if (kind === 'season') {
        button.children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.prop('title', s.unlog_season_str)
        if ($(s.log_btn_seasons).length === $(s.log_btn_logged).length) {
          $(s.log_btn_series).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          $(s.log_btn_series).removeClass('log-btn--unlogged').addClass('log-btn--logged')
          $(s.log_btn_series).prop('title', s.unlog_series_str)
        }

      } else if (kind === 'episode') {
        button.children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.prop('title', s.unlog_episode_str)
      }
      Watchlog.bindUIActions()
    },
    viewUnloggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        $(s.log_btn_logged).each(function () {
          var obj_kind = $(this).data('kind')
          if (obj_kind === 'series') {
            $(this).prop('title', s.log_series_str)
          } else if (obj_kind === 'season') {
            $(this).prop('title', s.log_season_str)
          } else if (obj_kind === 'episode') {
            $(this).prop('title', s.log_episode_str)
          }
          $(this).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
          $(this).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        })
      } else if (kind === 'season') {
        button.children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        button.removeClass('log-btn--logged').addClass('log-btn--unlogged')
        button.prop('title', s.log_season_str)
        $(s.log_btn_series).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        $(s.log_btn_series).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        $(s.log_btn_series).prop('title', s.log_series_str)
      } else if (kind === 'episode') {
        button.children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        button.prop('title', s.log_episode_str)
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
