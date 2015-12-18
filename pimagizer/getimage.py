#!/usr/bin/python
#-*- coding: UTF-8 -*-
#
#   File: getimage.py
#   Gets an image when handling a bundle of them
#       
#   This file is part of Pimagizer
#   Pimagizer (C) 2012-2014 Víctor Fernández Rico <vfrico@gmail.com>
#
#   Pimagizer is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
#
#   Pimagizer is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>


from PIL import Image
import os,math,re
import gettext
fontpath = "/usr/share/pimagizer/neucha.ttf"
#fontpath = "/usr/share/pimagizer/AutourOne-Regular.ttf"
#fontpath = "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf"
#fontpath = "/usr/share/fonts/truetype/horai-umefont/ume-pmo3.ttf"
#fontpath = "/home/victor/.fonts/salida/ofl/neucha/Neucha.ttf"

# For translations:
APP="pimagizer"
DIR="/usr/share/pimagizer/i18n/"
# Esto permite traducir los textos escritos en el .py (no en glade)
gettext.textdomain(APP)
gettext.bindtextdomain(APP, DIR)
# Y con esto podemos marcar las cadenas a traducir de la forma _("cadena")
_ = gettext.gettext
# End translations

def savefromPIL(PILImage,name):
    rutaaguardar = os.path.expanduser("~")+"/.config/pimagizer/"+name
    PILImage.save(rutaaguardar)
    return rutaaguardar
    
def getimage_num(numero):
    """Returns the URL to an image created with a font"""
    texto = _("Images") #Plural of images
    texto = texto.decode("utf8")
    # Support for non cyrilic or latin characters
    lang = None,None
    for n in re.findall(ur'[\u4e00-\u9fff]+',texto):
        lang = ("zh_CN","/usr/share/pimagizer/images_zh_CN.png")
        lang = ("zh_TW","/usr/share/pimagizer/images_zh_TW.png")
    try:
        import ImageFont, ImageDraw
    except:
        from PIL import ImageFont, ImageDraw
    #Cargo la fuente
    fuente = ImageFont.truetype(fontpath, 60)
    
    #Creo la imagen
    imagen = Image.open("/usr/share/pimagizer/bundle-background.png")
    (width,height) = imagen.size
    
    #Inicio la imagen para poder pintar
    draw = ImageDraw.Draw(imagen)
    
    if lang[0] == "zh_CN" or lang[0] == "zh_TW":
        # Open chinese text
        ch_text = Image.open(lang[1])

        coord_x = width / 2 - ch_text.size[0] / 2
        # Paste chinese text
        imagen.paste(ch_text,(coord_x,340),mask=ch_text)
    else:
        # Get appropiate x cordinate for center the word
        ### Aprox size of word in pixels
        size_texto = len(texto)*29
        ### Value of x coordinate
        coord_x = width / 2 - size_texto / 2
        #~ print "Coordenada X",coord_x
        
        # Draw on image
        draw.text((coord_x, 340), texto, font=fuente, fill="black")
    
    # Change font and draw again
    fuente = ImageFont.truetype(fontpath, 250)
    draw.text((190, 90), str(numero), font=fuente, fill="black") #orange was: #E56200
    
    return savefromPIL(imagen,"bundle.png")

def getimage_2(bundle):
    """
    Returns a PIL image object for a bundle of 
    images. Shape: Mosaic
    """
    # Number of images
    qty = len(bundle)
    raiz = math.sqrt(qty)
    part_ent = int(raiz)
    part_dec = float(raiz - part_ent)
    # Rows (filas) are given by the number of its square root
    if part_dec == 0:
        # If sqrt is exact -> nothing to do: same cols as rows
        #~ print "caso 1"
        filas = part_ent
        columnas = filas
    elif part_dec > 0.5 :
        # If sqrt is greater than 0.5 -> You need to add 1 to rows and cols
        #~ print "caso 2"
        columnas = part_ent + 1
        filas = columnas
    else:
        #~ print "caso 3"
        # If sqrt is less than 0.5 -> Only needed to add 1 to rows (the col won't get filled)
        columnas = part_ent
        filas = columnas + 1
    a = filas
    filas = columnas
    columnas = a
    print "Hay",filas,"filas y",columnas,"columnas" # for debugging
    
    # Get the ratio, to get the width of the final image, based on any image of array.
    #    [In first position (0), always are an image
    example = Image.open(os.path.abspath(bundle[0]))
    w,h = example.size
    ratio = float(float(w) / float(h))
    # Tamaño máximo del alto final
    #max_hgt = 500
    from pimagizer import config
    max_hgt = config.get_value("height")
    # Tamaño máximo del ancho final
    max_wdt = float(max_hgt) * float(ratio)
    #~ print ratio,max_hgt,max_wdt
    
    # Get the size of each miniature in the final mosaic
    min_hgt = int(max_hgt / columnas) 
    min_wdt = int(min_hgt * ratio) # W = h * k
    #~ print min_hgt, min_wdt
        
    # Final size of image: Is important to no pass float to PIL
    fin_wdt = int(max_wdt)
    if part_dec <= 0.5 and not part_dec == 0:
        fin_hgt = int(max_hgt) - min_hgt
    else:
        fin_hgt = int(max_hgt)
    
    # To create the final mosaic, you need to say the left 
    # top position on each image.
    # List with position from left side to the image
    x_axis_list = []
    startx = 0
    for x in range(columnas):
        # It simply works. Don't touch !!
        x_axis_list.append(startx)
        startx = startx + min_wdt
    #~ print "x",x_axis_list
    # List with position from top to the desired image
    y_axis_list = []
    starty = 0 
    for y in range(filas):
        # It simply works. Don't touch !!
        y_axis_list.append(starty)
        starty = starty + min_hgt
    #~ print "y",y_axis_list
    
    # Mosaic image (final image)
    mosaico = Image.new("RGBA", (fin_wdt,fin_hgt))
    
    # We insert images to mosaic
    # Indice allows to know the next image to insert
    indice = -1
    #~ print "for"
    for img_row in y_axis_list:
        #~ print "algo"
        for img_col in x_axis_list: 
            #~ print "algo2"
            # Avance one position on array
            indice = indice + 1
            #~ print "before try"
            try:
                img = bundle[indice]
            except:
                #~ print "in except"
                # Will arrive one moment in what the array won't have 
                #   [more images (not all the rows are always filled)
                break
            #~ print "after try"
            #~ print img,img_col,img_row
            #~ print "     _",min_wdt,min_hgt
            
            # Open the image to handle it
            imagen = Image.open(img)
            
            # Resize the image to get fit in its place
            #~ print "imageantialias"
            imagenresized = imagen.resize((min_wdt,min_hgt), Image.ANTIALIAS)
            
            # Paste the image in right place
            #~ print "paste"
            mosaico.paste(imagenresized,(img_col,img_row))
            
            #~ print "algo2_imgattached"
    # Returns a PIL image object, no a URL
    #~ print "finish"
    return mosaico

def get_correct_preview(lista):
    """
    Imput: A list; Outputs: a filename with image;
    Chooses the best element in each case
    """
    if is_bundle_equal(lista):
        # Returns a mosaic
        return savefromPIL(getimage_2(lista), "mosaicBundle.png")
    else:
        # Returns an image with number
        numero = len(lista)
        imagePIL = getimage_num(numero)
        #~ filename = savefromPIL(imagePIL, "numeredBundle.png")
        return imagePIL
    
def is_bundle_equal(bundle):
    bundle_width = []
    bundle_height = []
    bundle_ratio = []
    for image in bundle:
        # Gets height, width and ratio of all images
        imagen = Image.open(image)
        (width, height) = imagen.size
        bundle_width.append(width)
        bundle_height.append(height)
        bundle_ratio.append(width/height)
    
    def is_all_same(lista):
        """
        used to check if the values on a list are all the same
        """
        for elem in lista:
            all_elem_same = True
            for elem1 in lista:
                #print "elementos",elem,elem1
                if elem != elem1:
                    #~ print False
                    all_elem_same = False
                    break
        return all_elem_same
    
    if is_all_same(bundle_width) and is_all_same(bundle_height):
        return True
    else:
        return False
