var botui = new BotUI('waste-bot');

botui.message
  .bot('Would you like to add a reminder?')
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
      content: '질문을 입력해주세요.'
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
          delay: 2000,
          loading: true,
          content: '저의 답은 이것입니다. ' + res.value
        });

      return botui.action.button({
        delay: 3000,
        action: [{
          icon: 'plus',
          text: '질문 더하기',
          value: 'yes'
        }]
      })
    }).then(showReminderInput);
}
