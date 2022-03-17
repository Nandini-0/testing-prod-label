from flask import Flask,render_template,request
from fastai.vision import *
import numpy as np 
import pandas as pd
#from fastai.vision.widgets import *
import urllib.request
import os
from PIL import Image
from fastai import *
#from fastai.vision.data import ImageDataLoaders
from helper import extract_label
import pickle
#import pathlib
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath


#import pathlib
#plt = platform.system()
#pathlib.WindowsPath = pathlib.PosixPath


#--------------------------------------------Category----------------------------------------------
All_dictionary = [
    {'Apparel':[{'Topwear':['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover']},
            {'Bottomwear':  ['Jeans','Pant','Shorts','Skirt','Trouser']},
            {'Outerwear': ['Coat','Sweater','Hoodie','Cardigan','Blazer','Knit']}]},
            
    {'Footwear':[{'Casual':['Sandal','Flipflop','Boots','Heels','Flats']},
            {'Formal': ['Shoes']},
            {'Sports':['Sneaker']}]},
            
    {'Accessories': [{'Bags' : ['Bagpack','Handbag','Dufflebag','Slingbag']},
                {'Wristwear' : ['Watch','Cufflink','Gloves','Wristband']},
                {'Eyewear' : ['Sunglass']},
                {'Jewellery' : ['Necklace','Ring','Bracelet','Pendent','Earring']},
                {'hats' : ['Cap','Hat','Beanie cap']},
                {'Others' : ['Scarf','Socks','Wallet','Belt','Ties']}]},

    {'Furniture': [{'Storage' : ['Wardrobe','Trolley','Drawer','Cabinet']},
                {'Display' : ['Table','Hanger']},
                {'Others' : ['Chair','Stool','Sofa']}]}
                ]

#------------------------------------All product label--------------------------------------------



All_categories = ['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover','Jeans','Pant','Shorts','Skirt','Trouser',
                    'Coat','Sweater','Hoodie','Cardigan','Blazer','Knit','Sandal','Flipflop','Boots','Heels','Flats','Shoes',
                    'Sneaker','Bagpack','Handbag','Dufflebag','Slingbag','Watch','Cufflink','Gloves','Wristband','Sunglass',
                    'Necklace','Ring','Bracelet','Pendent','Earring','Cap','Hat','Beanie cap','Scarf','Socks','Wallet','Belt',
                    'Ties','Wardrobe','Trolley','Drawer','Cabinet','Table','Hanger','Chair','Stool','Sofa']





app = Flask(__name__)

def get_category_detail(label):
    if label == 'Innerwear':
        sub_cat = 'Innerwear'
        cat = 'Apparel'
    else:
        for i in All_dictionary:
            for j in i.values():
                for k in j:
                    for l in k.values():
                        if label in l:
                            sub_cat = np.array(list(k.keys()))
                            cat = np.array(list(i.keys()))
                            sub_cat = ''.join(map(str,sub_cat))
                            cat = ''.join(map(str,cat))
    return (sub_cat,cat)
    

def get_model():
    global model
    #with open('export.pkl','rb') as f:model = pkl.load(f)f.close()
    #model = pickle.load(open('export.pkl'), 'rb')
    model = load_learner(fname ='export.pkl')
    print("Model loaded!")
   
def prediction(img_path):
    label = extract_label(img_path)
    if label is not None:
        pred = model.predict(img_path)
        predt = str(pred[0])
        predt = predt.capitalize()
        return(predt)
    return label

get_model()

@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join('static//', filename)
        file.save(file_path)
        extracted_label = extract_label(file_path)
        if extracted_label is not None:
            product = extracted_label
        else:
            product = prediction(file_path)
        sub_cat,cat = get_category_detail(product)
    return render_template('predict.html', product = product, sub_cat = sub_cat,cat = cat,user_image = file_path)  


if __name__ == "__main__":
    app.run()
