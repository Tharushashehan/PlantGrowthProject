#For more info [https://docs.opencv.org/trunk/d3/db4/tutorial_py_watershed.html]


from functools import wraps
from flask import (
    current_app,
    jsonify,
    request,
)

from PlantGrowthProject import app
import sys
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
from flask import render_template, json, json, make_response, Response
from PlantGrowthProject import app
from flask.app import Flask
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
from flask import Flask, request
from werkzeug import secure_filename
from flask import send_file
from .ProcessImg import *
import mahotas

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class ClsCompromise:

    def Compromise(self):
        #Detection of color green
        #START
        # load the image
        #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\5.JPG)
        #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\6.JPG") #Input the image
        image = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\Capture.png")

        #Color detection Green color
        #START

        # define range of green color in RGB
        lower_green = np.array([17, 15, 100], dtype = "uint8") #60,100,50
        upper_green = np.array([50, 56, 200], dtype = "uint8") #60,255,255

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower_green, upper_green)
        output = cv2.bitwise_and(image, image, mask = mask)
        #END

        #the Otsu's binarization
        gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1

        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0
        markers = cv2.watershed(output,markers)
        output[markers == -1] = [255,0,0]

        nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
        numberAll = thresh.size #this gives number of all pixels you have in the image
        print(nWhitePixels)
        print(numberAll)

        cv2.imshow("images", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print ("Tharusha shehan")
        return

    def Comp02(self):
        print("***************************************")
        print("Tharusha shehan")
        print("***************************************")
        return "Hei"

    def AjaxCompromise(self):
        target = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        lstOfUploadedImages = os.listdir(os.path.join(APP_ROOT, 'images/'))
        ArrangedImages = sorted(lstOfUploadedImages)
        nBlackPixelArrylst = list()
        nAllPixelArrylst = list()

        for nImage in ArrangedImages:
            destination = "/".join([target, nImage])
            #Detection of color green
            #START
            # load the image
            imageNoHSV = cv2.imread(destination)
            image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

            #Color detection Green color
            #START
            # define range of green color in HSV
            lower_green0 = np.array([45, 100, 50], dtype = "uint8")
            lower_green1 = np.array([60, 100, 50], dtype = "uint8")
            upper_green0 = np.array([60, 255, 255], dtype = "uint8")
            upper_green1 = np.array([75, 255, 255], dtype = "uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask0 = cv2.inRange(image, lower_green0, upper_green0)
            mask1 = cv2.inRange(image, lower_green1, upper_green1)

            #mask = cv2.inRange(image, lower_green, upper_green)
            output = cv2.bitwise_or(image, image, mask = mask0 + mask1)
            #END

            #the Otsu's binarization
            output02 = cv2.cvtColor(output,cv2.COLOR_HSV2BGR)       
            gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg,sure_fg)

            # Marker labelling
            ret, markers = cv2.connectedComponents(sure_fg)

            # Add one to all labels so that sure background is not 0, but 1
            markers = markers+1

            # Now, mark the region of unknown with zero
            markers[unknown==255] = 0
            markers = cv2.watershed(output,markers)
            output[markers == -1] = [255,0,0]

            nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
            numberAll = thresh.size #this gives number of all pixels you have in the image

            nBlackPixel = numberAll - nWhitePixels
            nBlackPixelArrylst.append(nBlackPixel)
            nAllPixelArrylst.append(numberAll)

            #cv2.imshow("images", thresh)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

        FrameSize = "Test"
        f_read = open('FrameSize.txt', encoding='utf-8')
        for line in f_read:
            FrameSize = line
        f_read.close()

        jObj = {}
        jObj["FrameSize"]=FrameSize
        jObj["nBlackPixelArrylst"] = nBlackPixelArrylst
        jObj["nAllPixelArrylst"] = nAllPixelArrylst
        return Response(json.dumps(jObj), mimetype='application/json')

    def Comp03(self):
        
        #Getting the FrameSize input and saving that in a txt file
        #START
        FrameSize = request.form["FrameSize"]
        with open("FrameSize.txt", "w+") as f_write:
            f_write.write(FrameSize)
        #END

        target = os.path.join(APP_ROOT, 'images/')

        if not os.path.isdir(target):
            os.mkdir(target)

        #here we save output examples
        targetForOutput = os.path.join(APP_ROOT, 'imagesOut/')
        if not os.path.isdir(targetForOutput):
            os.mkdir(targetForOutput)

        nBlackPixelArrylst = list()
        nAllPixelArrylst = list()
        noOfFiles = len(request.files.getlist("file"))
        if noOfFiles>1:
            for upFile in request.files.getlist("file"):
                
                filename = upFile.filename
                destination = "/".join([target, filename])
                
                upFile.save(destination)
                #Detection of color green
                #START
                # load the image
                imageNoHSV = cv2.imread(destination)
                image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

                #Color detection Green color
                #START

                # define range of green color in RGB

                lower_green0 = np.array([45, 100, 50], dtype = "uint8") 
                lower_green1 = np.array([60, 100, 50], dtype = "uint8") 
                upper_green0 = np.array([60, 255, 255], dtype = "uint8") 
                upper_green1 = np.array([75, 255, 255], dtype = "uint8") 

                # find the colors within the specified boundaries and apply
                # the mask

                mask0 = cv2.inRange(image, lower_green0, upper_green0)
                mask1 = cv2.inRange(image, lower_green1, upper_green1)

                #mask = cv2.inRange(image, lower_green, upper_green)
                output = cv2.bitwise_or(image, image, mask = mask0 + mask1)
                #END

                #the Otsu's binarization
                output02 = cv2.cvtColor(output,cv2.COLOR_HSV2BGR) 
                gray = cv2.cvtColor(output02,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
                ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                # noise removal
                kernel = np.ones((3,3),np.uint8)
                opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

                # sure background area
                sure_bg = cv2.dilate(opening,kernel,iterations=3)

                # Finding sure foreground area
                dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
                ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

                # Finding unknown region
                sure_fg = np.uint8(sure_fg)
                unknown = cv2.subtract(sure_bg,sure_fg)

                # Marker labelling
                ret, markers = cv2.connectedComponents(sure_fg)

                # Add one to all labels so that sure background is not 0, but 1
                markers = markers+1

                # Now, mark the region of unknown with zero
                markers[unknown==255] = 0
                markers = cv2.watershed(imageNoHSV,markers)
                imageNoHSV[markers == -1] = [255,0,0]

                cv2.imshow("images", dist_transform)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
                numberAll = thresh.size #this gives number of all pixels you have in the image

                nBlackPixel = numberAll - nWhitePixels
                nBlackPixelArrylst.append(nBlackPixel)
                nAllPixelArrylst.append(numberAll)

                filename = upFile.filename
                destinationForOutput = "/".join([targetForOutput, filename])
                cv2.imwrite(destinationForOutput, thresh)

                #cv2.imshow("images", thresh)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

        ObjData = {}
        ObjData["nBlackPixelArrylst"] = nBlackPixelArrylst
        ObjData["nAllPixelArrylst"] = nAllPixelArrylst
        jsonData = json.dumps(ObjData)

        response = make_response(render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'))
        
        response.headers.set('Content-Security-Policy', "default-src 'self'")
        response.jsonData = jsonData

        #return response
        return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.',
        jsonData = jsonData)

    def JsegAPI(self):
        target = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        lstOfUploadedImages = os.listdir(os.path.join(APP_ROOT, 'images/'))
        ArrangedImages = sorted(lstOfUploadedImages)
        nBlackPixelArrylst = list()
        nAllPixelArrylst = list()

        for nImage in ArrangedImages:
            destination = "/".join([target, nImage])
            #Detection of color green
            #START
            # load the image
            imageNoHSV = cv2.imread(destination)
            image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

            #Color detection Green color
            #START
            # define range of green color in HSV
            lower_green0 = np.array([45, 100, 50], dtype = "uint8")
            lower_green1 = np.array([60, 100, 50], dtype = "uint8")
            upper_green0 = np.array([60, 255, 255], dtype = "uint8")
            upper_green1 = np.array([75, 255, 255], dtype = "uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask0 = cv2.inRange(image, lower_green0, upper_green0)
            mask1 = cv2.inRange(image, lower_green1, upper_green1)

            #mask = cv2.inRange(image, lower_green, upper_green)
            output = cv2.bitwise_or(image, image, mask = mask0 + mask1)
            #END

            #the Otsu's binarization
            output02 = cv2.cvtColor(output,cv2.COLOR_HSV2BGR)       
            gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

           

            nWhitePixels = cv2.countNonZero(opening) #this gives number of white pixels you have in the image
            numberAll = opening.size #this gives number of all pixels you have in the image

            nBlackPixel = numberAll - nWhitePixels
            nBlackPixelArrylst.append(nBlackPixel)
            nAllPixelArrylst.append(numberAll)

            #cv2.imshow("images", thresh)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

        FrameSize = "Test"
        f_read = open('FrameSize.txt', encoding='utf-8')
        for line in f_read:
            FrameSize = line
        f_read.close()

        jObj = {}
        jObj["FrameSize"]=FrameSize
        jObj["nBlackPixelArrylst"] = nBlackPixelArrylst
        jObj["nAllPixelArrylst"] = nAllPixelArrylst
        return Response(json.dumps(jObj), mimetype='application/json')
