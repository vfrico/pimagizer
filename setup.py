#!/usr/bin/env python3
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
from setuptools import setup
from setuptools.command.install import install
from pimagizer import info
from babel.messages import frontend as babel

class InstallWithCompile(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()

lang_install_path = "/usr/share/pimagizer/i18n/{}/LC_MESSAGES/"
lang_resource_path = "src/i18n/{}/LC_MESSAGES/pimagizer.mo"
langs = ["ar", "ca", "es", "fr", "id", "ja", "jv", "ru", "zh_TW", "zh_CN"]
localization_tuples = [(lang_install_path.format(lang),
                        [lang_resource_path.format(lang)]) for lang in langs]

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
                ("/usr/share/applications/",
                                            ["src/pimagizer.desktop"]),
                ("/usr/share/icons/hicolor/scalable/apps/",
                                            ["src/pimagizer.svg"]),
                *localization_tuples,
                ("/usr/bin/", ["pimagizer.py"])],
    package_data={'': ['src/i18n/*/*/*.mo', 'src/i18n/*/*/*.po']},                
    packages=["pimagizer"],
    setup_requires=[
        'babel'
        #, 'BabelGladeExtractor',
    ],
    cmdclass = {
        'install': InstallWithCompile,        
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    }               
    )
try:
    os.chmod("/usr/bin/pimagizer",  shutil.stat.S_IXUSR)
    print("Yes")
except:
    print("Not installed (still) in /usr/bin/")
