import cv2
from matplotlib import pyplot as plt

from sort_contours import sort_contours

image = cv2.imread("/home/anshul/Desktop/ImageToMNIST/image68.jpeg",0)
#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
image = cv2.medianBlur(image,5)
#plt.imshow(image)
#plt.show()
thresh=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,19,10)

#_,thresh = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
#plt.imshow(thresh)
#plt.show()
#threshold
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#erosion = cv2.erode(thresh,kernel,iterations = 1)
#plt.imshow(erosion)
#plt.show()
th = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
dilated = cv2.dilate(th,kernel,iterations = 30) # dilate
plt.imshow(dilated)
plt.show()
x, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
number_lines=0
# get contours
# for each contour found, draw a rectangle around it on original
#image

contours = sort_contours(contours, method="top-to-bottom")
lx=-1
mx=2000
ly=-1
my=2000
for contour in contours:

    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)
    #print("initial")
    #print([x,y,w,h])
    if lx!=-1 and ly!=-1:
       if abs(ly-y)<100:
          if x<lx:
              lx=x
          if(mx<x+w):
              mx=x+w
          if y<ly:
              ly=y
          if(my<y+h):
              my=y+h
          number_lines-=1
          #print("modified")
          #print([lx,ly,mx,my])
          crop_img = image[ly:my, lx:mx]
          #cv2.imshow("cropped", crop_img)
          cv2.waitKey(0)
          filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_lines/line_%d.jpg"%(number_lines)
          cv2.imwrite(filename, crop_img)
          number_lines+=1
          continue
    # discard areas that are too large

    #if h>300 and w>300:
    #    continue

    # discard areas that are too small

    if h<60 or w<60:
        continue
    # draw rectangle around contour on original image

    #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
    # save each part as a separate image
    crop_img = image[y:y+h, x:x+w]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_lines/line_%d.jpg"%(number_lines)
    cv2.imwrite(filename, crop_img)
    [lx,ly,mx,my]=[x,y,x+w,y+h]
    number_lines+=1
# write original image with added contours to disk
