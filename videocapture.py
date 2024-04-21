import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from segment import *
from calculator import *
from model import *
from video_processing import *

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
                # print("Some part of hand is detecting")
                contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                if num < 90:
                    cv2.putText(clone, 'Calculator Ready', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 90 and num < 150:
                    cv2.putText(clone, 'Enter the first Number', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 481 and num < 540:
                    cv2.putText(clone, "Confirmed", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    wor = "The first number is " + first_number
                    cv2.putText(clone, wor, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 540 and num < 660:
                    cv2.putText(clone, "Enter the operator", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 721 and num < 781:
                    cv2.putText(clone, "Confirmed", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    cv2.putText(clone, operator, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 781 and num < 840:
                    cv2.putText(clone, 'Enter the Second Number', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                3)

                elif num > 1201 and num < 1261:
                    cv2.putText(clone, "Confirmed", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    wor = "The second number is " + second_number
                    cv2.putText(clone, wor, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                elif num > 1300:
                    res = calculate(first_number, operator, second_number)
                    in_line = first_number + operator + second_number + " = " + str(res)
                    cv2.putText(clone, "The answer is ", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    cv2.putText(clone, in_line, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                elif num > 1800:
                    print("destroy window")
                    cap.release()
                    cv2.destroyAllWindows()
                print(len(contours))
                for cnt in contours:
                    if cv2.contourArea(cnt) > 2500:
                        # print("Hand detecting for prediction")

                        if num > 150 and num < 481:
                            cv2.putText(clone, first_number, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                            if num % 60 == 0:
                                pred = get_prediction(thresholded)
                                if pred != "Confirm" and pred != "Clear":
                                    first_number = first_number + pred
                                elif pred == "Clear":
                                    num = 91
                                    first_number = ""
                                else:
                                    num = 481

                        elif num > 660 and num < 721:
                            pred = get_prediction(thresholded)
                            operator = pred
                            if pred == "Clear":
                                num = 661
                                operator = ""

                        elif num > 841 and num < 1201:
                            cv2.putText(clone, second_number, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                            if num % 60 == 0:
                                pred = get_prediction(thresholded)
                                if pred != "Confirm" and pred != "Clear":
                                    second_number = second_number + pred
                                elif pred == "Clear":
                                    num = 782
                                    second_number = ""
                                else:
                                    num = 1201
                        elif num > 1300:
                            if num % 60 == 0:
                                pred = get_prediction(thresholded)
                                if pred == "Clear":
                                    num = 0
                                    first_number = ""
                                    operator = ""
                                    second_number = ""

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
