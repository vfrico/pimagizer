#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: pimagizerr_bundle.py
#   Class to manage image bundles
#
#   This file is part of Pimagizer
#   Pimagizer (C) 2012-2015 Víctor Fernández Rico <vfrico@gmail.com>
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
from pimagizer_single import PimagizerSingle

class PimagizerBundle:

    def __init__(self):
        self.images = []
        self.has_same_ratio = False
        self.has_same_sizes = False


    def get_image(self,index):
        try:
            return self.images[index]
        except IndexError:
            print ("Error. Index not exists")


    def get_images(self):
        return self.images


    def get_type(self):
        if self.has_same_ratio and self.has_same_sizes:
            return 1 #same ratio,same sizes
        elif self.has_same_ratio and not self.has_same_sizes:
            return 2 #Same ratio, distinct sizes
        else:
            return 3 #Heterogeneus


    def show_images(self):
        img_array = []
        for image in self.images:
            img_array.append(image.origin_path)
        return img_array


    def put_image(self,imageURL):
        new_image = PimagizerSingle()
        new_image.set_image(imageURL)
        self.images.append(new_image)

        self.check_ratio()
        self.check_sizes()
        return True


    def put_images(self,iterableImageURL):
        for imageURL in iterableImageURL:
            self.put_image(imageURL)


    def check_ratio(self):
        ratios = []
        for image in self.images:
            ratios.append(image.get_image_ratio())

        if len(set(ratios)) <= 1:
            self.has_same_ratio = True
        else:
            self.has_same_ratio = False


    def check_sizes(self):
        sizes = []
        for image in self.images:
            sizes.append(image.get_image_size())

        if len(set(sizes)) <= 1:
            self.has_same_sizes = True
        else:
            self.has_same_sizes = False



    def resize_width_height(self,width,height,force_prop=False):
        if not self.has_same_ratio and force_prop:
            print("Images haven't the same ratio,\
             so resize won't be proportional")
            return False

        if not self.has_same_sizes:
            print ("Trying to resize images wich haven't the same size.\
                The result might not be the expected")

        for image in self.images:
            image.resize_width_height(width,height)

        return True

    def resize_proportional_width(self,width):
        for image in self.images:
            image.resize_proportional_width(width)

        return True

    def resize_proportional_height(self,height):
        for image in self.images:
            image.resize_proportional_height(height)

        return True

    def resize_by_percent(self,percent):
        for image in self.images:
            image.resize_by_percent(percent)
        return True

    def save_overwrite(self):
        """
        Save recursivelly all the images
        """
        for image in self.images:
            image.save_image(image.origin_path)

        return True

    def save_new_path(self,path):
        """
        Save all images on a single folder.
        path must be valid and a folder not file
        """
        path = os.path.dirname(path)
        for image in self.images:
            name = os.path.basename(image.origin_path)
            destination = os.path.join(path,name)
            image.save_image(destination)

        return True







#



            #
