var botui = new BotUI('waste-bot');

botui.message.bot({
  photo: true,
  loading: true,
  delay:500,
  content: '안녕하세요? 챗봇 철이에요~ 폐기물처리에 대해 알려드려요!'
}).then(function () {
  showReminderInput();
});

var showReminderInput = function () {
  botui.action.text({
    delay: 3000,
    action: {
      placeholder: '질문을 입력해주세요.'
    }
  }).then(function (res) {
    function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }

      var csrftoken = getCookie('csrftoken');

      function csrfSafeMethod(method) {
          // these HTTP methods do not require CSRF protection
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }

      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

/*      $(document).ready( function (data) {
      $('#myTable').DataTable();
      } );*/
      $.post('/chatbots', {'text': res}).done(function(data){
        console.log(data);

        botui.message
        .bot({
         delay: 2000,
         loading: true,
         type: 'html',
         content: data.output.text
       });
      });
    }).then(function (res) {
      showReminderInput();
    })
  }
