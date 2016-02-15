var $ = require('jquery')
var Cookies = require('js-cookie')
;(function ($, Cookies) {
  /** Variable to store the settings */
  var s
  /**
   * Module used on the search page to load the searchresults.
   * @type {Object}
   */
  var Search = {
    /**
     * Checks if the Telly namespace is defined and returns the settings.
     * @return {object} Settings for the Watchlist
     */
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          /** @type {str} CSRF Token */
          csrftoken: Cookies.get('csrftoken'),
          /** @type {str} ID of the Task */
          task_id: window.Telly.task_id,
          /** @type {str} Ajax url to get the status of the task */
          status_url: window.Telly.status_url,
          /** @type {str} Ajax url to get the result of the query */
          result_url: window.Telly.result_url,
          /** @type {str} Search query */
          query: window.Telly.query,
          /** @type {str} Path to the placeholder image */
          placeholder: window.Telly.placeholder,
          /** @type {object} jQuery result list selector */
          result_list: $('#result-list'),
          /** @type {object} jQuery result list info selector */
          result_list_info: $('#result-list_info'),
          /** @type {int} Maximum number of requests to poll */
          max_requests: 300,
          /** @type {int} Maximum number of characters of the description  */
          max_description_length: 240,
          /** @type {String} Empty result entry. */
          result_sceleton: '<div class="result"> \
                              <a class="result__link"> \
                                <img class="result__image"> \
                              </a> \
                              <div class="result__text"> \
                                <a class="result__link"> \
                                  <h1 class="result__heading"></h1> \
                                </a> \
                                <h2 class="result__subheading"></h2> \
                                <p class="result__description"></p> \
                              </div> \
                            </div>'
        }
      }
    },
    /**
     * Function to initialise the Module.
     * Sets s to the settings and starts the polling.
     * @return {void} Does not return anything
     */
    init: function ($) {
      s = this.settings()
      this.poll(0)
    },

    /**
     * Sends an ajax request to the status url and checks if the task is finished, still running or errored.
     * If the task is still running it sends another request.
     * @param  {int} number Number of the current request
     */
    poll: function (number) {
      if (number <= s.max_requests) {
        /** Check if the number of the request is smaller or equal the number of max requests */
        $.ajax({
          url: s.status_url,
          type: 'GET',
          dataType: 'json',
          data: {
            task_id: s.task_id
          },
          beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
          }
        })
          .done(function (data) {
            if (data.status === 'PENDING') {
              /** Task is still running */
              if (number <= 5) {
                /** The first six requests are fired with a 100 ms delay */
                setTimeout(function () { Search.poll(++number) }, 100)
              } else if (number <= 10) {
                /** The next five requests are fired with a 500 ms delay */
                setTimeout(function () { Search.poll(++number) }, 500)
              } else if (number <= 100) {
                /** The next 90 requests are fired with a delay of one second */
                setTimeout(function () { Search.poll(++number) }, 1000)
              } else {
                /** Every other request is fired with a delay of five seconds */
                setTimeout(function () { Search.poll(++number) }, 5000)
              }
            } else if (data.status === 'SUCCESS') {
              /** The task finished successfull. The results are loaded. */
              Search.load_results()
            } else {
              /** The task errored. Display an error message. */
              Search.search_error()
            }
          })
          .fail(function () {
            /** The ajax call failed. Display an error message. */
            Search.search_error()
          })
      } else {
        /** The max number of requests was exceeded. Display an error message. */
        Search.search_error()
      }
    },
    /**
     * Displays an error message on the page.
     */
    search_error: function () {
      s.result_list_info.replaceWith('There was an error with your search request. <i class="fa fa-frown-o"></i>')
    },
    /**
     * Makes an ajax call to get the results of the query.
     */
    load_results: function () {
      $.ajax({
        url: s.result_url,
        type: 'GET',
        dataType: 'json',
        data: {query: s.query},
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (data.search_res.length) {
            /** There are results. Display them on the page. */
            Search.build_results(data)
          } else {
            /** There are no results. Display an error that there are no results. */
            Search.no_results()
          }
        })
        .fail(function () {
          /** The request failed. Display an error on the page. */
          Search.search_error()
        })
    },
    /**
     * Display the results on the page.
     * @param  {object} data Results of the ajax request
     */
    build_results: function (data) {
      /** @type {int} Number of results */
      var res_count = data.search_res.length
      /** Display the number of results. */
      s.result_list_info.replaceWith('Your search returned ' + res_count + ' ' + ((res_count > 1) ? 'results' : 'result') + '.')
      /** Display every result on the page. */
      for (var i = 0; i < data.search_res.length; i++) {
        /** @type {object} Current search result. */
        var search_res = data.search_res[i]
        /** @type {str} If an url is given use it. Else use the placeholder image url. */
        var poster_url = (search_res.poster ? search_res.poster : s.placeholder)
        /** @type {Array} Holds the genres of the current result */
        var genres = []
        for (var j = 0; j < search_res.genres.length; j++) {
          genres.push(search_res.genres[j].name)
        }
        /** Sort the genres alphabetically */
        genres.sort()
        /** @type {str} String to hold the names of the genres seperated by a comma. */
        var genre_str = genres.join(', ')
        /** @type {object} New empty result entry. */
        var result = $(s.result_sceleton)
        /** Add the href attribute of the result link */
        $('.result__link', result).attr('href', search_res.url)
        /** Add the src attribute of the poster */
        $('.result__image', result).attr('src', poster_url)
        /** @type {str} Title of the series */
        var result_title = search_res.name
        /** If a year is given add it to the title */
        result_title += (search_res.year ? ' (' + search_res.year + ')' : '')
        /** Fill the heading of the result with the title of the series  */
        $('.result__heading', result).append(result_title)
        /** Fill the subheading with the genre string */
        $('.result__subheading', result).append(genre_str)
        /** @type {str} Full description of the series */
        var description = search_res.overview
        if (description.length >= s.max_description_length) {
          /** The description is longer than the max_description_length */
          /** @type {str} Trimmed the description to the maximum number of characters */
          var trimmed_description = description.substr(0, s.max_description_length)
          /** @type {str} Trim the description down to the next space. */
          trimmed_description = trimmed_description.substr(0, Math.min(trimmed_description.length, trimmed_description.lastIndexOf(' ')))
          /** Add an elipsis to the end of the trimmed description. */
          trimmed_description += '&hellip;'
        } else {
          /** @type {str} Description is allready smaller than the maximum number of characters */
          trimmed_description = description
        }
        /** Fill the description paragraph with the description. */
        $('.result__description', result).append(trimmed_description)
        /** Append the result to the page */
        s.result_list.append(result)
      }
    },
    /**
     * Displays an error to signal that no results where found.
     */
    no_results: function () {
      s.result_list_info.replaceWith('Your search did not return any results. <i class="fa fa-meh-o"></i>')
    }
  }
  module.exports = Search
})($, Cookies)
