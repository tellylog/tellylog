;(function () {
  'use strict'

  var csrftoken = Cookies.get('csrftoken')
  function poll () {
    $.ajax({
      url: status_url,
      type: 'POST',
      dataType: 'json',
      data: {
        task_id: task_id
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken)
      }
    })
      .done(function (data) {
        console.log(data)
        if (data.status === 'PENDING') {
          setTimeout(poll(), 5000)
        }
        console.log('success')
      })
      .fail(function () {
        console.log('error')
      })
      .always(function () {
        console.log('complete')
      })
  }
}())
