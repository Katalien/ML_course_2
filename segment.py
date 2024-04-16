import cv2

def segment(img, bg, thres=25):
    diff = cv2.absdiff(bg.astype('uint8'), img)
    _, thresholded = cv2.threshold(diff, thres, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return
    else:
        segmented = max(contours, key=cv2.contourArea)
    return (thresholded, segmented)