;(function () {
  var s
  var Watchlist = {
    settings: function () {
      if (window.Telly !== undefined) {
        return {
          csrftoken: window.Cookies.get('csrftoken'),
          wlist_list_url: window.Telly.wlist_list_url,
          wlist_unlist_url: window.Telly.wlist_unlist_url,
          list_btn: '.list-btn',
          list_btn_unlisted: '.list-btn--unlisted',
          list_btn_listed: '.list-btn--listed',
          listed_icon: 'fa-bookmark',
          unlisted_icon: 'fa-bookmark-o',
          list_str: 'Add to list',
          unlist_str: 'Remove from list'
        }
      }
    },

    init: function () {
      s = this.settings()
    },

    bindUIActions: function () {
      $(s.list_btn_listed).off('click').click(function (event) {
        var id = $(this).data('id')
        Watchlist.rmFromWlist($(this), id)
      })
      $(s.list_btn_unlisted).off('click').click(function (event) {
        var id = $(this).data('id')
        console.log('hello')
        Watchlist.addToWlist($(this), id)
      })
    },

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
          console.log(data)
          if (!data.error) {
            Watchlist.viewListedUpdate(button, id)
          }
        })
    },

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
          console.log(data)
          if (!data.error) {
            Watchlist.viewUnlistedUpdate(button, id)
          }
        })
    },

    viewListedUpdate: function (button, id) {
      button.children('i').removeClass(s.unlisted_icon).addClass(s.listed_icon)
      button.removeClass('list-btn--unlisted').addClass('list-btn--listed')
      button.prop('title', s.unlist_str)
      Watchlist.bindUIActions()
    },

    viewUnlistedUpdate: function (button, id) {
      button.children('i').removeClass(s.listed_icon).addClass(s.unlisted_icon)
      button.removeClass('list-btn--listed').addClass('list-btn--unlisted')
      button.prop('title', s.list_str)
      Watchlist.bindUIActions()
    },

  }

  $(document).ready(function () {
    if ((window.Telly !== undefined) && window.Telly.wlist_list_url && window.Telly.wlist_unlist_url) {
      Watchlist.init()
      Watchlist.bindUIActions()
    }
  })
})()
