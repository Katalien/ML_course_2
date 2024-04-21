import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

label = ['0','1','+','-','*','/','Confirm','**','%','Clear','2','3','4','5','6','7','8','9']
model = load_model('model_best.h5')

def get_prediction(img):
    for_pred = cv2.resize(img,(64,64))
    x = img_to_array(for_pred)
    x = x/255.0
    x = x.reshape((1,) + x.shape)
    pred = str(label[np.argmax(model.predict(x))])
    return pred