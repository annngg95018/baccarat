
import numpy as np
from PIL import ImageGrab
import cv2
import time

import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
def screen_record(): 
    printscreen =  np.array(ImageGrab.grab(bbox=(480,360,2600,1270)))
    cv2.imwrite('capture.png',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
    print('cap')


set_interval(screen_record, 2)




