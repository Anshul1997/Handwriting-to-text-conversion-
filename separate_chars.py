import cv2
from matplotlib import pyplot as plt

from sort_contours import sort_contours
from separate_words import all_words_count
from separate_lines import number_lines

all_chars_count=[[0 for x in range(max(all_words_count))] for y in range(number_lines)]
ax=[]*1000
ay=[]*1000
aw=[]*1000
ah=[]*1000

for lines in range(0,number_lines):
    for words in range(0,all_words_count[lines]):
        filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_words/word_%d_%d.jpg"%(lines,words)
        image = cv2.imread(filename,0)
        image = cv2.medianBlur(image,5)
        #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale

        thresh=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                   cv2.THRESH_BINARY_INV,19,10)
        #plt.imshow(thresh)
        #plt.show()
        #_,thresh = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
        # threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        #erosion = cv2.erode(thresh,kernel,iterations = 0)
        #plt.imshow(erosion)
        #plt.show()
        dilated = cv2.dilate(thresh,kernel,iterations = 3) # dilate
        plt.imshow(dilated)
        plt.show()
        _, contours, _ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        number_chars=0
        # get contours
        #count contours
        count=0
        for i in contours:
            count+=1
        if count==0:
            continue
        # sort contours
        contours = sort_contours(contours, method="left-to-right")
        #print(contours)
        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            print ("current ")
            print ([x,y,w,h])
            if number_chars==0:
                ax.append(x)
                ay.append(y)
                aw.append(w)
                ah.append(h)
                print ("modified ")
                print ([ax[number_chars],ay[number_chars],aw[number_chars],ah[number_chars]])
                print("\n")
                number_chars+=1
                continue
            pcp=ax[number_chars-1]+(aw[number_chars-1]/2)
            ccp=x+w/2
            if(abs(pcp-ccp)>25):
                ax.append(x)
                ay.append(y)
                aw.append(w)
                ah.append(h)
                print ("modified ")
                print ([ax[number_chars],ay[number_chars],aw[number_chars],ah[number_chars]])
                print("\n")
                number_chars+=1
                continue
            if x<ax[number_chars-1]:
                ax[number_chars-1]=x
            if y<ay[number_chars-1]:
                ay[number_chars-1]=y
            if w>aw[number_chars-1]:
                aw[number_chars-1]=w+5
            else:
                aw[number_chars-1]+=5
            ah[number_chars-1]=h+ah[number_chars-1]+10
            print ("modified ")
            print ([ax[number_chars-1],ay[number_chars-1],aw[number_chars-1],ah[number_chars-1]])
            print("\n")

        count=0
        for i in range(0,number_chars):

            # get rectangle bounding contour
            #print(contour)
            [x,y,w,h] = [ax[i],ay[i],aw[i],ah[i]]

            # discard areas that are too large

            if h>300 and w>300:
                continue

            # discard areas that are too small

            if h<40 and w<40:
                print("low")
                continue
            if h<30:
                continue
            # draw rectangle around contour on original image

            #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
            # save each part as a separate image

            crop_img = image[y:y+h, x:x+w]
            cv2.imshow("cropped", crop_img)
            cv2.waitKey(0)
            filename = "/home/anshul/Desktop/handwritten to text/OCR/Separated_chars/char_%d_%d_%d.jpg"%(lines,words,count)
            cv2.imwrite(filename, crop_img)
            count+=1
        # write original image with added contours to disk
        all_chars_count[lines][words]=count
        ax.clear()
        ay.clear()
        aw.clear()
        ah.clear()
