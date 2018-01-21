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
        #here we save some output examples
        targetForOutput = os.path.join(APP_ROOT, 'imagesOutExample/')
        if not os.path.isdir(targetForOutput):
            os.mkdir(targetForOutput)

        noOfFiles = len(request.files.getlist("file"))
        if noOfFiles == 1:
            filename = "Uploaded.jpg"
            destination = "/".join([targetForOutput, filename])
            request.files.getlist("file")[0].save(destination)    

            #Detection of color green
            #START
            # load the image
            imageNoHSV = cv2.imread(destination)
            image = cv2.cvtColor(imageNoHSV, cv2.COLOR_BGR2HSV)

            #This saves the image
            #START
            filename = "imageOnHSV.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, image)
            #END

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

            #This saves the image
            #START
            filename = "imageWithMask.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, output)
            #END

            #the Otsu's binarization
            output02 = cv2.cvtColor(output,cv2.COLOR_HSV2BGR) 
            gray = cv2.cvtColor(output02,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            #This saves the image
            #START
            filename = "imageAfterOtsu.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, thresh)
            #END

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            #This saves the image
            #START
            filename = "imageAfterNoise.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, opening)
            #END

            # sure foreground area
            fg = cv2.erode(opening,kernel,iterations = 2)

            #This saves the image
            #START
            filename = "imageAfterForeGround.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, fg)
            #END

            # Finding sure background area  
            bgt = cv2.dilate(opening,kernel,iterations = 3)
            ret,bg = cv2.threshold(bgt,1,128,1)

            #This saves the image
            #START
            filename = "imageAfterBackGround.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, bg)
            #END

            # Marker labelling
            marker = cv2.add(fg,bg)
            marker32 = np.int32(marker)

            # Now, Apply the watershed algorithm
            cv2.watershed(imageNoHSV,marker32)
            m = cv2.convertScaleAbs(marker32)

            #This saves the image
            #START
            filename = "waterShedOut.jpg"
            destinationForOutput = "/".join([targetForOutput, filename])
            cv2.imwrite(destinationForOutput, m)
            #END

            #cv2.imshow("images", dist_transform)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            return "The image uploaded successfully"
        else:
            return "Upload only one image at a time"

    def Comp02(self):
        print("***************************************")
        print("Hello World")
        print("***************************************")
        return "Hei"

    def AjaxCompromise(self):

        lstOfUploadedImages = os.listdir(os.path.join(APP_ROOT, 'imagesOut/'))
        target = os.path.join(APP_ROOT, 'imagesOut/')
        ArrangedImages = sorted(lstOfUploadedImages)
        nBlackPixelArrylst = list()
        nAllPixelArrylst = list()

        for nImage in ArrangedImages:
            destination = "/".join([target, nImage])
            #START
            #load the image and calculate the relevent area
            imageToCalculate = cv2.imread(destination)
            imageToCalculateHSV = cv2.cvtColor(imageToCalculate, cv2.COLOR_BGR2HSV)
            lower_white = np.array([0, 0, 0], dtype = "uint8") 
            upper_white = np.array([0, 0, 255], dtype = "uint8")
            whiteMask = cv2.inRange(imageToCalculateHSV, lower_white, upper_white)
            frame = cv2.bitwise_and(imageToCalculate, imageToCalculate, mask= whiteMask)
            frame = cv2.cvtColor(frame,cv2.COLOR_HSV2BGR) 
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ret, frame = cv2.threshold(frame,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            nBlackPixel = cv2.countNonZero(frame) #this gives number of white pixels you have in the image
            numberAll = frame.size #this gives number of all pixels you have in the image

            nWhitePixels = numberAll - nBlackPixel
            nBlackPixelArrylst.append(nWhitePixels) #here after the mask been added region with green color has become the color of white
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

                # sure foreground area
                fg = cv2.erode(opening,kernel,iterations = 2)

                # Finding sure background area
                bgt = cv2.dilate(opening,kernel,iterations = 3)
                ret,bg = cv2.threshold(bgt,1,128,1)

                # Marker labelling
                marker = cv2.add(fg,bg)
                marker32 = np.int32(marker)

                # Now, Apply the watershed algorithm
                cv2.watershed(imageNoHSV,marker32)
                m = cv2.convertScaleAbs(marker32)

                filename = upFile.filename
                destinationForOutput = "/".join([targetForOutput, filename])
                cv2.imwrite(destinationForOutput, m)

                imageToCalculate = cv2.imread(destinationForOutput)
                imageToCalculateHSV = cv2.cvtColor(imageToCalculate, cv2.COLOR_BGR2HSV)
                lower_white = np.array([0, 0, 0], dtype = "uint8") 
                upper_white = np.array([0, 0, 255], dtype = "uint8")
                whiteMask = cv2.inRange(imageToCalculateHSV, lower_white, upper_white)
                frame = cv2.bitwise_and(imageToCalculate, imageToCalculate, mask= whiteMask)
                frame = cv2.cvtColor(frame,cv2.COLOR_HSV2BGR) 
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                ret, frame = cv2.threshold(frame,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                nBlackPixel = cv2.countNonZero(frame) #this gives number of white pixels you have in the image
                numberAll = frame.size #this gives number of all pixels you have in the image

                nWhitePixels = numberAll - nBlackPixel
                nBlackPixelArrylst.append(nWhitePixels) #here after the mask been added region with green color has become the color of white
                nAllPixelArrylst.append(numberAll)

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
