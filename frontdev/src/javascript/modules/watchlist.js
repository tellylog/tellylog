var $ = require('jquery')
var Cookies = require('js-cookie')
;(function ($, Cookies) {
  /** Variable to store the settings */
  var s
  /**
   * Module used to list or unlist series
   * @type {Object}
   */
  var Watchlist = {
    /**
     * Checks if the Telly namespace is defined and returns the settings.
     * @return {object} Settings for the Watchlist
     */
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          /** @type {str} CSRF Token */
          csrftoken: Cookies.get('csrftoken'),
          /** @type {str} Ajax url to add a series to the Watchlist */
          wlist_list_url: window.Telly.wlist_list_url,
          /** @type {str} Ajax url to remove a series from the Watchlist */
          wlist_unlist_url: window.Telly.wlist_unlist_url,
          /** @type {bool} Defines if series is on the Watchlist */
          on_wlist: window.Telly.on_wlist,
          /** @type {String} Class of the list button */
          list_btn: '.list-btn',
          /** @type {String} Class of the unlisted button */
          list_btn_unlisted: '.list-btn--unlisted',
          /** @type {String} Class of the listed button */
          list_btn_listed: '.list-btn--listed',
          /** @type {String} Class of the listed icon */
          listed_icon: 'fa-bookmark',
          /** @type {String} Class of the unlisted icon */
          unlisted_icon: 'fa-bookmark-o',
          /** @type {String} Title text if the series is not on the watchlist */
          list_str: 'Add to list',
          /** @type {String} Title text if the series is on the watchlist */
          unlist_str: 'Remove from list'
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
      $(s.list_btn_listed).off('click').click(function (event) {
        var id = $(this).data('id')
        Watchlist.rmFromWlist($(this), id)
      })
      $(s.list_btn_unlisted).off('click').click(function (event) {
        var id = $(this).data('id')
        Watchlist.addToWlist($(this), id)
      })
      $(document).on('list:bindUI', function () {
        Watchlist.bindUIActions()
      })
    },

    /**
     * Makes an ajax request to add the series to the watchlist
     * Calls viewListedUpdate on success
     * @param {object} button Button that triggerd the function
     * @param {int} id     ID of the series
     */
    addToWlist: function (button, id) {
      $.ajax({
        url: s.wlist_list_url,
        type: 'POST',
        dataType: 'json',
        data: {
          id: id
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (!data.error) {
            Watchlist.viewListedUpdate(button, id)
          }
        })
    },

    /**
     * Makes an ajax request to remove the series from the watchlist
     * Calls viewUnlistedUpdate on success
     * @param {object} button Button that triggerd the function
     * @param {int} id     ID of the series
     */
    rmFromWlist: function (button, id) {
      $.ajax({
        url: s.wlist_unlist_url,
        type: 'POST',
        dataType: 'json',
        data: {
          id: id
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (!data.error) {
            Watchlist.viewUnlistedUpdate(button, id)
          }
        })
    },

    /**
     * Updates the DOM elements to signal that a series was listed
     * @param  {object} button Add to watchlist button
     * @param  {int} id     ID of the series
     */
    viewListedUpdate: function (button, id) {
      /** Remove the unlisted icon from the button and replace it with the listed icon */
      button.children('i').removeClass(s.unlisted_icon).addClass(s.listed_icon)
      /** Remove the unlisted class from the button and replace it with the listed class */
      button.removeClass('list-btn--unlisted').addClass('list-btn--listed')
      /** Set the title of the button */
      button.prop('title', s.unlist_str)
      /** Update the on_wlist property to true */
      window.Telly.on_wlist = true
      /** Rebind the UI actions */
      Watchlist.bindUIActions()
    },

    /**
     * Updates the DOM elements to signal that a series was removed from the watchlist
     * @param  {object} button Remove from watchlist button
     * @param  {int} id     ID of the series
     */
    viewUnlistedUpdate: function (button, id) {
      /** Remove the listed icon from the button and replace it with the unlisted icon */
      button.children('i').removeClass(s.listed_icon).addClass(s.unlisted_icon)
      /** Remove the listed class from the button and replace it with the unlisted class */
      button.removeClass('list-btn--listed').addClass('list-btn--unlisted')
      /** Set the title of the button */
      button.prop('title', s.list_str)
      /** Update the on_wlist property to false */
      window.Telly.on_wlist = false
      /** Rebind the UI actions */
      Watchlist.bindUIActions()
    }
  }
  module.exports = Watchlist
})($, Cookies)
