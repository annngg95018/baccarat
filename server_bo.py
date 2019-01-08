from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,ButtonsTemplate,PostbackTemplateAction, 
    URITemplateAction, MessageTemplateAction, ConfirmTemplate, PostbackAction, MessageAction,
    PostbackEvent, Postback, CarouselColumn, CarouselTemplate
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

#Image detection region 
tem = ['Peace.png', 'Home.png', 'Client.png']
strategy_dic = {'閒':'閒', '莊':'莊', '和':'和'}

strategy_dicR = {'C':'閒', 'H':'莊', 'P':'和'}

Users_id = []

import random

#  Felzenszwalb et al.
def non_max_suppression_slow(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
 
	# initialize the list of picked indexes
	pick = []
 
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
 
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list, add the index
		# value to the list of picked indexes, then initialize
		# the suppression list (i.e. indexes that will be deleted)
		# using the last index
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		suppress = [last]
		# loop over all indexes in the indexes list
		for pos in range(0, last):
			# grab the current index
			j = idxs[pos]
 
			# find the largest (x, y) coordinates for the start of
			# the bounding box and the smallest (x, y) coordinates
			# for the end of the bounding box
			xx1 = max(x1[i], x1[j])
			yy1 = max(y1[i], y1[j])
			xx2 = min(x2[i], x2[j])
			yy2 = min(y2[i], y2[j])
 
			# compute the width and height of the bounding box
			w = max(0, xx2 - xx1 + 1)
			h = max(0, yy2 - yy1 + 1)
 
			# compute the ratio of overlap between the computed
			# bounding box and the bounding box in the area list
			overlap = float(w * h) / area[j]
 
			# if there is sufficient overlap, suppress the
			# current bounding box
			if overlap > overlapThresh:
				suppress.append(pos)
 
		# delete all indexes from the index list that are in the
		# suppression list
		idxs = np.delete(idxs, suppress)
 
	# return only the bounding boxes that were picked
	return boxes[pick]

def component():
  return random.randint(0,255)

# Interval 
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

##################### Setting parameters 
# Mac parameters
#s_x = 480
#s_y = 360
#first_x = 170
#first_y = 395
#pos = [(first_x, first_y), (first_x, first_y+320), (first_x+1070, first_y-320),(first_x+1070, first_y), (first_x+1070, first_y+320)]
#ww = 315
#hh = 188
#printscreen =  np.array(ImageGrab.grab(bbox=(s_x,s_y,2600,1340)))
#cv2.imwrite('capture.png',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))

# Windows parameters
first_x = 427
first_y = 431
pos = [(first_x, first_y), (first_x, first_y+216), (first_x+722, first_y-216),(first_x+722, first_y), (first_x+722, first_y+216), (first_x, first_y+216+216), (first_x+722, first_y+216+216)]
table_name = ['聚寶廳 LB002', '聚寶廳 LB004', '聚寶廳 LB001', '聚寶廳 LB003', '聚寶廳 LB005', '聚龍廳 B002', '聚龍廳 B004', '聚龍廳 B001', '聚龍廳 B003', '聚龍廳 B005', '聚龍廳 B006', '聚龍廳 B007']
ww = 212
hh = 126
s_x = 310
s_y = 180

# Sending Info.
def sendmeg():

    #cap first image
    printscreen = np.array(ImageGrab.grab()) 
    cv2.imwrite('capture1.png',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    print('cap1')

    #using hotkey control the calibet change to second page
    hotkey('ctrl', 'tab')
    
    #cap second image
    printscreen = np.array(ImageGrab.grab()) 
    cv2.imwrite('capture2.png',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    print('cap2')
    
    #using hotkey control the calibet Return to first page
    hotkey('ctrl', 'tab')

    img_rgb1 = cv2.imread('capture1.png')
    img_rgb2 = cv2.imread('capture2.png')
    img_rgbs = [img_rgb1, img_rgb2]
    final_result = ""
    table = 0
    img_control = 0
    report = []
    #foreach cap img
    for img_rgb in img_rgbs:
        #foreach position
        for xx, yy in pos:
            if img_control == 0 and table >4:
                break
            img_sub = img_rgb[int(yy-10):int(yy+hh+10), int(xx-5):int(xx+ww+5)]
            game_sort = []

            for t in tem:

                #col = (component(),component(),component())
                template = cv2.imread(t)

                # Mac parameters
                #template = cv2.resize(template, (18,18))
                #w, h = template.shape[0:2]
                #res = cv2.matchTemplate(img_sub,template,cv2.TM_CCOEFF_NORMED)
                #threshold = 0.55
                
                # Windows parameters
                template = cv2.resize(template, (13,13))
                w, h = template.shape[0:2]
                res = cv2.matchTemplate(img_sub,template,cv2.TM_CCOEFF_NORMED)
                threshold = 0.55
                loc = np.where( res >= threshold)

                boundingbox = []
                for pt in zip(*loc[::-1]):
                    boundingbox.append([pt[0],pt[1], pt[0]+w, pt[1]+h])
                # perform non-maximum suppression on the bounding boxes
                loc = non_max_suppression_slow(np.array(boundingbox), 0.5)
                for pt in loc:

                    #cv2.rectangle(img_sub, (pt[0],pt[1]), (pt[2], pt[3]), col, 1)
                    game_sort.append([t[0], int(int(pt[0])/12), int(int(pt[1])/12)])
            game_sort = sorted(game_sort, key = lambda game_sort: (game_sort[1], game_sort[2]))
            game_sort.reverse()
            print(len(game_sort))
            table_info = ""
            if len(game_sort) > 0:
                for iii in range(len(game_sort)):
                    table_info += strategy_dicR[game_sort[iii][0]]
            
            report.append([table_name[table], table_info[::-1]])
            table += 1

        img_control += 1
    print('---------------------------------') 

    #send message
    Users_data = np.load("Database.npy")
    for i in range(len(Users_data)):
        if i > 0:
            if Users_data[i][6] != "" and Users_data[i][7] == '1':
                try:
                    url_or_not = False
                    for k in range(5):
                        message_ornot = False
                        for j in range(len(report)):
                            if Users_data[i][k+1] in report[j][1][len(Users_data[i][k+1])*-1:]:
                                if message_ornot == False and url_or_not == False:
                                    line_bot_api.push_message(Users_data[i][0], TextSendMessage("-------------------------------"))
                                if message_ornot == False:
                                    line_bot_api.push_message(Users_data[i][0], TextSendMessage("--套路 "+str(k+1)+" 符合通知--"))
                                combinemessage = "「"+str(report[j][0])+"」\n"
                                combinemessage += "目前牌路為「"+report[j][1][-8:]+"」\n"
                                combinemessage += "符合您設定的牌路「"+Users_data[i][k+1]+"」"
                                line_bot_api.push_message(Users_data[i][0], TextSendMessage(combinemessage))
                                message_ornot = True
                                url_or_not = True
                    if url_or_not:
                        
                        line_bot_api.push_message(Users_data[i][0], TextSendMessage("--快速連結--"))
                        line_bot_api.push_message(Users_data[i][0], TextSendMessage("https://www.win7889.net/"))
                        

                except:
                    excc = ""
    


#Line app setting
app = Flask(__name__)

line_bot_api = LineBotApi('+Jgyg3wv6IdzR4KAUz9rIY81BkJV9oTBfOlZ9aYDpsNSUO7MjK9ezaqiqRguBHrOvMjTIVoGK6wIi3nAMHFD/Fr7BnkQxt0f9GGLjOYHaMOns18QqUM81KLNinhxcViBZpluOfoi9d5hhnlEbE3ynwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e932e9253cab105336c606bf6f9fa7f6')
my_id = "Ud3635ab30831e9f1ca5bef2d4a1e4c54"

help_strings = "請跟著以下步驟設定套路："
help_strings += "\n\n1. 輸入「套路1=莊閒和」，完成第一組套路設定，範例：「套路1=莊閒莊和」。（可重新設定）"
help_strings += "\n\n2. 輸入「套路2=莊閒和」，完成第二組套路設定，範例：「套路2=莊莊閒」。（可重新設定）"
help_strings += "\n\n   設定多組套路以此類推......."
help_strings += "\n\nPs1. 每組帳號總共五組套路可設定。"
help_strings += "\n\nPs2. 輸入「刪除套路N」，即可刪除第N組套路，範例：「刪除套路2」。"
#Starting sending messages 
set_interval(sendmeg, 20)

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

@handler.add(PostbackEvent)
def handle_postback(event):

    
    if event.postback.data == "註冊":
        strange_id = event.source.user_id
        Users_data = np.load("Database.npy")
        if any (strange_id in s[0] for s in Users_data):
            for i in range(len(Users_data)):
                if i > 0:

                    if Users_data[i][6] != "":
                        print("already register")
                        line_bot_api.reply_message(event.reply_token,TextSendMessage("重複註冊！"))
                    else:
                        print("not support lineID")
                        line_bot_api.reply_message(event.reply_token,TextSendMessage("尚未提供LineID，請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。！"))

        else:
            print(event.source.user_id)
            Users_data = np.append(Users_data, [[strange_id, "無", "無", "無", "無", "無", "", 1]], axis=0)
            np.save("Database.npy", Users_data)
            line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。"))

    elif event.postback.data == '開啟':
        strange_id = event.source.user_id
        Users_data = np.load("Database.npy")
        open_i = 0
        for i in range(len(Users_data)):
            if strange_id in Users_data[i][0]:
                open_i = i
                break
        if open_i != 0:
            Users_data[open_i][7] =  1
            np.save("Database.npy", Users_data)
            print("Close Notice")
            line_bot_api.reply_message(event.reply_token,TextSendMessage("報牌通知開啟！"))

    
    elif event.postback.data == "Confirm":

        strange_id = event.source.user_id
        Users_data = np.load("Database.npy")
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
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
        else:
            print("weird guy")
            line_bot_api.reply_message(event.reply_token,TextSendMessage("您尚未註冊！"))

    elif event.postback.data == "取消":
        strange_id = event.source.user_id
        Users_data = np.load("Database.npy")
        stop_i = 0
        for i in range(len(Users_data)):
            if strange_id in Users_data[i][0]:
                stop_i = i
                break
        if stop_i != 0:
            Users_data[stop_i][7] =  0
            np.save("Database.npy", Users_data)
            print("Close Notice")
            line_bot_api.reply_message(event.reply_token,TextSendMessage("報牌通知關閉！"))

    
    elif event.postback.data == "使用教學":
        some_onesId = event.source.user_id
        line_bot_api.push_message(some_onesId,TextSendMessage(help_strings))

    elif  event.postback.data == "套路清單":
        
        strange_id = event.source.user_id
        
        Users_data = np.load("Database.npy")
        
        if any (strange_id in s[0] for s in Users_data):
            for i in range(len(Users_data)):
                if strange_id in Users_data[i][0]:
                    if Users_data[i][6] != "":
                        list_strategys = "您的套路清單："
                        for j in range(6):
                            if j != 0:
                                list_strategys += "\n\n套路"+str(j)+" = "+Users_data[i][j]
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(list_strategys))
                    else:
                        print("not support lineID")
                        line_bot_api.reply_message(event.reply_token,TextSendMessage("尚未提供LineID，請輸入您的LineID，格式「ID=xxxxxx」。\n\n若未正確設定LineID將無法使用報牌系統。！"))


        else:
            print(event.source.user_id)
            line_bot_api.reply_message(event.reply_token,TextSendMessage("您尚未註冊！"))

        

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if "套路" in event.message.text and "=" in event.message.text or "套路" in event.message.text and "＝" in event.message.text:
        strange_id = event.source.user_id
        strategy = ""
        try:
        
            strategy = event.message.text.split('＝')[1]
        
        except:
        
            strategy = event.message.text.split('=')[1]
        
        Users_data = np.load("Database.npy")
        
        if any (strange_id in s[0] for s in Users_data):
            try:
                for i in range(len(Users_data)):
                    if strange_id in Users_data[i][0]:
                        cus_strategy = ""

                        for key in strategy:
                            cus_strategy += strategy_dic[key]
                        Users_data[i][int(event.message.text[2])] =  cus_strategy
                        line_bot_api.reply_message(event.reply_token,TextSendMessage("套路設定成功！"))
            except:
                some_onesId = event.source.user_id
                line_bot_api.push_message(some_onesId,TextSendMessage("請檢查是否有錯字，範例：「套路1=莊閒莊閒」。"))

        else:
            print(event.source.user_id)
            line_bot_api.reply_message(event.reply_token,TextSendMessage("欲設定請先註冊！"))
        np.save("Database.npy", Users_data)

    

    elif "刪除套路" in event.message.text:
        strange_id = event.source.user_id
        strategy = ""
        try:
        
            int(event.message.text[4])
            Users_data = np.load("Database.npy")
        
            if any (strange_id in s[0] for s in Users_data):
                for i in range(len(Users_data)):
                    if strange_id in Users_data[i][0]:
                        Users_data[i][int(event.message.text[4])] =  "無"
                        line_bot_api.reply_message(event.reply_token,TextSendMessage("套路"+event.message.text[4]+"已刪除！"))
            else:
                print(event.source.user_id)
                line_bot_api.reply_message(event.reply_token,TextSendMessage("欲設定請先註冊！"))
            np.save("Database.npy", Users_data)
        
        except:
        
            print('delete_type_fail')
            line_bot_api.reply_message(event.reply_token,TextSendMessage("請檢查是否有錯字，範例：「刪除套路1」。"))

        
    elif "ID" in event.message.text or "id" in event.message.text:
        strange_id = event.source.user_id
        Lineid = ""
        try:
        
            Lineid = event.message.text.split('＝')[1]
        
        except:
        
            Lineid = event.message.text.split('=')[1]

        Users_data = np.load("Database.npy")
        user_i = 0
        if any (strange_id in s[0] for s in Users_data):
            for i in range(len(Users_data)):
                if strange_id in Users_data[i][0]:
                    user_i = i
                    break
            if user_i != 0:
                Users_data[user_i][6] =  Lineid
                np.save("Database.npy", Users_data)
                print("Add user line ID")
                line_bot_api.reply_message(event.reply_token,TextSendMessage("註冊成功！"))
        else:
            print("weird guy")
            line_bot_api.reply_message(event.reply_token,TextSendMessage("您尚未註冊！"))

    


    
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
        
        line_bot_api.reply_message(event.reply_token, message)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)