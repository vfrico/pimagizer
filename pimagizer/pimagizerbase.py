#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: pimagizerbase.py
#   Abstract class for pimagizer
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


import sys
import os
from PIL import Image
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class PimagizerBase:
    # Array of path of valid images
    images = []

    # Matrix containing the size values for images
    sizes = []
    new_sizes = []

    # If working with a bundle of images
    #   0: It is not a bundle: using sizes only
    #   1: It is a bundle of images with the same sizes (and ratio)
    #   2: It is a bundle of images with the same aspect ratio
    #   3: It is a heterogeneous bundle (Image sizes are of all kinds)
    type_bundle = 0

    def __init__(self, imput_images):
        # Parse imput to get images
        for img in imput_images:
            curr_img = os.path.abspath(img)
            try:
                # Only the image is attached to array
                # if it is a valid image file
                i = Image.open(curr_img)
                self.images.append(curr_img)
                self.sizes.append(list(i.size))
                logging.debug("The file %s is a valid image" % curr_img)
            except IOError:
                logging.warning("The file %s isn't a valid image.\
                Skipping." % curr_img)

        # Evaluating type of bundle of images
        same_ratio = self.__have_same_ratio(self.sizes)
        same_size = self.__have_same_sizes(self.sizes)

        if not same_size and not same_ratio:
            self.type_bundle = 3
        elif not same_size and same_ratio:
            self.type_bundle = 2
        else:
            if len(self.images) == 1:
                self.type_bundle = 0
            else:
                self.type_bundle = 1

        logging.debug("List of loaded images " + str(self.images) +
                      ". Type of bundle: " + str(self.type_bundle) +
                      "\n Sizes: " + str(self.sizes))

    def __have_same_ratio(self, imputs):
        """
        Helper funtion to calculate if the sizes of
        all images have the same aspect ratio
        """
        all_same_ratio = True

        # Defining function to get aspect ratio
        ratio = lambda x: float(imputs[x][0])/float(imputs[x][1])

        # Ratio of the first images
        current_ratio = ratio(0)
        logging.debug("RATIO image #0: %s" % current_ratio)

        # While variable helper
        iterator = 1
        while iterator < len(self.images) and all_same_ratio:
            if current_ratio == ratio(iterator):
                all_same_ratio = all_same_ratio and True
            else:
                all_same_ratio = all_same_ratio and False

            # Updates for next iteration
            current_ratio = ratio(iterator)
            logging.debug("RATIO image #%d: %s" %
                          (iterator, current_ratio))
            iterator += 1

        return all_same_ratio

    def __have_same_sizes(self, imputs):
        """
        Helper funtion to calculate if the sizes of
        all images have the same sizes
        """
        all_same_sizes = True

        # Size of the first image
        current_size = imputs[0]
        logging.debug("SIZE image #0: %s" % str(current_size))

        # While variable helper
        iterator = 1
        while iterator < len(self.images) and all_same_sizes:
            if current_size == imputs[iterator]:
                all_same_sizes = all_same_sizes and True
            else:
                all_same_sizes = all_same_sizes and False
            # Updates for next iteration
            current_size = imputs[iterator]
            logging.debug("SIZE  image #%d: %s" %
                          (iterator, str(current_size)))
            iterator += 1

        return all_same_sizes

    def resize_using_size(self, width, heigth):
        """
        This function
        """


# Ejecución del programa
if __name__ == '__main__':
    # Argumentos de entrada (sin el nombre del programa)
    arg = sys.argv[1:]
    arg = ["a.png", "b.png"]
    # Inicializamos la clase
    p = PimagizerBase(arg)
