var botui = new BotUI('waste-bot');

botui.message
  .bot('안녕하세요? 챗봇 철-E 입니다.')
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
      botui.message
        .bot({
          delay: 1500,
          loading: true,
          type: 'html',
          content: '폐기물 <u>처리방법</u> 입니다.<br><br>' //+ res.value
          + '<table>\n' +
              '      <thead>\n' +
              '        <tr>\n' +
              '          <th>Lorem</th><th>Lorem</th><th>Ipsum</th><th>Dolor</th>\n' +
              '        </tr>\n' +
              '      </thead>\n' +
              '      <tbody>\n' +
              '        <tr>\n' +
              '          <td>Lorem</td><td>Lorem</td><td>Ipsum</td><td>Dolor</td>\n' +
              '        </tr>\n' +
              '        <tr>\n' +
              '          <td>Lorem</td><td>Lorem</td><td>Ipsum</td><td>Dolor</td>\n' +
              '        </tr>\n' +
              '      </tbody>\n' +
              '    </table>' +
              '<style>\n' +
              '  table {\n' +
              '    width: 100%;\n' +
              '    border: 1px solid #444444;\n' +
              '    border-collapse: collapse;\n' +
              '  }\n' +
              '  th, td {\n' +
              '    border: 1px solid #444444;\n' +
              '    padding: 10px;\n' +
              '  }\n' +
              '</style><br>'

          + '궁금한 사항이 더 있으신가요?'
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