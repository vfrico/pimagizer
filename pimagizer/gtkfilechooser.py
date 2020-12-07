#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: gtkpimagizer.py
#   Gui of pimagizer
#
#   This file is part of Pimagizer
#   Pimagizer (C) 2020 Víctor Fernández Rico <vfrico@gmail.com>
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
from pimagizer import utils
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, GObject

_ = utils.config_translations()


def get_resources_folder():
    return utils.get_base_src()


def gtk_hide(widget, data):
    print("Hide window")
    widget.hide()
    return True


class GtkFileChooser:
    def __init__(self, file_selected_cb=None):

        # Gets the GTK Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file(get_resources_folder() + "ui/filech.glade")

        # File chooser
        self.filech = self.builder.get_object("filechooserdialog1")
        self.filech.connect('delete-event', gtk_hide)
        self.filech.set_title(_(self.filech.get_title()))

        # Add filter for images
        filter_img = Gtk.FileFilter()
        filter_img.set_name(_("Image files"))
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        self.filech.add_filter(filter_img)

        signals = {
            "filech-accept": self.setfilename,
            "filech-cancel": self.closefilename
        }

        self.builder.connect_signals(signals)

        # Callbacks
        self.file_choosed_cb = file_selected_cb

    def get_widget(self):
        return self.filech

    def changefile(self, widget, *args):
        """Run dialog"""
        print("Changefile")
        self.filech.set_title(_(self.filech.get_title()))
        self.filech.show()
        self.filech.run()

    def setfilename(self, widget):
        "After selecting a file on Filechooserbutton"
        self.filech.hide()
        # self.filename = self.filech.get_filenames()
        # self.listbundle = self.filename
        # How many images are selected? Do different things in each case
        #TODO self.updateUI(self.filename)
        self.file_choosed_cb(self.filech.get_filenames())


    def closefilename(self, widget):
        self.filech.hide()

    def show(self):
        """Run dialog"""
        print("Changefile")
        self.filech.show()
        self.filech.run()