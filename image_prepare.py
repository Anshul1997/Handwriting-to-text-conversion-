import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import loadmat
import  pickle
from scipy.misc import toimage
from PIL import Image, ImageFilter
from scipy.misc import toimage
import cv2


def imageprepare(argv):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    #THRESHOLD_VALUE = 0
    #im = Image.open(argv).convert('L')
    #imgData = np.asarray(im)
    #img = (imgData > THRESHOLD_VALUE) * 1.0
    #im=toimage(img)

    image = cv2.imread(argv,0)
    image = cv2.medianBlur(image,5)
    thresh=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,19,10)
    #edges = cv2.Canny(thresh,50,200)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    #dilated = cv2.dilate(thresh,kernel,iterations = 4) # dilate
    erosion = cv2.erode(thresh,kernel,iterations = 2)
    im=toimage(erosion)
    #plt.imshow(im)
    #plt.show()

    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        img=img.filter(ImageFilter.SMOOTH)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas

    tv = list(newImage.getdata())  # get pixel values
    tva=[abs(x-255) for x in tv]
    for x in range(0,len(tva)):
        if (tva[x]>20):
            tva[x]=255
        else:
            tva[x]=0
    return tva
