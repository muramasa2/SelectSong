from flask import Flask, request, abort
import numpy as np
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, ConfirmTemplate, MessageAction)
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# def make_button_template():
#     message_template = TemplateSendMessage(
#         alt_text="にゃーん",
#         template=ButtonsTemplate(
#             text="セッションジャンルを選んでください。",
#             image_size="cover",
#             thumbnail_image_url="https://www.shimay.uno/nekoguruma/wp-content/uploads/sites/2/2018/03/20171124_194201-508x339.jpg",
#             actions=[
#                 URIAction(
#                     uri="https://www.shimay.uno/nekoguruma/archives/620",
#                     label="URIアクションのLABEL"
#                 )
#             ]
#         )
#     )
#     return message_template


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    song_list = [['Autumn Leaves(枯葉)', \
    'Beautiful Love', \
    'Blue Bossa', \
    'Bye Bye Black Bird', \
    'Days Of Wine And Roses', \
    'Fly Me To The Moon', \
    'Girl From Ipanema', \
    'I’ll Close My Eyes', \
    'It Could Happen To You', \
    'Now’s the Time(Fブルース)', \
    'Satin Doll', \
    'Someday My Prince Will Come', \
    'Take The “A” Train', \
    'There Will Never Be Another You', \
    'You’d be so nice to come home to'], 
    ['Feel like makin’ love', \
     'The Chicken', \
     'Chameleon', \
     'Isn’t she lovely', \
     'Spain', \
     'Cissy Strut', \
     'Sunny', \
     'Just the two of us', \
     'Cantaloupe island' \
    ]]

    confirm_template = ConfirmTemplate(text='セッションのジャンルは?', actions=[
            MessageAction(label='Jazz', text='Jazz'),
            MessageAction(label='R&B, Funk', text='R&B, Funk'),
        ])
    template_message = TemplateSendMessage(
        alt_text='Confirm alt text', template=confirm_template)
    line_bot_api.reply_message(event.reply_token, template_message)
    list_num = 0 if template_message=='Jazz' else 1

    if event.message.text == '次の曲を教えて':
        return_text = song_list[list_num][np.random.randint(0, len(song_list))]
    else:
        return_text = '無効な入力です。\n「次の曲を教えて」と入力してみてね！'
    
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=return_text))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)