from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
    song_list = ['Autumn Leaves(枯葉)', \
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
    'You’d be so nice to come home to']
    # return_text =  event.message.text

    return_text = song_list[np.random(len(song_list))]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)