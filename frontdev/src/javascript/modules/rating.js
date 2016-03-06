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
          series_rating: '.single-page__rating',
          series_rating_cls: 'single-page__rating',
          series_subheading: '.single-page__subheading',
          wlog_rate_url: window.Telly.wlog_rate_url,
          wlog_calc_rating_url: window.Telly.wlog_calc_rating_url,
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
    /**
     * Toggle the classes of the previous buttons
     * @param  {object} button Current button
     * @param  {bool} action true adds active class and false removes the active class
     * @return {void}        Does not return anything
     */
    toggleAllPrev: function (button, action) {
      if (action) {
        button.removeClass(s.btn_empty).addClass(s.btn_full + ' ' + s.btn_active)
      } else {
        if (!button.hasClass(s.rating_active_cls)) {
          button.removeClass(s.btn_full + ' ' + s.btn_active).addClass(s.btn_empty)
        }
      }
      /** Check if current rating is above 0 */
      if (button.data(s.data_rating)) {
        Rating.toggleAllPrev(button.prev(s.rating_btn), action)
      }
    },

    /**
     * Remove the rating buttons of an entry
     * @param  {object} wlog_btn Watchlog button of the entry
     * @return {void}
     */
    rmRatingBtns: function (wlog_btn) {
      wlog_btn.parent().prev(s.rating_section).empty()
      Rating.bindUIActions()
    },

    /**
     * Append the rating buttons to an entry
     * @param  {object} wlog_btn Watchlog button of the entry
     * @return {void}
     */
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
    /**
     * Fill or empty the rating buttons of an entry according to a given rating.
     * @param  {object} btn    current button
     * @param  {int} rating Rating to show
     * @return {void}
     */
    redoRatingBtns: function (btn, rating) {
      var max_btn = btn
      /** Get the button for the highest rating */
      while (max_btn.data(s.data_rating) !== s.max_rating) {
        max_btn = max_btn.next(s.rating_btn)
      }
      /** @type {array} All buttons previous of the button with the highest rating + the button with the highest rating */
      var all_prev = max_btn.prevAll().addBack()

      all_prev.each(function (index) {
        /** Get rid of all classes of the button */
        $(this).removeClass()
        /** Check if the rating is bigger than the desired rating. */
        if ($(this).data(s.data_rating) > rating) {
          /** Add the empty class to the button */
          $(this).addClass(s.rating_btn_empty_cls)
        } else {
          /** Button is in the desired range. Add the active class */
          $(this).addClass(s.rating_btn_active_cls)
        }
      })
    },
    /**
     * Make an AJAX request to rate an Episode
     * @param  {object} btn    Clicked rating button
     * @param  {int} id     Episode id
     * @param  {int} rating Rating
     * @return {void}
     */
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
          if (!data.error) {
            Rating.redoRatingBtns(btn, rating)
          }
        })
    },

    recalcSeriesRating: function (id) {
      $.ajax({
        url: s.wlog_calc_rating_url,
        type: 'Get',
        dataType: 'json',
        data: {'id': id},
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (!data.error) {
            Rating.updateSeriesRating(data.avg_rating)
          }
        })
    },
    updateSeriesRating: function (new_rating) {
      if (new_rating === null) {
        $(s.series_rating).remove()
      } else {
        if (!$(s.series_rating).length) {
          var new_series_rating = $('<div/>')
          new_series_rating.addClass(s.series_rating_cls)
          $(s.series_subheading).after(new_series_rating)
        }
        var rating = $(s.series_rating)
        rating.empty()
        for (var i = 1; i <= 5; i++) {
          var new_star = $('<span/>')
          new_star.addClass('fa')
          if (i <= new_rating) {
            new_star.addClass('fa-star chery-font')
          } else if ((i > new_rating) && (i === new_rating + 0.5)) {
            new_star.addClass('fa-star-half-o chery-font')
          } else {
            new_star.addClass('fa-star-o semilight-font')
          }
          rating.append(new_star)
        }
      }
    }
  }
  module.exports = Rating
})($, Cookies)
