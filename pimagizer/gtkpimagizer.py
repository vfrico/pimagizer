#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: gtkpimagizer.py
#   Gui of pimagizer
#
#   This file is part of Pimagizer
#   Pimagizer (C) 2012-2016 Víctor Fernández Rico <vfrico@gmail.com>
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
from pimagizer import info
from pimagizer import config
from pimagizer import utils
from pimagizer import getimage
from PIL import Image
import math
import os
import glob
import locale
import gettext
import time
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf, GObject

_ = utils.config_translations()


def get_resources_folder():
    return utils.get_base_src()

class Pimagizer:
    def __init__(self, imputfile):

        # Gets the GTK Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file(get_resources_folder() + "/pimagizer.glade")

        # Get the GTK object
        self.wdgtimg = self.builder.get_object("mainimage")

        # Sets the default file for image
        self.filename = get_resources_folder() + "/pimagizer-main.png"

        self.absheight = 0
        self.abswidth = 0

        # #********************************************
        # ###### GET EACH OBJECT ON BUILDER ###########
        # #********************************************

        # File chooser
        self.filech = self.builder.get_object("filechooserdialog1")

        # Add filter for images
        filter_img = Gtk.FileFilter()
        filter_img.set_name(_("Image files"))
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        self.filech.add_filter(filter_img)

        # Init Width box
        self.inputwidth = self.builder.get_object("width")
        self.inputwidth.set_value(self.abswidth)
        self.txtwidth = ""

        # Init Height box
        self.inputheight = self.builder.get_object("height")
        self.inputheight.set_value(self.absheight)
        self.txtheight = ""

        # Get and translate "proportional"
        self.checkprop = self.builder.get_object("checkprop")
        self.checkprop.set_label(_(self.checkprop.get_label()))

        # Setup labelresol (global and percentage)
        self.lblresol = self.builder.get_object("lblresol")
        self.lblresol1 = self.builder.get_object("lblresol1")
        # self.lblresol.set_text(str(width)+"x"+str(height))
        # self.lblresol1.set_text(str(width)+"x"+str(height))
        self.lblst = self.builder.get_object("labelst")

        # Save folder
        self.btflsave = self.builder.get_object("filechooserbutton1")
        self.btflsave.set_title(_(self.btflsave.get_title()))
        self.labelsave = self.builder.get_object("savefile")

        # Preferences Window
        self.wpref = self.builder.get_object("preferences")
        self.ntbkpref = self.builder.get_object("notebook1")

        # Formats box
        self.boxformats = self.builder.get_object("formatbox")

        # Expanders
        self.boxPx = self.builder.get_object("box6")
        self.boxPr = self.builder.get_object("box23")

        self.height1 = self.builder.get_object("height1")
        self.height1.set_value(100)

        #  "Size in pixels"
        # self.label2 = self.builder.get_object("label2")
        # self.label2.set_text(_(self.label2.get_text()))
        # "Percentage resizing"
        # self.label22 = self.builder.get_object("label22")
        # self.label22.set_text(_(self.label22.get_text()))
        # "Percentage (%)"
        self.label24 = self.builder.get_object("label24")
        self.label24.set_text(_(self.label24.get_text()))
        # "Percentage (%)"
        # self.label25 = self.builder.get_object("label25")
        # self.label25.set_text(_(self.label25.get_text()))
        # "Percentage (%)"
        self.label26 = self.builder.get_object("label26")
        self.label26.set_label(_(self.label26.get_label()))

        #  Translates
        # "Click on image to change"
        self.label6 = self.builder.get_object("label6")
        # if self.tipo == 1:
        #    self.label6.set_text(_("Click here to update preview"))
        # elif self.tipo == 2:
        #    self.label6.set_text(_("The images you selected
        #                            have different sizes"))
        # else:
        #    self.label6.set_text(_(self.label6.get_text()))
        # if self.hidelabel and not (self.tipo == 1 or self.tipo == 2):
        #    self.label6.hide() #Hides the label "Click on image to change"
        self.label3 = self.builder.get_object("label3")  # "Save:"
        self.label3.set_text(_(self.label3.get_text()))
        self.label1 = self.builder.get_object("label1")  # "Size:"
        self.label1.set_text(_(self.label1.get_text()))
        # self.label25 = self.builder.get_object("label25") # "Size:"
        # self.label25.set_text(_(self.label25.get_text()))
        # Is actived nw file or not?
        self.labelnwfl = self.builder.get_object("labelnwfl")
        self.f_labelnwfl()

        # On Preferences window
        # Right now, Pimagizer suports JPG and PNG formats
        self.label10 = self.builder.get_object("label10")
        self.label10.set_text(_(self.label10.get_text()))
        self.label8 = self.builder.get_object("label8")  # Works with
        self.label8.set_text(_(self.label8.get_text()))
        self.label7 = self.builder.get_object("label7")  # Launchpad
        self.label7.set_text(_(self.label7.get_text()))
        self.linkbutton1 = self.builder.get_object("linkbutton1")  # Translate
        self.linkbutton1.set_label(_(self.linkbutton1.get_label()))
        self.linkbutton2 = self.builder.get_object("linkbutton2")  # Bugs
        self.linkbutton2.set_label(_(self.linkbutton2.get_label()))
        self.linkbutton3 = self.builder.get_object("linkbutton3")  # Questions
        self.linkbutton3.set_label(_(self.linkbutton3.get_label()))
        self.label9 = self.builder.get_object("label9")  # Size of preview
        self.label9.set_text(_(self.label9.get_text()))
        # Here you can set the size of the image preview on main window
        self.label13 = self.builder.get_object("label13")
        self.label13.set_text(_(self.label13.get_text()))
        # Is recommended to set a value near to 300px
        self.label12 = self.builder.get_object("label12")
        self.label12.set_text(_(self.label12.get_text()))
        self.label11 = self.builder.get_object("label11")  # Height
        self.label11.set_text(_(self.label11.get_text()))
        self.label4 = self.builder.get_object("label4")  # Information
        self.label4.set_text(_(self.label4.get_text()))
        self.label5 = self.builder.get_object("label5")  # Interface
        self.label5.set_text(_(self.label5.get_text()))
        # preferences -> (tab) saving
        # Switch for new file name
        self.switch_newfilename = self.builder.get_object("switch1")
        self.label15 = self.builder.get_object("label15")  # label on tab
        self.label15.set_text(_(self.label15.get_text()))
        # title frame: <b>Saving options</b>
        self.label16 = self.builder.get_object("label16")
        self.label16.set_text(_(self.label16.get_text()))
        self.label16.set_use_markup(True)
        # Do you want to save the new file with a
        self.label17 = self.builder.get_object("label17")
        # new name as image(widthxheight).jpg?
        self.label17.set_text(_(self.label17.get_text()))
        # save images with new name
        self.label18 = self.builder.get_object("label18")
        self.label18.set_text(_(self.label18.get_text()))
        # If you <b>turn off</b> this option, you will
        # <b>overwrite</b> all you save with Pimagizer
        self.label19 = self.builder.get_object("label19")
        textohelp = _(("If you <b>turn off</b> this option, you will \n"
                       "<b>overwrite</b> all you save with Pimagizer"))
        self.label19.set_text(textohelp)
        self.label19.set_use_markup(True)

        self.label20 = self.builder.get_object("label20")  # Width
        self.label20.set_text(_(self.label20.get_text()))
        self.label23 = self.builder.get_object("label23")  # Height
        self.label23.set_text(_(self.label23.get_text()))

        # Preview size
        self.spinprew = self.builder.get_object("spinbutton1")
        self.spinprew.set_value(config.get_value("height"))

        signals = {
                "about_activate": self.showabout,
                "main_close": self.cerrarapp,
                "resize-accept": self.resizeimg,
                "File-update": self.updateimg,
                "main-update": self.updateimg,
                "img-click": self.updateimg,
                "height-cursor": self.heightcursor,
                "width-cursor": self.widthcursor,
                "filech-accept": self.setfilename,
                "filech-cancel": self.closefilename,
                "chfile": self.changefile,
                "activeprop": self.proporcionar,
                "show-preferences": self.showpreferences,
                "prefer-cancel": self.cancelpref,
                "prefer-acept": self.aceptpref,
                "nwfile-lbl": self.pref_saving,
                "expander_pix": self.expander_pix,
                "expander_times": self.expander_times,
                "times_changed": self.times_changed,
                "help_exp_times": self.sethelp_exp_times,
                "help_exp_times_": self.sethelp_exp_times_,
                "iniciado": self.on_init,
                "bundle-update": self.bundle_update,
                # "newnameact": self.newname
                }

        self.builder.connect_signals(signals)

        # Get main window
        self.window1 = self.builder.get_object("window1")

        # Test if system can generate HeaderBar
        # (only available on Gnome/GTK+ 3.10 +)
        try:
            hb = Gtk.HeaderBar()
            self.g310support = True
            self.buttonbox1 = self.builder.get_object("buttonbox1")
            self.buttonbox1.hide()
        except:
            self.g310support = False

        # ###########################################
        # ··············  HeaderBar  ················
        # *******************************************
        if self.g310support:

            # Add a HeaderBar
            self.hb = Gtk.HeaderBar()
            self.hb.props.show_close_button = True
            self.hb.props.title = "Pimagizer"
            self.window1.set_titlebar(self.hb)

            ############################################
            # *** Buttons About and Preferences

            buttonAb = Gtk.Button()
            iconAb = Gio.ThemedIcon(name="gtk-about")
            imageAb = Gtk.Image.new_from_gicon(iconAb, Gtk.IconSize.BUTTON)
            buttonAb.add(imageAb)
            buttonAb.show()
            imageAb.show()
            buttonAb.connect("clicked", self.showabout)

            buttonSt = Gtk.Button()
            iconSt = Gio.ThemedIcon(name="gtk-preferences")
            imageSt = Gtk.Image.new_from_gicon(iconSt, Gtk.IconSize.BUTTON)
            buttonSt.add(imageSt)
            buttonSt.show()
            imageSt.show()
            buttonSt.connect("clicked", self.showpreferences)

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            Gtk.StyleContext.add_class(box.get_style_context(), "linked")
            box.add(buttonAb)
            box.add(buttonSt)
            box.show()

            self.hb.pack_start(box)

            ###############################################
            # *** Buttons Pixels(px) and Percent(%)
            big_format = '<span size="xx-large"><b>{}</b></span>'

            self.buttonPx = Gtk.ToggleButton()
            labelPx = Gtk.Label(big_format.format("Px"))
            self.buttonPx.add(labelPx)
            self.buttonPx.show()
            labelPx.set_use_markup(True)
            labelPx.show()

            # It is connected below
            self.buttonPr = Gtk.ToggleButton()
            labelPr = Gtk.Label(big_format.format("%"))
            self.buttonPr.add(labelPr)
            self.buttonPr.show()
            labelPr.set_use_markup(True)
            labelPr.show()

            # pr => box23
            self.buttonPr.connect("toggled", self.toggledPr, self.buttonPx)
            # px => box6
            self.buttonPx.connect("toggled", self.toggledPx, self.buttonPr)

            if config.get_value("defaultpx") == 1:
                # Si es verdad, esconder el Pr
                self.boxPr.hide()
                self.buttonPx.set_active(True)
            else:
                # Si no es verdad, esconder el Px
                self.boxPx.hide()
                self.buttonPr.set_active(True)

            box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            Gtk.StyleContext.add_class(box2.get_style_context(), "linked")
            box2.add(self.buttonPx)
            box2.add(self.buttonPr)
            box2.show()

            self.hb.pack_end(box2)

        else:  # Else generate fake headerbar (for GTK =< 3.6)
            self.buttonPr36 = self.builder.get_object("togglepr36")
            self.buttonPx36 = self.builder.get_object("togglepx36")

            if config.get_value("defaultpx") == 1:
                # Si es verdad, esconder el Pr
                self.boxPr.hide()
                self.buttonPx36.set_active(True)
            else:
                # Si no es verdad, esconder el Px
                self.boxPx.hide()
                self.buttonPr36.set_active(True)

            self.buttonPr36.connect("toggled", self.toggledPr, self.buttonPx36)
            self.buttonPx36.connect("toggled", self.toggledPx, self.buttonPr36)

            # Linking boxes to get more beautiful experience
            self.box3 = self.builder.get_object("box3")
            Gtk.StyleContext.add_class(self.box3.get_style_context(), "linked")
            self.box4 = self.builder.get_object("box4")
            Gtk.StyleContext.add_class(self.box4.get_style_context(), "linked")
        ###
        # **************************************************
        # ··············END HeaderBar·······················
        ####################################################

        # Show Window and HeaderBar
        if self.g310support:
            self.hb.show()
        self.window1.show()

        if imputfile == []:
            imputfile = [self.filename]
        print("imputfile+ "+str(imputfile))
        self.updateUI(imputfile)

        if(self.window1):
            self.window1.connect("destroy", self.cerrarapp)

    def cerrarapp(self, widget):
        print(_("Saving preferences data"))
        if self.g310support:
            if self.buttonPx.get_active():
                config.set_value("defaultpx", 1)
            else:
                config.set_value("defaultpx", 0)

        print(_("Closing program"))
        Gtk.main_quit()

    def showabout(self, widget):
        print(_("About"))
        self.aboutwindow = self.builder.get_object("aboutdialog")
        self.aboutwindow.set_version(info.version)
        self.aboutwindow.set_comments(_(self.aboutwindow.get_comments()))
        self.aboutwindow.run()
        self.aboutwindow.hide()

    def closeabout(self, widget):
        print(_("Close about dialog"))
        self.aboutwindow.hide()

    def resizeimg(self, widget):
        """Saves the image"""
        if self.tipo != 0:
            print("Working with a set of images")
            # self.lblst.set_text("You have selected a set of images.\n
            #                      We are working to \n support that. Thanks!")
            # Gets the values of width and height
            width = int(float(self.inputwidth.get_value_as_int()))
            height = int(float(self.inputheight.get_value_as_int()))
            print(width, height)
            # Set of image files: self.listbundle
            for img in self.listbundle:
                img = os.path.abspath(img)
                print("Opening image ", img)
                # PIL open the image
                image = Image.open(img)
                if self.tipo == 2:
                    # If there are several images (not at same proportion) =>
                    # it is needed to calc each size
                    percent = self.height1.get_value_as_int()
                    percent = percent * 0.01
                    wth, hgt = image.size
                    width = int(wth*percent)
                    height = int(hgt*percent)
                elif self.tipo == 1:
                    width = int(float(self.inputwidth.get_value_as_int()))
                    height = int(float(self.inputheight.get_value_as_int()))
                # PIL resizes the image
                image = image.resize((width, height), Image.ANTIALIAS)

                # PIL creates the new file name
                imgname, ext = os.path.splitext(img)
                savename = imgname+"("+str(width)+"x"+str(height)+")"+ext
                # PIL saves the image
                image.save(savename)
                print("Saved image", savename)
                # save_txt =
                #     _("Bundle of %d images saved") % len(self.listbundle)
                save_txt = _("Saved %d images") % len(self.listbundle)
                self.lblst.set_text(save_txt)
                self.lblst.set_use_markup(True)

        else:
            print("Working with a single image")
            # Separamos el nombre de la imagen de su extensión
            # para reconocer el formato de la imagen
            imgfile, ext0 = os.path.splitext(self.filename)
            # If press save button when there's no text on entry
            if (self.labelsave.get_text() == ""):
                errorMSG = _("You have not selected any file")
                print(errorMSG)
                self.lblst.set_text(errorMSG)
                return 1

            # PIL open the selected image
            image = Image.open(self.filename)

            # Gets the desired width and height
            width = int(float(self.inputwidth.get_value_as_int()))
            height = int(float(self.inputheight.get_value_as_int()))

            # PIL applyes changes (resize) to image buffer
            image = image.resize((width, height), Image.ANTIALIAS)

            # Gets the desired name by the user (on entry)
            imgname = self.labelsave.get_text()

            # Extensions support (for the desired name of the user)
            nada, ext = os.path.splitext(imgname)
            # Si el usuario no ha escrito una extensión
            # se usa la del archivo de origen
            if ext == "":
                ext = ext0
            if(ext == ".jpg" or ext == ".JPG" or
               ext == ".jpeg" or ext == ".JPEG"):
                ext2 = "JPEG"
            elif(ext == ".png" or ext == ".PNG"):
                ext2 = "PNG"
            else:
                print("No format supported, trying JPEG")
                ext2 = "JPEG"

            # Getting the final name desired by user
            if self.folderset()[0]:  # Chosen folder
                final = self.folderset()[1]+"/"+imgname  # Final name of image
                print(final)
            else:  # If filechooser not changed
                # Nombre final de la dirección de guardado
                final = os.path.dirname(os.path.abspath(self.filename))
                final += "/"+imgname
            # PIL saves the image
            image.save(final, ext2)
            # Final saving
            print("Saved", final)
            # Puts some messages for user
            self.lblst.set_text(_("Image saved"))  # +imgname+
            # self.lblst.set_use_markup(True)

    def resizing(self, filename):
        filename = os.path.abspath(filename)
        """When called, returns a GTKPixBuf created from filename"""
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        pbuf_width = pixbuf.get_width()
        pbuf_height = pixbuf.get_height()
        ratio = int(pbuf_width) * math.pow(int(pbuf_height), -1)  # Division
        self.ratio = ratio
        height = config.get_value('height')
        width = height*ratio
        scaled_buf = pixbuf.scale_simple(width,
                                         height,
                                         GdkPixbuf.InterpType.BILINEAR)
        return scaled_buf

    def updateimg(self, widget):
        """Update preview in main window"""
        # Variable filename contains path
        filename = self.imgfile.get_filename()
        self.filename = filename
        self.wdgtimg.set_from_pixbuf(self.resizing(filename))
        if (self.isimgbox):
            self.wdgtimg.hide()
            self.isimgbox = False
            self.imgfile.show()
        else:
            self.imgfile.hide()
            self.wdgtimg.show()
            self.isimgbox = True

    def changefile(self, widget, *args):
        """Run dialog"""
        print("Changefile")
        self.filech.set_title(_(self.filech.get_title()))
        self.filech.show()
        self.filech.run()

    def update_sizeUI(self, wid, hei):
        "Updates the resolution on all items on UI and do them global"

        self.absheight = hei
        self.abswidth = wid
        # self.ratio = int(wid) * math.pow(int(hei),-1)
        try:
            self.ratio = float(wid) / float(hei)
        except:
            self.ratio = 1
        print(self.ratio)

        if self.g310support:
            if self.buttonPr.get_active():
                percent = self.height1.get_value_as_int() * 0.01
            else:
                percent = 1
        else:
            if self.buttonPr36.get_active():
                percent = self.height1.get_value_as_int() * 0.01
            else:
                percent = 1
        print(percent)

        (wid, hei) = (int(wid * percent), int(hei * percent))
        self.lblresol.set_text(str(wid)+"x"+str(hei))  # Sets text on top label
        self.inputheight.set_value(hei)  # set height on imput
        self.inputwidth.set_value(wid)  # set width on input
        self.setlabelsave()  # Changes the imput text for file to save

    def updateUI(self, files):
        """Makes all needed actions to get ui updated"""
        self.filename = files
        print(self.filename)
        if self.g310support:
            self.buttonPx.set_sensitive(True)
        else:
            self.buttonPx36.set_sensitive(True)

        self.builder.get_object("box11").show()

        if len(self.filename) == 1:
            print("One image is selected")
            self.tipo = 0
            # If only one image then catch the only image on list
            self.filename = self.filename[0]

            # Changes preview
            self.wdgtimg.set_from_pixbuf(self.resizing(self.filename))

            # Sets folder on Filechooserbutton
            self.btflsave.set_current_folder(os.path.dirname(self.filename))

            # Get width and height for selected image
            imagen = Image.open(self.filename)
            (width, height) = imagen.size  # Gets width and height
            self.update_sizeUI(width, height)

        elif len(self.filename) > 1:
            print("Several images selected")

            # Set preview of a bundle
            # preview_file = getimage.get_correct_preview(self.filename)
            preview_file = getimage.getimage_num(len(self.filename))
            self.wdgtimg.set_from_pixbuf(self.resizing(preview_file))

            # Get the folder
            carpeta = os.path.dirname(self.filename[0])
            self.btflsave.set_current_folder(carpeta)

            # If are all images the same
            # If is a bundle: 1) If all images are of same dimensions ->
            #   width , height ;; else) first ratio
            if getimage.is_bundle_equal(self.filename):
                """If images has the same dimensions ->
                Width and Height are same for all"""
                self.tipo = 1

                # Open any image on list and get values
                imagen = Image.open(self.filename[0])
                (width, height) = imagen.size
                self.update_sizeUI(width, height)
                self.listbundle = self.filename
            else:
                """If Images are irregular"""
                self.tipo = 2
                # Set 0 as default value
                height = 0
                width = 0

                self.update_sizeUI(width, height)

                # Hide expand 2 -> Is not possible to modify size in pixels
                # exp_pix = self.builder.get_object("expander2").hide()
                # Expand expander 1 -> Only modify size in percent
                # exp_times= self.builder.get_object("expander1")
                #                        .set_expanded(True)
                if self.g310support:
                    self.buttonPx.set_sensitive(False)
                else:
                    self.buttonPx36.set_sensitive(False)

                # Init some helper vars
                self.several = True
                self.listbundle = self.filename
        else:
            print(_("Error"))
            self.lblresol.set_text(_("Error"))

        if self.tipo == 1:
            self.label6.set_text(_("Click here to update preview"))
            self.label6.show()
            self.labelsave.hide()
        elif self.tipo == 2:
            self.label6.set_text(_("The images you selected "
                                   "have different sizes"))
            self.label6.show()
            self.labelsave.hide()
            self.builder.get_object("box11").hide()
        elif self.tipo == 0:
            self.builder.get_object("box11").show()
            self.label6.hide()
            self.labelsave.show()
        else:
            self.label6.set_text(_(self.label6.get_text()))
            self.label6.show()

    def setfilename(self, widget):
        "After selecting a file on Filechooserbutton"
        self.filech.hide()
        self.filename = self.filech.get_filenames()
        self.listbundle = self.filename
        # How many images are selected? Do different things in each case
        self.updateUI(self.filename)

#        if self.hidelabel and not (self.tipo == 1 or self.tipo == 2):
#            self.label6.hide() #Hides the label "Click on image to change"

    def setlabelsave(self):
        "Changes imput text (on the bottom) for change file"
        if self.tipo == 0:
            name, ext = os.path.splitext(os.path.basename(self.filename))

            if self.nwnamefile() is False:
                self.labelsave.set_text(name+''+ext)
            else:
                self.labelsave.set_text(
                    name+"("+self.lblresol.get_text()+")"+ext)

        else:
            self.labelsave.set_placeholder_text(_("file.png"))
            self.labelsave.set_text(_("file.png"))

    def closefilename(self, widget):
        self.filech.hide()

    def calcheight(self):
        width = self.inputwidth.get_value_as_int()
        if width != 0:
            height = width/self.ratio
            # print "nuevo height", height
        else:
            # print "Valor 0"
            height = 1
        return int(height)

    def calcwidth(self):
        height = self.inputheight.get_value_as_int()
        if height != 0:
            width = height*self.ratio
            # print "nuevo width",width
        else:
            # print "Valor 0"
            width = 1
        return int(width)

    def widthcursor(self, widget, *args):
        if(self.checkprop.get_active()):
            # print "New width"
            self.inputheight.set_value(self.calcheight())
        nwdth = float(self.inputwidth.get_value_as_int())
        nhght = float(self.inputheight.get_value_as_int())
        self.lblresol.set_text(str(int(nwdth))+"x"+str(int(nhght)))
        self.setlabelsave()
        self.ad = False

        # None
    def heightcursor(self, widget, *args):
        if(self.checkprop.get_active()):
            # print "New height"
            self.inputwidth.set_value(self.calcwidth())
        nwdth = float(self.inputwidth.get_value_as_int())
        nhght = float(self.inputheight.get_value_as_int())
        self.lblresol.set_text(str(int(nwdth))+"x"+str(int(nhght)))
        self.setlabelsave()
        self.da = False
        # None

    def proporcionar(self, widget):
        None

    def showpreferences(self, widget):
        "Shows preferences window"
        value = self.nwnamefile()
        print(value)
        self.switch_newfilename.set_active(value)

        # Translate window title
        self.wpref.set_title(_("Pimagizer preferences"))
        self.wpref.show()
        # config.get_value("height")

    def cancelpref(self, widget):
        self.wpref.hide()

    def aceptpref(self, widget):
        "After clicking button accept on preferences window"
        self.wpref.hide()
        # Configure height
        config.set_value("height", self.spinprew.get_value_as_int())
        # Configure saving options
        if self.switch_newfilename.get_active():
            valor = 1  # New file name
        else:
            valor = 0  # overwrite
        print("Setting up value:", valor)
        config.set_value("newname", valor)
        self.f_labelnwfl()

    def nwnamefile(self):  # returns true if file name is image(WxH).png
        if config.get_value("newname") == 0:
            # print "sobrescribir"
            return False  # overwrite
        else:
            # print "No sobreescribe"
            return True  # New file name

    def f_labelnwfl(self):
        """Updates the text tag for advice the user which mode is using"""
        if self.nwnamefile():
            texto = _("Saving under new name")
        else:
            texto = _("You are <b>overwritting</b> the image file")
        self.labelnwfl.set_text(texto)
        self.labelnwfl.set_use_markup(True)

    def pref_saving(self, widget, *args):
        # notebook.set_tab_pos
        "Change position of tabs in notebook (set 1 as default)"
        posini = self.ntbkpref.get_current_page()
        movim = 1-posini
        if movim > 0:  # + (plus)
            for i in range(0, movim):
                self.ntbkpref.next_page()
        elif movim < 0:  # - (neg)
            movim = abs(movim)
            for i in range(0, movim):
                self.ntbkpref.prev_page()
        self.showpreferences(self.wpref)

    def folderset(self):
        """Returns value of filechooser if selected folder"""
        # if True:#self.selected:
        print("existe")
        return [True, self.btflsave.get_filename()]
        # else:
        #     print "no"
        #     return [False,""]

    #####
    # When open one expand, the other gets closed
    #####
    def expander_pix(self, widget):
        """Esta función hace que se encoja el expand de pixeles,
        cuando se expande el de "times"""
        if self.exp_times.get_expanded():
            self.exp_times.set_expanded(False)

    def expander_times(self, widget):
        """Esta función hace que se encoja el expand de times,
        cuando se expande el de pixeles"""
        if self.exp_pix.get_expanded():
            self.exp_pix.set_expanded(False)
    ####

    def times_changed(self, widget):
        """Updates the width and height when changed the absolute size"""
        percent = int(widget.get_value()) * math.pow(100, -1)
        altura = percent*self.absheight
        # print "altura",altura
        anchura = percent*self.abswidth
        self.inputheight.set_value(altura)
        self.inputwidth.set_value(anchura)
        self.lblresol.set_text(str(int(anchura))+"x"+str(int(altura)))
        self.lblresol1.set_text(str(int(anchura))+"x"+str(int(altura)))
        self.setlabelsave()

    #########
    # ### Changes the text on label for user help
    def sethelp_exp_times(self, widget, widget_ev):
        widget.set_text(_("You can select here how small \n"
                          "you want your new image(s), \n"
                          "expressed in percent (%)"))

    def sethelp_exp_times_(self, widget, widget_ev):
        widget.set_text(_("Help? Click"))
    # ### Finish changes
    #########

    def on_init(self, widget):
        print("New preview should load")
        print("now!")

    def update_img_callbk(self, img_retrieved):
        """Callback to update image when ready"""
        print("call", img_retrieved)

        # Uses callback arg for update the image
        self.wdgtimg.set_from_pixbuf(self.resizing(img_retrieved))
        self.label6.hide()

    def bundle_update(self, widget, widget2):
        """Update the preview when a bundle is loaded"""
        if self.tipo == 1:
            # Call to other fucntion which handles better the process
            self.bundle_update_2(widget, self.update_img_callbk)

    def bundle_update_2(self, spinner, update_img_callbk):
        """Function which makes better update the GTK UI"""
        # Initialize spinner
        spinner.show()
        spinner.start()

        def runthread():
            # Called in other thread
            returned = getimage.savefromPIL(
                        getimage.getimage_2(self.listbundle),
                        "bundle-mosaic.png")
            # Add
            GObject.idle_add(finished, returned)

        def finished(returned):
            """When function finishes"""
            # Stop and hide the spinner
            spinner.stop()
            spinner.hide()

            # Join thread
            th.join()

            # Return argument for update image
            update_img_callbk(returned)

        # Call to threading
        th = threading.Thread(target=runthread)
        th.start()

    def toggledPx(self, widget, widgetCom):
        # Hide box of Pr (23) and show box of Px(6)
        if widget.get_active():
            self.boxPr.hide()
            if widgetCom.get_active():
                widgetCom.set_active(False)
            self.boxPx.show()

    def toggledPr(self, widget, widgetCom):
        if widget.get_active():
            self.boxPx.hide()
            if widgetCom.get_active():
                widgetCom.set_active(False)
            self.boxPr.show()


# Ejecucion del programa
if __name__ == '__main__':
    pimagizer = Pimagizer([])
    Gtk.main()
