(function () {
    'use strict';

    var csrftoken = Cookies.get('csrftoken');
    (function poll(){
        setTimeout(function(){
            $.ajax({
                url: status_url,
                type: 'POST',
                dataType: 'json',
                data: {task_id: task_id},
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            })
                .done(function(data) {
                    console.log(data);
                    console.log("success");
                })
                .fail(function() {
                    console.log("error");
                })
                .always(function() {
                    console.log("complete");
                });
        }, 10000);
    })();
}());

