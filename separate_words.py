import cv2
from matplotlib import pyplot as plt

from sort_contours import sort_contours
from separate_lines import number_lines

all_words_count=[]*number_lines

for lines in range(0,number_lines):
    filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_lines/line_%d.jpg"%(lines)
    image = cv2.imread(filename,0)
    image = cv2.medianBlur(image,5)
    #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale

    thresh=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY_INV,19,10)
    #plt.imshow(thresh)
    #plt.show()
    #_,thresh = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
    #threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    #erosion = cv2.erode(thresh,kernel,iterations = 0)
    #th = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    dilated = cv2.dilate(thresh,kernel,iterations = 30) # dilate
    plt.imshow(dilated)
    plt.show()
    #dilated = cv2.dilate(erosion,kernel,iterations = 25) # dilate
    #plt.imshow(dilated)
    #plt.show()
    _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    number_words=0
    # get contours
    #count contours
    count=0
    for i in contours:
        count+=1
    if count==0:
        continue
    # sort contours
    contours = sort_contours(contours, method="left-to-right")

    for contour in contours:

        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        #print([x,y,w,h])
        # discard areas that are too large

        #if h>400 and w>400:
        #   continue

        # discard areas that are too small

        if h<70 or w<70:
           continue
        # draw rectangle around contour on original image

        #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
        # save each part as a separate image

        crop_img = image[y:y+h, x:x+w]
        cv2.imshow("cropped", crop_img)
        cv2.waitKey(0)
        filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_words/word_%d_%d.jpg"%(lines,number_words)
        cv2.imwrite(filename, crop_img)
        number_words+=1
        # write original image with added contours to disk
    all_words_count.append(number_words)
