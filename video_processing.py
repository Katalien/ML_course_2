import cv2
from segment import *
from calculator import *
from model import *


def add_video_text(num, clone, first_number, operator, second_number):
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
        cv2.putText(clone, 'Enter the Second Number', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    elif num > 1201 and num < 1261:
        cv2.putText(clone, "Confirmed", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        wor = "The second number is " + second_number
        cv2.putText(clone, wor, (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    elif num > 1300:
        res = calculate(first_number,operator,second_number)
        in_line = first_number + operator + second_number + " = " + str(res)
        cv2.putText(clone, "The answer is ", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(clone,in_line,(50,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
    elif num > 1800:
        cap.release()
        cv2.destroyAllWindows()


def process_frames(contours, num, clone, thresholded, first_number, operator, second_number ):
    for cnt in contours:
        if cv2.contourArea(cnt) > 5000:
            print("Hand detecting for prediction")

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
