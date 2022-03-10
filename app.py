from flask import Flask,render_template,request
from fastai.vision.all import *
import numpy as np 
import pandas as pd
from fastai.vision.widgets import *
import urllib.request
import os
from PIL import Image
from fastai import *
from fastai.vision.data import ImageDataLoaders
import pickle
#import pathlib
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath


import pathlib
plt = platform.system()
pathlib.WindowsPath = pathlib.PosixPath


#--------------------------------------------Category----------------------------------------------
All_dictionary = [
    {'Apparel':[{'Topwear':['Tshirt','Shirt','Dress','Jackets','Tops','Undershirt','Pullover']},
            {'Bottomwear':  ['Jeans','Pants','Shorts','Skirts','Trousers']},
            {'Outerwear': ['Coats','Sweater','Hoodie','Cardigan','Blazer','Knits']}]},
            
    {'Footwear':[{'Casual':['Sandals','Flipflop','Boots','Heels','Flats']},
            {'Formal': ['Shoes']},
            {'Sports':['Seakers']}]},
            
    {'Accessories': [{'Bags' : ['Bagpack','Handbag','Dufflebag','Slingbag']},
                {'Wristwear' : ['Watch','Cufflinks','Gloves','Wristband']},
                {'Eyewear' : ['Sunglasses']},
                {'Jewellery' : ['Necklace','Ring','Bracelet','Pendent','Earrings']},
                {'hats' : ['Caps','Hats','Beanie cap']},
                {'Others' : ['Scarf','Socks','Wallets','Belts','Ties']}]},

    {'Furniture': [{'Storage' : ['wardrobe','Trolleys','Drawer','Cabinet']},
                {'Display' : ['Table','Hanger']},
                {'Others' : ['Chair','Stool','Sofa']}]}
                ]

#------------------------------------All product label--------------------------------------------



All_categories = ['Tshirt','Shirt','Dress','Jackets','Tops','Undershirt','Pullover','Jeans','Pants','Shorts','Skirts','Trousers',
                    'Coats','Sweater','Hoodie','Cardigan','Blazer','Knits','Sandals','Flipflop','Boots','Heels','Flats','Shoes',
                    'Seakers','Bagpack','Handbag','Dufflebag','Slingbag','Watch','Cufflinks','Gloves','Wristband','Sunglasses',
                    'Necklace','Ring','Bracelet','Pendent','Earrings','Caps','Hats','Beanie cap','Scarf','Socks','Wallets','Belts',
                    'Ties','wardrobe','Trolleys','Drawer','Cabinet','Table','Hanger','Chair','Stool','Sofa']





app = Flask(__name__)

def get_category_detail(label):
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

'''
def load_image(img_path):

    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)        
    img_tensor = np.expand_dims(img_tensor, axis=0) 
    img_tensor /= 255.
    return img_tensor

'''    

def prediction(img_path):
    #new_image = load_image(img_path)
    pred = model.predict(img_path)
    pred[0] = pred[0].capitalize()
    return(pred[0])

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
        product = prediction(file_path)
        sub_cat,cat = get_category_detail(product)
    return render_template('predict.html', product = product, sub_cat = sub_cat,cat = cat,user_image = file_path)  


if __name__ == "__main__":
    app.run()
