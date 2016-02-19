var $ = require('jquery')
var Cookies = require('js-cookie')
;(function ($, Cookies) {
  /** Variable to store the settings */
  var s
  /**
   * Module used to rate episodes
   * @type {Object}
   */
  var Rating = {
    /**
     * Checks if the Telly namespace is defined and returns the settings.
     * @return {object} Settings for the Watchlist
     */
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          /** @type {str} CSRF Token */
          csrftoken: Cookies.get('csrftoken'),
          rating_section: '.rating',
          rating_btn: '.rating__btn',
          rating_active_cls: 'rating__btn--active',
          rating_btn_active_cls: 'rating__btn rating__btn--active fa fa-star',
          btn_empty: 'fa-star-o',
          btn_full: 'fa-star',
          btn_active: 'rating__btn--hover',
          rating_btn_cls: 'rating__btn',
          rating_btn_empty_cls: 'rating__btn fa fa-star-o',
          data_rating: 'rating',
          wlog_rate_url: window.Telly.wlog_rate_url,
          max_rating: 4
        }
      }
    },

    /**
     * Function to initialise the Module.
     * Sets s to the settings and calls the function to bind UI actions
     * @return {void} Does not return anything
     */
    init: function () {
      s = this.settings()
      this.bindUIActions()
    },

    /** Sets up all element listeners for the module */
    bindUIActions: function () {
      $(s.rating_btn).off('hover').hover(function () {
        /* Stuff to do when the mouse enters the element */
        Rating.toggleAllPrev($(this), true)
      }, function () {
        /* Stuff to do when the mouse leaves the element */
        Rating.toggleAllPrev($(this), false)
      })
      $(s.rating_btn).off('click').click(function (e) {
        var btn = $(this)
        var rating = btn.data('rating')
        var id = btn.parent(s.rating_section).data('id')
        Rating.rateEpisode(btn, id, rating)
      })
    },

    toggleAllPrev: function (button, action) {
      if (action) {
        button.removeClass(s.btn_empty).addClass(s.btn_full + ' ' + s.btn_active)
      } else {
        if (!button.hasClass(s.rating_active_cls)) {
          button.removeClass(s.btn_full + ' ' + s.btn_active).addClass(s.btn_empty)
        }
      }
      if (button.data(s.data_rating)) {
        Rating.toggleAllPrev(button.prev(s.rating_btn), action)
      }
    },

    rmRatingBtns: function (wlog_btn) {
      wlog_btn.parent().prev(s.rating_section).empty()
      Rating.bindUIActions()
    },

    showRatingBtns: function (wlog_btn) {
      var rating_section = wlog_btn.parent().prev(s.rating_section)
      if (rating_section.length <= 1) {
        for (var i = 0; i < 5; i++) {
          var rating_btn = $('<span/>')
          rating_btn.attr('data-rating', i)
          rating_btn.addClass(s.rating_btn_empty_cls)
          rating_section.append(rating_btn)
        }
        Rating.bindUIActions()
      }
    },
    redoRatingBtns: function (btn, rating) {
      var max_btn = btn

      while (max_btn.data(s.data_rating) !== s.max_rating) {
        max_btn = max_btn.next(s.rating_btn)
      }
      var all_prev = max_btn.prevAll().addBack()

      all_prev.each(function (index) {
        $(this).removeClass()
        if ($(this).data(s.data_rating) > rating) {
          $(this).addClass(s.rating_btn_empty_cls)
        } else {
          $(this).addClass(s.rating_btn_active_cls)
        }
      })
    },
    rateEpisode: function (btn, id, rating) {
      $.ajax({
        url: s.wlog_rate_url,
        type: 'POST',
        dataType: 'json',
        data: {id: id,
          rating: rating
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          console.log(data)
          if (!data.error) {
            Rating.redoRatingBtns(btn, rating)
          }
        })
    }
  }
  module.exports = Rating
})($, Cookies)
