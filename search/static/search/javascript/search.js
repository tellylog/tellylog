var s
var Search = {
  settings: {
    csrftoken: window.Cookies.get('csrftoken'),
    task_id: window.Telly.task_id,
    status_url: window.Telly.status_url,
    result_url: window.Telly.result_url,
    query: window.Telly.query
  },

  init: function () {
    s = this.settings
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
          console.log(data)
          if (data.status === 'PENDING') {
            setTimeout(function () { Search.poll($, number) }, 5000)
          } else if (data.status === 'SUCCESS') {
            Search.load_results($)
          } else {
            Search.search_error()
          }
          console.log('success')
        })
        .fail(function () {
          console.log('error')
        })
        .always(function () {
          console.log('complete')
        })
    } else {
    }
  },
  search_error: function () {
    console.log('There was an error with your search request :(')
  },
  load_results: function ($) {
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
        console.log(data)
        console.log('success')
      })
      .fail(function () {
        console.log('error')
      })
      .always(function () {
        console.log('complete')
      })
  }
}

jQuery(document).ready(function ($) {
  Search.init()
  Search.poll($, 0)
})
