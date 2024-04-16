import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


aweight = 0.5
num_frames = 0
bg = None

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
        roi = frame[100:300, 300:500]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        cv2.imshow('frame', clone)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

print(first_number, operator, second_number)
cv2.waitKey()
cv2.destroyAllWindows()
