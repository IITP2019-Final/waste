var botui = new BotUI('waste-bot');

botui.message
  .bot('안녕하세요? 챗봇 철이 입니다.')
  .then(function () {
    return botui.action.button({
      delay: 1000,
      action: [{
        text: 'Yep',
        value: 'yes'
      }, {
        text: 'Nope!',
        value: 'no'
      }]
    })
}).then(function (res) {
  if(res.value == 'yes') {
    showReminderInput();
  } else {
    botui.message.bot('Okay.');
  }
});

var showReminderInput = function () {
  botui.message
    .bot({
      delay: 500,
      type: 'html',
      content: '무엇이 궁금한가요?'
    })
    .then(function () {
      return botui.action.text({
        delay: 1000,
        action: {
          placeholder: '질문을 입력해주세요.'
        }
      })
    }).then(function (res) {


      // using jQuery
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

      $.post('/chatbots', {text: res}).done(function(data){
        console.log(data)

        botui.message
          .bot({
            delay: 2000,
            loading: true,
            type: 'html',
            content: '<div class="answer-table">폐기물 <u>처리비용</u> 입니다.<br><br>' //+ res.value
            + '<table>\n' +
                '      <thead>\n' +
                '        <tr>\n' +
                '          <th>품목</th><th>규격</th><th>부과금액(단위:원)</th>\n' +
                '        </tr>\n' +
                '      </thead>\n' +
                '      <tbody>\n' +
                '        <tr>\n' +
                '          <td>침대</td><td>2인용 세트</td><td>16,000</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <td>침대</td><td>침대 헤드 2인용</td><td>3,000</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <td>침대</td><td>2인용 매트리스</td><td>8,000</td>\n' +
                '        </tr>\n' +
                '      </tbody>\n' +
                '    </table></div>'
            + '<div class="answer-table2">*대형폐가전(원형보전) 또는 재활용 가능 시 : <b>무상수거</b> 가능합니다.<br>궁금한 사항이 더 있으신가요?</div>'

          });

        botui.message
          .bot({
            delay: 2000,
            loading: true,
            type: 'html',
            content: '<div class="answer-table">'+data.sigungu[0]+' <u>수거업체</u> 입니다.<br><br>' //+ res.value
            + '<table>\n' +
                '      <thead>\n' +
                '        <tr>\n' +
                '          <th>지역</th><th>업체명</th><th>소재지</th><th>전화번호</th>\n' +
                '        </tr>\n' +
                '      </thead>\n' +
                '      <tbody>\n' +
                '        <tr>\n' +
                '          <td>'+data.sigungu[0]+'</td><td>세명실업</td><td>종로구17길30(신사동)</td><td>02-305-3311</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <td>'+data.sigungu[0]+'</td><td>세명실업</td><td>종로구17길30(신사동)</td><td>02-305-3311</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <td>'+data.sigungu[0]+'</td><td>세명실업</td><td>종로구17길30(신사동)</td><td>02-305-3311</td>\n' +
                '        </tr>\n' +
                '      </tbody>\n' +
                '    </table></div>'
            + '<div class="answer-table2">궁금한 사항이 더 있으신가요?</div>'
          });

        botui.message
          .bot({
            delay: 2000,
            loading: true,
            type: 'html',
            content: '<div class="answer-table2"> 폐기물 <u>처리방법</u> 입니다.<br><br>' //+ res.value
            + '<table>\n' +
                '      <thead>\n' +
                '        <tr>\n' +
                '          <th>동주민센터</th><td>관할 동주민센터 직접방문 → 접수<br>→ 스티커 부착, 직접 폐기</td>\n' +
                '        </tr>\n' +
                '      </thead>\n' +
                '      <tbody>\n' +
                '        <tr>\n' +
                '          <th>구청</th><td>구청 홈페이지 접수 → 방문수거 신청</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <th>대형폐가전</th><td>원형 보전 시 무상수거<br>→ 전체 또는 홈페이지 접수</td>\n' +
                '        </tr>\n' +
                '        <tr>\n' +
                '          <th>재활용</th><td>재활용 가능 시 재활용센터에서 무상수거</td>\n' +
                '        </tr>\n' +
                '      </tbody>\n' +
                '    </table></div">'
            + '<div class="answer-table2">궁금한 사항이 더 있으신가요?</div">'
          });
      });



      return botui.action.button({
        type: 'html',
        delay: 1700,
        action: [{
         // icon: 'plus',
          text: '처음으로',
          value: 'yes'
        }, {
        text: '견적문의',
        value: 'no'
        }, {
        text: '종료',
        value: 'no'
      }]
      })
    }).then(function (res) {
  if(res.value == 'yes') {
    showReminderInput();
  } else {
    botui.message.bot('이용해 주셔서 감사해요. 또 오세요 :)');
  }
});
}
