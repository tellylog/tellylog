;(function () {
  var s
  var Search = {
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          csrftoken: window.Cookies.get('csrftoken'),
          task_id: window.Telly.task_id,
          status_url: window.Telly.status_url,
          result_url: window.Telly.result_url,
          query: window.Telly.query,
          placeholder: window.Telly.placeholder,
          result_list: $('#result-list'),
          result_list_info: $('#result-list_info')
        }
      }
    },

    init: function ($) {
      s = this.settings()
    },

    poll: function ($, number) {
      if (number <= 300) {
        $.ajax({
          url: s.status_url,
          type: 'POST',
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
              if (number <= 5) {
                setTimeout(function () { Search.poll($, number) }, 100)
              } else if (number <= 10) {
                setTimeout(function () { Search.poll($, number) }, 500)
              } else {
                setTimeout(function () { Search.poll($, number) }, 5000)
              }
            } else if (data.status === 'SUCCESS') {
              Search.load_results()
            } else {
              Search.search_error()
            }
          })
          .fail(function () {
            Search.search_error()
          })
      } else {
        Search.search_error()
      }
    },
    search_error: function () {
      s.result_list_info.replaceWith('There was an error with your search request. <i class="fa fa-frown-o"></i>')
    },
    load_results: function () {
      $.ajax({
        url: s.result_url,
        type: 'POST',
        dataType: 'json',
        data: {query: s.query},
        beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', s.csrftoken)
        }
      })
        .done(function (data) {
          if (data.search_res.length) {
            Search.build_results(data)
          } else {
            Search.no_results(data)
          }
        })
        .fail(function () {
          Search.search_error()
        })
    },
    build_results: function (data) {
      var res_count = data.search_res.length
      s.result_list_info.replaceWith('Your search returned ' + res_count + ' ' + ((res_count > 1) ? 'results' : 'result') + '.')
      for (var i = 0; i < data.search_res.length; i++) {
        var search_res = data.search_res[i]
        var poster_url = (search_res.poster ? search_res.poster : s.placeholder)
        var genre_str = ''
        for (var j = 0; j < search_res.genres.length; j++) {
          if (j === (search_res.genres.length - 1)) {
            genre_str += search_res.genres[j].name
          } else {
            genre_str += search_res.genres[j].name + ', '
          }
        }
        var result = $('<div class="result"><a class="result__link"><img class="result__image"></a><div class="result__text"><a class="result__link"><h1 class="result__heading"></h1></a><h2 class="result__subheading"></h2><p class="result__description"></p></div></div>')
        $('.result__link', result).attr('href', search_res.url)
        $('.result__image', result).attr('src', poster_url)
        $('.result__heading', result).append(search_res.name + ' (' + search_res.year + ')')
        $('.result__subheading', result).append(genre_str)
        var description = search_res.overview
        var maxLength = 240
        var trimmedDescription = description.substr(0, maxLength)
        trimmedDescription = trimmedDescription.substr(0, Math.min(trimmedDescription.length, trimmedDescription.lastIndexOf(' ')))
        trimmedDescription += '...'
        $('.result__description', result).append(trimmedDescription)
        s.result_list.append(result)
      }
    },
    no_results: function (data) {
      s.result_list_info.replaceWith('Your search did not return any results. <i class="fa fa-meh-o"></i>')
    }
  }

  $(document).ready(function () {
    if ((window.Telly !== undefined) && window.Telly.task_id) {
      Search.init()
      Search.poll($, 0)
    }
  })
})($)
