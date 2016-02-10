;(function () {
  var s
  /**
   * Module used to log or unlog episodes
   * @type {object}
   */
  var Watchlog = {
    /**
     * Checks if the Telly namespace is defined and returns settings
     * @return {object} Watchlog module settings.
     */
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          csrftoken: window.Cookies.get('csrftoken'),
          wlog_log_url: window.Telly.wlog_log_url,
          wlog_unlog_url: window.Telly.wlog_unlog_url,
          series_id: window.Telly.series_id,
          log_btn: '.log-btn',
          log_btn_unlogged: '.log-btn--unlogged',
          log_btn_logged: '.log-btn--logged',
          log_btn_series: '.log-btn--series',
          log_btn_seasons: '.log-btn--season',
          log_btn_episodes: '.log-btn--episode',
          logged_icon: 'fa-eye',
          unlogged_icon: 'fa-eye-slash',
          log_season_str: 'Log the whole season',
          unlog_season_str: 'Unlog the whole season',
          log_series_str: 'Log the whole series',
          unlog_series_str: 'Unlog the whole series',
          log_episode_str: 'Log this episode',
          unlog_episode_str: 'Unlog this episode',
          list_btn: '.list-btn',
          list_btn_unlisted: '.list-btn--unlisted',
          list_btn_listed: '.list-btn--listed',
          page_controlls: '.single-page__controls'
        }
      }
    },
    /**
     * Function to initialise the Module.
     * Sets s to the settings
     * @return {void} Does not return anything
     */
    init: function () {
      s = this.settings()
      this.bindUIActions()
    },

    /** Binds all handlers to the DOM */
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
    /**
     * Makes an AJAX request to add an episode, season or series to the watchlog
     * Calls the viewLoggedUpdate() function on success
     * @param {object} button Button that triggered the event
     * @param {str} kind   Describes what should be logged
     * @param {int} id     ID of the element that should be logged
     */
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
    /**
     * Makes an AJAX request to remove an episode, season or series from the watchlog
     * Calls the viewUnloggedUpdate() function on success
     * @param {object} button Button that triggered the event
     * @param {str} kind   Describes what should be unlogged
     * @param {int} id     ID of the element that should be unlogged
     */
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
    /**
     * Updates the DOM elements to signal that an element has been logged.
     * @param {object} button Button that triggered the event
     * @param {str} kind   Describes what should be logged
     * @param {int} id     ID of the element that should be logged
     */
    viewLoggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        /** A series was logged. Every button is updated */
        $(s.log_btn_unlogged).each(function () {
          var obj_kind = $(this).data('kind')
          if (obj_kind === 'series') {
            /** Button for a series */
            $(this).prop('title', s.unlog_series_str)
          } else if (obj_kind === 'season') {
            /** Button for a season */
            $(this).prop('title', s.unlog_season_str)
          } else if (obj_kind === 'episode') {
            /** Button for an episode */
            $(this).prop('title', s.unlog_episode_str)
          }
          /** Remove the unlogged_icon and replace it with the logged_icon. */
          $(this).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          /** Remove the unlogged button class and replace it with the logged button class. */
          $(this).removeClass('log-btn--unlogged').addClass('log-btn--logged')
        })
      } else if (kind === 'season') {
        /** A season was logged. */
        /** Remove the unlogged_icon from the logged season and replace it with the logged_icon. */
        button.children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
        /** Remove the unlogged button class from the logged season and replace it with the logged button class. */
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        /** Set the title of the logged season button */
        button.prop('title', s.unlog_season_str)
        $(s.log_btn_episodes + s.log_btn_unlogged).each(function () {
          /** Set every episode from unlogged to logged */
          $(this).prop('title', s.unlog_episode_str)
          $(this).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          $(this).removeClass('log-btn--unlogged').addClass('log-btn--logged')
        })
        if ($(s.log_btn_seasons).length === $(s.log_btn_logged).length) {
          /** All seasons of a series are logged */
          /** Remove the unlogged_icon from the series button and replace it with the logged_icon. */
          $(s.log_btn_series).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          /** Remove the unlogged button class from the series button and replace it with the logged button class. */
          $(s.log_btn_series).removeClass('log-btn--unlogged').addClass('log-btn--logged')
          /** Set the title of the series button */
          $(s.log_btn_series).prop('title', s.unlog_series_str)
        }
      } else if (kind === 'episode') {
        /** An episode was logged */
        /** Remove the unlogged_icon from the logged episode and replace it with the logged_icon. */
        button.children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
        /** Remove the unlogged button class from the logged episode and replace it with the logged button class. */
        button.removeClass('log-btn--unlogged').addClass('log-btn--logged')
        /** Set the title of the logged episode button */
        button.prop('title', s.unlog_episode_str)
        if ($(s.log_btn_episodes).length === $(s.log_btn_logged).length) {
          /** All episodes of a season are logged */
          /** Remove the unlogged_icon from the logged season and replace it with the logged_icon. */
          $(s.log_btn_seasons).children('i').removeClass(s.unlogged_icon).addClass(s.logged_icon)
          /** Remove the unlogged button class from the logged season and replace it with the logged button class. */
          $(s.log_btn_seasons).removeClass('log-btn--unlogged').addClass('log-btn--logged')
          /** Set the title of the logged season button */
          $(s.log_btn_seasons).prop('title', s.unlog_season_str)
        }
      }
      /** Trigger a click on an active Watchlist button to unlist the series */
      $(s.list_btn_listed).trigger('click')
      /** Remove the Watchlist button. */
      $(s.list_btn).remove()
      /** Rebind the UIActions */
      Watchlog.bindUIActions()
    },
    /**
     * Updates the DOM elements to signal that an element has been unlogged.
     * @param {object} button Button that triggered the event
     * @param {str} kind   Describes what should be unlogged
     * @param {int} id     ID of the element that should be unlogged
     */
    viewUnloggedUpdate: function (button, kind, id) {
      if (kind === 'series') {
        /** A series was unlogged, every button is updated */
        $(s.log_btn_logged).each(function () {
          var obj_kind = $(this).data('kind')
          if (obj_kind === 'series') {
            /** Button for the series */
            $(this).prop('title', s.log_series_str)
          } else if (obj_kind === 'season') {
            /** Button for a season */
            $(this).prop('title', s.log_season_str)
          } else if (obj_kind === 'episode') {
            /** Button for an episode */
            $(this).prop('title', s.log_episode_str)
          }
          /** Remove the icon that signals that the element is logged and replace it with the unlogged icon */
          $(this).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
          /** Switch the button class from logged to unlogged */
          $(this).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        })
      } else if (kind === 'season') {
        /** A season was unlogged */
        /** Update icons, title and class of the season button */
        button.children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        button.removeClass('log-btn--logged').addClass('log-btn--unlogged')
        button.prop('title', s.log_season_str)
        /** Update icons, title and class of the series button */
        $(s.log_btn_series).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        $(s.log_btn_series).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        $(s.log_btn_series).prop('title', s.log_series_str)
        /** Update icons, title and class of the episode buttons */
        $(s.log_btn_episodes + s.log_btn_logged).each(function () {
          $(this).prop('title', s.log_episode_str)
          $(this).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
          $(this).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        })
      } else if (kind === 'episode') {
        /** An episode was unlogged */
        /** Update icons, title and class of the episode button */
        button.children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        button.removeClass('log-btn--logged').addClass('log-btn--unlogged')
        button.prop('title', s.log_episode_str)
        /** Update icons, title and class of the season button */
        $(s.log_btn_seasons).children('i').removeClass(s.logged_icon).addClass(s.unlogged_icon)
        $(s.log_btn_seasons).removeClass('log-btn--logged').addClass('log-btn--unlogged')
        $(s.log_btn_seasons).prop('title', s.log_season_str)
      }
      if ($(s.log_btn_seasons).length === $(s.log_btn_unlogged).length - 1) {
        /** All seasons are unlogged. Display the list button. */
        var wlist_icon = $('<span class="list-btn list-btn--unlisted" data-id="' + s.series_id + '" title="Add to list"><i class="fa fa-bookmark-o" ></i></span>')
        $(s.page_controlls).append(wlist_icon)
        $(document).trigger('list:bindUI')
      }
      /** Update the Eventlisteners */
      Watchlog.bindUIActions()
    }

  }

  $(document).ready(function () {
    if ((window.Telly !== undefined) && window.Telly.wlog_log_url && window.Telly.wlog_unlog_url) {
      /** Check if the Telly namespace and the urls are defined. */
      /** Initialise the Watchlog */
      Watchlog.init()
    }
  })
})()
