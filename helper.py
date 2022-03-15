import easyocr
from easyocr import Reader
#reader = easyocr.Reader(['en'])
#result = reader.readtext('02.png', detail = 0)
#lst = '\n'.join(''.join(i) for i in result)
#print("scanned text:",lst)

All_categories = ['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover','Jeans','Pant','Shorts','Skirt','Trouser',
                    'Coat','Sweater','Hoodie','Cardigan','Blazer','Knit','Sandal','Flipflop','Boots','Heels','Flats','Shoes',
                    'Sneaker','Bagpack','Handbag','Dufflebag','Slingbag','Watch','Cufflink','Gloves','Wristband','Sunglass',
                    'Necklace','Ring','Bracelet','Pendent','Earring','Cap','Hat','Beanie cap','Scarf','Socks','Wallet','Belt',
                    'Ties','Wardrobe','Trolley','Drawer','Cabinet','Table','Hanger','Chair','Stool','Sofa']




def extract_label(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    lst = '\n'.join(''.join(i) for i in result)
    for i in All_categories:
        if i in lst:
            #print("label Found : ", i)
            return i


image = '02.png'
extract_label(image)
