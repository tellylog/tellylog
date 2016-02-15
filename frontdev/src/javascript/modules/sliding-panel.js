var $ = require('jquery')
/**
 * Slides the sliding panel in and out of the view.
 */
;(function ($) {
  /** Variable to store the settings */
  var s
  /**
   * Module used to initialise the Sliding Panel
   * @type {Object}
   */
  var SlidingPanel = {
    settings: {
      slidingSelector: '.sliding-panel-button,.sliding-panel-fade-screen,.sliding-panel-close',
      slidingContent: '.sliding-panel-content,.sliding-panel-fade-screen',
      slidingClass: 'is-visible'
    },

    init: function () {
      s = this.settings
      this.bindUIActions()
    },

    bindUIActions: function () {
      $(s.slidingSelector).on('click touchstart', function (e) {
        $(s.slidingContent).toggleClass(s.slidingClass)
        e.preventDefault()
      })
    }
  }

  module.exports = SlidingPanel
})($)
