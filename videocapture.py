import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from segment import *

def accumulate(img,aweight):
    global bg
    if bg is None:
        bg = img.copy().astype('float')
        return
    cv2.accumulateWeighted(img,bg,aweight)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


aweight = 0.5
num_frames = 0
bg = None
working_area_rect_left = (600, 100)
working_area_rect_right = (800, 300)
roi_y = (working_area_rect_left[1], working_area_rect_right[1])
roi_x = (working_area_rect_left[0], working_area_rect_right[0])

num = 0
first_number = ""
operator = ""
second_number = ""

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret ==True:
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        (height, width) = frame.shape[:2]
        roi = frame[roi_y[0]:roi_y[1], roi_x[0]:roi_x[1]]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            accumulate(gray, aweight)
        else:
            hand = segment(gray, bg)

            if hand is not None:
                (thresholded, segmented) = hand
                num = num + 1
                cv2.drawContours(clone, [segmented + working_area_rect_left], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)
                print("Some part of hand is detecting")
                contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

      
        cv2.rectangle(clone, working_area_rect_left, working_area_rect_right, (0, 255, 255), 2)
        num_frames += 1
        cv2.imshow('frame', clone)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
print(first_number, operator, second_number)
cv2.waitKey()
cv2.destroyAllWindows()
