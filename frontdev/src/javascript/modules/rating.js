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
          btn_empty: 'fa-star-o',
          btn_full: 'fa-star',
          btn_active: 'rating__btn--active',
          rating_btn_cls: 'rating__btn fa fa-star-o',
          data_rating: 'rating',
          wlog_rate_url: window.Telly.wlog_rate_url
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
      $(s.rating_btn).hover(function () {
        /* Stuff to do when the mouse enters the element */
        Rating.toggleAllPrev($(this), true)
      }, function () {
        /* Stuff to do when the mouse leaves the element */
        Rating.toggleAllPrev($(this), false)
      })
      $(s.rating_btn).click(function () {
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
        button.removeClass(s.btn_full + ' ' + s.btn_active).addClass(s.btn_empty)
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
          rating_btn.addClass(s.rating_btn_cls)
          rating_section.append(rating_btn)
        }
        Rating.bindUIActions()
      }
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
            Rating.toggleAllPrev(btn, true)
          }
        })
    }
  }
  module.exports = Rating
})($, Cookies)
