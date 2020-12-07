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
from pimagizer import info
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, GObject

_ = utils.config_translations()


def get_resources_folder():
    return utils.get_base_src()


class GtkAbout:
    def __init__(self):
        self.logo_filename = get_resources_folder() + "/pimagizer.svg"
        self.glade_file = get_resources_folder() + "ui/about.glade"

        self.builder = None
        self.aboutwindow = None

    def create(self):
        if self.builder is None or self.aboutwindow is None:
            logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.logo_filename)

            # Gets the GTK Builder
            self.builder = Gtk.Builder()
            self.builder.add_from_file(self.glade_file)

            signals = {
                "close_about": self.close,
            }

            self.builder.connect_signals(signals)

            self.aboutwindow = self.builder.get_object("aboutdialog")
            self.aboutwindow.set_version(info.version)
            self.aboutwindow.set_logo(logo_pixbuf)
            self.aboutwindow.set_comments(_(self.aboutwindow.get_comments()))

    def open(self):
        print(_("About"))
        self.create()
        self.aboutwindow.run()

    def close(self, widget, *args):
        print(_("Close about dialog"))
        self.aboutwindow.hide()
