"""
Routes and views for the flask application.
"""

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

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )
    
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Report_02')
def Report_02():
    """Renders the about page."""
    return render_template(
        'Report_02.html',
        title='Report_02',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/Report_03')
def Report_03():
    """Renders the about page."""
    return render_template(
        'Report03.html',
        title='Report_03',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/ajax', methods =  ['GET', 'POST'])
def ajax() :
    clssToCall = ClsCompromise()
    return clssToCall.AjaxCompromise()

@app.route('/JsegAPI', methods =  ['GET', 'POST'])
def JsegAPI() :
    clssToCall = ClsCompromise()
    return clssToCall.JsegAPI()

@app.route('/uploader' , methods = ['GET', 'POST'])
def Compromise():
     if request.method == 'POST':
        clssToCall = ClsCompromise()
        return clssToCall.Comp03()

if __name__ == '__main__':
    app.run(port=50000, debug=True)