#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: pimagizerr_single.py
#   Class to manage single images
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
import os


class PimagizerSingle:

    def __init__(self):
        self.image = None
        self.img_format = ""
        self.origin_path = ""

    def get_image(self):
        return self.image

    def get_image_size(self):
        return self.image.size

    def get_image_ratio(self):
        sizes = self.get_image_size()
        return sizes[1] / sizes[0]

    def get_image_format(self):
        return self.img_format

    def set_image(self, imageURL):
        try:
            self.image = Image.open(imageURL)
            self.img_format = self.image.format
            self.origin_path = os.path.abspath(imageURL)
            return True
        except IOError:
            raise IOError("Image '%s' not found" % imageURL)
            return False

    def set_format(self, new_format):
        """
        Changes Image format. Avalible formats:
            PNG,JPEG,GIF,TIFF,PPM,ICO
        """
        formats = "GIF", "TIFF", "JPEG", "PNG", "PPM", "ICO"
        if new_format.upper() in formats:
            self.img_format = new_format
            return True
        else:
            error = "The format %s is not allowed" % new_format.upper()
            raise TypeError(error)
            return False

    def save(self):
        """
        Overwrites the image
        """
        self.save_image(self.origin_path)
        return True

    def save_image(self, path):
        """
        Saves the image on path
        """
        try:
            self.image.save(path, self.img_format)
            return True
        except IOError:
            raise IOError("Unable to save on %s" % path)
            return False

    def resize_width_height(self, width, height):
        """
        Resizes instantaneally the image using PIL
        """
        width = int(width)
        height = int(height)
        self.image = self.image.resize((width, height), Image.ANTIALIAS)
        return True

    def resize_proportional_width(self, width):
        """
        When entering only width, the height will be calculated automatically.
        Will preserve the original ratio.
        """
        sizes = self.get_image_size()
        ratio = sizes[1] / sizes[0]
        height = width * ratio
        self.resize_width_height(width, height)
        return True

    def resize_proportional_height(self, height):
        """
        When entering only height, the width will be calculated automatically.
        Will preserve the original ratio.
        """
        sizes = self.get_image_size()
        ratio = sizes[0] / sizes[1]
        width = height * ratio
        self.resize_width_height(width, height)
        return True

    def resize_by_percent(self, percent):
        """
        Applies automatically a percent to images.
        percent arg should be between 0 and 1. Other values won't be ignored
        but may result on undesired behaviour
        """
        sizes = self.get_image_size()
        width = sizes[0]*percent
        height = sizes[1]*percent
        self.resize_width_height(width, height)
        return True
