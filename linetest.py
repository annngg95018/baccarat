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

app = Flask(__name__)

@app.route("/")
def root():
    return "Root Page"

line_bot_api = LineBotApi('+Jgyg3wv6IdzR4KAUz9rIY81BkJV9oTBfOlZ9aYDpsNSUO7MjK9ezaqiqRguBHrOvMjTIVoGK6wIi3nAMHFD/Fr7BnkQxt0f9GGLjOYHaMOns18QqUM81KLNinhxcViBZpluOfoi9d5hhnlEbE3ynwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e932e9253cab105336c606bf6f9fa7f6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(app.logger.info("Request body: " + body))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
    