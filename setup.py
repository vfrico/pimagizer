#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#       File: setup.py
#       This script allows install with: "sudo python ./setup.py install"
#
#       This file is part of Pimagizer
#       Pimagizer Copyright 2012-2016 Víctor Fernández Rico <vfrico@gmail.com>
#
#       Pimagizer is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       Pimagizer is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import shutil
# from distutils.core import setup
from setuptools import setup
from pimagizer import info
setup(
    name="pimagizer",
    version=info.version,
    license='gpl3',
    author='Víctor Fernández Rico',
    author_email='vfrico@gmail.com',
    description='Python Image resizer',
    long_description=("Pimagizer is a program used for resize images at "
                      "the easiest way with a simple interface written "
                      "with Python and GTK+3."),
    scripts=["bin/pimagizer"],
    url="http://www.cambiadeso.es/proyectos/pimagizer/",
    data_files=[("/usr/share/pimagizer/", ["src/pimagizer.glade",
                                           "src/pimagizer.svg",
                                           "src/bundle-background.png",
                                           "src/pimagizer-main.png",
                                           "src/neucha.ttf",
                                           "src/images_zh_CN.png",
                                           "src/images_zh_TW.png"]),
                ("/usr/share/applications/", ["src/pimagizer.desktop"]),
                ("/usr/share/icons/hicolor/scalable/apps/",
                    ["src/pimagizer.svg"]),
                ("/usr/share/pimagizer/i18n/es/LC_MESSAGES/",
                    ["src/i18n/es/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/fr/LC_MESSAGES/",
                    ["src/i18n/fr/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/ru/LC_MESSAGES/",
                    ["src/i18n/ru/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/ja/LC_MESSAGES/",
                    ["src/i18n/ja/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/jv/LC_MESSAGES/",
                    ["src/i18n/jv/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/id/LC_MESSAGES/",
                    ["src/i18n/id/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/ca/LC_MESSAGES/",
                    ["src/i18n/ca/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/id/LC_MESSAGES/",
                    ["src/i18n/id/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/zh_TW/LC_MESSAGES/",
                    ["src/i18n/zh_TW/pimagizer.mo"]),
                ("/usr/share/pimagizer/i18n/zh_CN/LC_MESSAGES/",
                    ["src/i18n/zh_CN/pimagizer.mo"]),
                ("/usr/bin/", ["bin/pimagizer"])],
    packages=["pimagizer"]
    )
try:
    os.chmod("/usr/bin/pimagizer",  stat.S_IXUSR)
    print("Yes")
except:
    print("Not installed (still) in /usr/bin/")
