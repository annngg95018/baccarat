from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton, Base,
)

import numpy as np
from PIL import ImageGrab
import cv2
import time

import threading

from pyautogui import press, typewrite, hotkey

import cv2
import numpy as np
from matplotlib import pyplot as plt

import json
import random

import threading

#json test
jsondata = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://linecorp.com"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "action": {
      "type": "uri",
      "uri": "https://linecorp.com"
    },
    "contents": [
      {
        "type": "text",
        "text": "Brown's Burger",
        "size": "xl",
        "weight": "bold"
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
              },
              {
                "type": "text",
                "text": "$10.5",
                "weight": "bold",
                "margin": "sm",
                "flex": 0
              },
              {
                "type": "text",
                "text": "400kcl",
                "size": "sm",
                "align": "end",
                "color": "#aaaaaa"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_large_32.png"
              },
              {
                "type": "text",
                "text": "$15.5",
                "weight": "bold",
                "margin": "sm",
                "flex": 0
              },
              {
                "type": "text",
                "text": "550kcl",
                "size": "sm",
                "align": "end",
                "color": "#aaaaaa"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "Sauce, Onions, Pickles, Lettuce & Cheese",
        "color": "#aaaaaa",
        "size": "xxs"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "spacer",
        "size": "xxl"
      },
      {
        "type": "button",
        "style": "primary",
        "color": "#905c44",
        "action": {
          "type": "uri",
          "label": "Add to Cart",
          "uri": "https://linecorp.com"
        }
      }
    ]
  }
}

jstr = json.dumps(jsondata)

print(jstr)

#Line app setting
app = Flask(__name__)

#0857
line_bot_api2 = LineBotApi('bWwBmKcECNbWVh1qzRo2ITtlWX96LR/aIV+rN2iRzaNIb4Axdy2mravOnYg8QZXUyYw8a7epEmKMyW+7IlWaB5DUtHNMtqcnn1+Nniu/4e83ftYW/PnfOX2HE5N+PYowuGQX0CcNW04QGxHB5NbRWwdB04t89/1O/w1cDnyilFU=')
handler2 = WebhookHandler('29d785907d4c3537c1f3ab4c9d2680eb')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle2 webhook body  
    try:
        handler2.handle(body, signature)
    except InvalidSignatureError:
        print("Handler2")
        # abort(400)

    return 'OK'


@handler2.add(PostbackEvent)
def handle2_postback(event):
    
    if event.postback.data == "註冊":
        strange_id = event.source.user_id
        Users_data = np.load("Database2.npy")
        if any (strange_id in s[0] for s in Users_data):
            for i in range(len(Users_data)):
                if strange_id in Users_data[i][0]:

                    if Users_data[i][6] != "":
                        print("already register")
                        line_bot_api2.reply_message(event.reply_token,TextSendMessage("重複註冊！"))
                        
                    else:
                        print("not support lineID")
                        line_bot_api2.reply_message(event.reply_token,TextSendMessage("尚未提供LineID，請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。！"))
                    

        else:
            print(event.source.user_id)
            Users_data = np.append(Users_data, [[strange_id, "無", "無", "無", "無", "無", "", 1]], axis=0)
            np.save("Database2.npy", Users_data)
            line_bot_api2.reply_message(event.reply_token,TextSendMessage("請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。"))

    elif event.postback.data == '開啟':
        strange_id = event.source.user_id
        Users_data = np.load("Database2.npy")
        open_i = 0
        for i in range(len(Users_data)):
            if strange_id in Users_data[i][0]:
                open_i = i
                break
        if open_i != 0:
            Users_data[open_i][7] =  1
            np.save("Database2.npy", Users_data)
            print("Close Notice")
            line_bot_api2.reply_message(event.reply_token,TextSendMessage("報牌通知開啟！"))

    
    elif event.postback.data == "Confirm":

        strange_id = event.source.user_id
        Users_data = np.load("Database2.npy")
        if any (strange_id in s[0] for s in Users_data):
                
            confirm_template_message = TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text='報牌通知設定',
                    actions=[
                        PostbackAction(
                            label='開啟通知',
                            data='開啟'
                        ),
                        PostbackAction(
                            label='取消通知',
                            data='取消'
                        )
                    ]
                )
            )
            line_bot_api2.reply_message(event.reply_token, confirm_template_message)
        else:
            print("weird guy")
            line_bot_api2.reply_message(event.reply_token,TextSendMessage("您尚未註冊！"))

    elif event.postback.data == "取消":
        strange_id = event.source.user_id
        Users_data = np.load("Database2.npy")
        stop_i = 0
        for i in range(len(Users_data)):
            if strange_id in Users_data[i][0]:
                stop_i = i
                break
        if stop_i != 0:
            Users_data[stop_i][7] =  0
            np.save("Database2.npy", Users_data)
            print("Close Notice")
            line_bot_api2.reply_message(event.reply_token,TextSendMessage("報牌通知關閉！"))

    
    elif event.postback.data == "使用教學":
        some_onesId = event.source.user_id
        line_bot_api2.push_message(some_onesId,TextSendMessage(help_strings))

    elif  event.postback.data == "套路清單":
        
        strange_id = event.source.user_id
        
        Users_data = np.load("Database2.npy")
        
        if any (strange_id in s[0] for s in Users_data):
            for i in range(len(Users_data)):
                if strange_id in Users_data[i][0]:
                    if Users_data[i][6] != "":
                        list_strategys = "您的套路清單："
                        for j in range(6):
                            if j != 0:
                                list_strategys += "\n\n套路"+str(j)+" = "+Users_data[i][j]
                        line_bot_api2.reply_message(event.reply_token,TextSendMessage(list_strategys))
                    else:
                        print("not support lineID")
                        line_bot_api2.reply_message(event.reply_token,TextSendMessage("尚未提供LineID，請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。！"))


        else:
            print(event.source.user_id)
            line_bot_api2.reply_message(event.reply_token,TextSendMessage("您尚未註冊！"))        

@handler2.add(MessageEvent, message=TextMessage)
def handle2_message(event):
    

    
    if event.message.text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api2.reply_message(
            event.reply_token,
            message
        )

    
    elif event.message.text == 'flex2':
        jsonToDict = json.loads(jstr)
        bubble = BubbleContainer.new_from_json_dict(jsonToDict)
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api2.reply_message(
            event.reply_token,
            message
        )
    
    else:
        message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://www.ultraegaming.com/wp-content/uploads/2017/10/%E7%99%BE%E5%AE%B6%E6%A8%82-1-2.jpg',
                    title='莫地百家樂',
                    text='歡迎使用本系統，請跟隨指示操作。',
                    actions=[
                        PostbackAction(
                            label='註冊會員',
                            data='註冊'
                        ),
                        PostbackAction(
                            label='報牌通知設定',
                            data='Confirm'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.triplecrowncasinos.com/wp-content/uploads/2016/07/casinos-in-colorado.jpg',
                    title='您的套路',
                    text='您可以自訂套路，並且可設定最多五組。',
                    actions=[
                        
                        PostbackAction(
                            label='套路清單',
                            data='套路清單'
                        ),
                        PostbackTemplateAction(
                            label='套路設定教學',
                            data='使用教學'
                        )
                    ]
                )
            ]
        )
        )
        
        line_bot_api2.reply_message(event.reply_token, message)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

    