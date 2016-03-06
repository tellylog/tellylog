var jQuery = require('jquery')
var $ = jQuery
var SlidingPanel = require('./modules/sliding-panel.js')
var Watchlist = require('./modules/watchlist.js')
var Watchlog = require('./modules/watchlog.js')
var Search = require('./modules/search.js')
var Rating = require('./modules/rating.js')
;(function ($) {
  $(document).ready(function () {
    SlidingPanel.init()
    if (window.Telly !== undefined) {
      if (window.Telly.wlist_list_url && window.Telly.wlist_unlist_url) {
        /** Check if the Telly namespace and the urls are defined. */
        /** Initialise the Watchlist */
        Watchlist.init()
      }
      if (window.Telly.task_id) {
        /** Check if the Telly namespace and the task_id are defined. */
        /** Initialise the Search */
        Search.init()
      }
      if (window.Telly.wlog_log_url && window.Telly.wlog_unlog_url) {
        /** Check if the Telly namespace and the urls are defined. */
        /** Initialise the Watchlog */
        Watchlog.init()
      }
      if (window.Telly.wlog_rate_url || window.Telly.wlog_calc_rating_url) {
        Rating.init()
      }
    }
  })
})($)
