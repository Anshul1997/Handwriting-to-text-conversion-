import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import loadmat
import  pickle
from scipy.misc import toimage
from PIL import Image, ImageFilter
from scipy.misc import toimage
from keras.models import model_from_yaml
import importlib

importlib.import_module('separate_chars')

from image_prepare import imageprepare
from load_model import loaded_model,mapping
from separate_chars import all_chars_count
from separate_words import all_words_count
from separate_lines import number_lines


f=open("converted_file.txt","w+")

for lines in range(0,number_lines):
    for words in range(0,all_words_count[lines]):
        for chars in range(0,all_chars_count[lines][words]):
            # get the image details
            filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_chars/char_%d_%d_%d.jpg"%(lines,words,chars)
            X_test = imageprepare(filename)
            X_test = np.asarray(X_test)
            X_test = np.reshape(X_test,(28,28))
            plt.imshow(X_test)
            plt.show()
            #print(X_test)
            X_test = X_test.reshape(1, 28, 28, 1).astype('float32')
            X_test = X_test / 255

            # evaluate loaded model on test data
            loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
            classes = loaded_model.predict(X_test)
            #print(classes)
            prediction = chr(mapping[(int(np.argmax(classes, axis=1)[0]))])
            confidence = str(max(classes[0]) * 100)[:6]
            response = {'prediction': chr(mapping[(int(np.argmax(classes, axis=1)[0]))]),
                        'confidence': str(max(classes[0]) * 100)[:6]}
            print(response)
            if confidence>"30" :
               f.write(prediction)
            else :
               f.write("")
        f.write(" ")
    f.write("\n")
f.close()
importlib.import_module('nlp_convert')
