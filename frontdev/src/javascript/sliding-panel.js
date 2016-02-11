/**
 * Slides the sliding panel in and out of the view.
 */
$(document).ready(function () {
  $('.sliding-panel-button,.sliding-panel-fade-screen,.sliding-panel-close').on('click touchstart', function (e) {
    $('.sliding-panel-content,.sliding-panel-fade-screen').toggleClass('is-visible')
    e.preventDefault()
  })
})
