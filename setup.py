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
    def copy_po_files(self):
        langs = ["ar", "ca", "es", "fr", "id", "ja", "jv", "ru", "zh_TW", "zh_CN"]
        source_path = "i18n/"
        dest_path = "pimagizer/i18n/{}/LC_MESSAGES/pimagizer.po"

        for lang in langs:
            orig_po = source_path + f"{lang}.po"
            dest_po = dest_path.format(lang)
            os.makedirs(os.path.split(dest_po)[0], exist_ok=True)
            print(f"Copia {orig_po} a {dest_po}")
            shutil.copy(orig_po, dest_po)

    def run(self):
        print("RUN INSTALL")
        self.copy_po_files()
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        print(option_dict)
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()



lang_install_path = "/usr/share/pimagizer/i18n/{}/LC_MESSAGES/"
lang_resource_path = "src/i18n/{}/LC_MESSAGES/pimagizer.mo"
#
# localization_tuples = [(lang_install_path.format(lang),
#                         [lang_resource_path.format(lang)]) for lang in langs]

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
    url="http://www.cambiadeso.es/proyectos/pimagizer/",
    package_data={
        'pimagizer': [
            'src/*.*',
            'i18n/*/LC_MESSAGES/*.mo'
        ]
    },
    # package_dir={'': 'src/'},
    include_package_data=True,
    packages=["pimagizer"],
    setup_requires=[
        'babel'
        #, 'BabelGladeExtractor',
    ],
    cmdclass={
        'install': InstallWithCompile,
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    },
    entry_points={
        "console_scripts": [
            "pimagizer = pimagizer.main:main",
        ]
    }
    )
