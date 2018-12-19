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

import numpy as np
from PIL import ImageGrab
import cv2
import time

import threading

import cv2
import numpy as np
from matplotlib import pyplot as plt

#Image detection region 
tem = ['Peace.png', 'Home.png', 'Client.png']

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

# Sending Info.
def sendmeg():
    s_x = 480
    s_y = 360
    printscreen =  np.array(ImageGrab.grab(bbox=(s_x,s_y,2600,1340)))
    cv2.imwrite('capture.png',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    print('cap')


    img_rgb = cv2.imread('capture.png')
    first_x = 170
    first_y = 395



    pos = [(first_x, first_y), (first_x, first_y+320), (first_x+1070, first_y-320),(first_x+1070, first_y), (first_x+1070, first_y+320)]
    ww = 315
    hh = 188
    final_result = ""
    table = 1
    for xx, yy in pos:
        img_sub = img_rgb[int(yy-10):int(yy+hh+10), int(xx-5):int(xx+ww+5)]
        game_sort = []

        for t in tem:

            col = (component(),component(),component())
            template = cv2.imread(t)
            template = cv2.resize(template, (18,18))
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

                cv2.rectangle(img_sub, (pt[0],pt[1]), (pt[2], pt[3]), col, 1)
                game_sort.append([t[0], int(int(pt[0])/12), int(int(pt[1])/12)])
        game_sort = sorted(game_sort, key = lambda game_sort: (game_sort[1], game_sort[2]))
        game_sort.reverse()
        print(len(game_sort))
        final_result += "table"+str(table)+"="
        if len(game_sort) > 4:
            for iii in range(5):
                final_result += game_sort[iii][0]+":"
        final_result += "\n"
        final_result += "\n"
        table += 1
    print('---------------------------------') 
    line_bot_api.push_message( my_id, TextSendMessage(final_result))


#Line app setting
app = Flask(__name__)

line_bot_api = LineBotApi('+Jgyg3wv6IdzR4KAUz9rIY81BkJV9oTBfOlZ9aYDpsNSUO7MjK9ezaqiqRguBHrOvMjTIVoGK6wIi3nAMHFD/Fr7BnkQxt0f9GGLjOYHaMOns18QqUM81KLNinhxcViBZpluOfoi9d5hhnlEbE3ynwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e932e9253cab105336c606bf6f9fa7f6')
my_id = "Ud3635ab30831e9f1ca5bef2d4a1e4c54"

#Starting sending messages 
set_interval(sendmeg, 10)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("翔祐"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)