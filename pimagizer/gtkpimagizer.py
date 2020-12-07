#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#
#   File: gtkpimagizer.py
#   Gui of pimagizer
#
#   This file is part of Pimagizer
#   Pimagizer (C) 2012-2020 Víctor Fernández Rico <vfrico@gmail.com>
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
from pimagizer import gtkpreferences
from pimagizer import gtkfilechooser
from pimagizer import gtkabout
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


def gtk_hide(widget, data):
    print("Hide window")
    widget.hide()
    return True


class GtkPimagizer:
    def __init__(self, imputfile):

        # Gets the GTK Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file(get_resources_folder() + "ui/main.glade")

        # Get the GTK object
        self.wdgtimg = self.builder.get_object("mainimage")

        # Sets the default file for image
        self.filename = get_resources_folder() + "/pimagizer-main.png"

        self.absheight = 0
        self.abswidth = 0

        # #********************************************
        # ###### GET EACH OBJECT ON BUILDER ###########
        # #********************************************

        # Preferences Window
        self.gtk_prefs = gtkpreferences.GtkPimagizerPreferences()

        # File chooser
        self.filech = gtkfilechooser.GtkFileChooser(file_selected_cb=self._callback_filechoosen)

        # About window
        self.gtkAbout = gtkabout.GtkAbout()

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
        self.lblst = self.builder.get_object("labelst")

        # Save folder
        self.btflsave = self.builder.get_object("filechooserbutton1")
        self.btflsave.set_title(_(self.btflsave.get_title()))
        self.labelsave = self.builder.get_object("savefile")

        # Formats box
        self.boxformats = self.builder.get_object("formatbox")

        # Expanders
        self.boxPx = self.builder.get_object("box_width_height")
        self.boxPr = self.builder.get_object("box_percent")

        self.height1 = self.builder.get_object("height1")
        self.height1.set_value(100)

        self.gtk_translate_label("label_percent")
        self.gtk_translate_label("label_help")
        self.gtk_translate_label("label3")
        self.gtk_translate_label("label_size")
        self.gtk_translate_label("label_width")
        self.gtk_translate_label("label_height")

        #  Translates
        # "Click on image to change"
        self.label_under_preview = self.builder.get_object("label_under_preview")
        self.labelnwfl = self.builder.get_object("labelnwfl")
        self.f_labelnwfl()

        signals = {
            "about_activate": self.showabout,
            "main_close": self.cerrarapp,
            "resize-accept": self.resizeimg,
            "File-update": self.updateimg,
            "main-update": self.updateimg,
            "img-click": self.updateimg,
            "height-cursor": self.heightcursor,
            "width-cursor": self.widthcursor,
            "chfile": self.changefile,
            "activeprop": self.proporcionar,
            # "expander_pix": self.expander_pix,
            # "expander_times": self.expander_times,
            "times_changed": self.times_changed,
            "help_exp_times": self.sethelp_exp_times,
            "help_exp_times_": self.sethelp_exp_times_,
            "iniciado": self.on_init,
            "bundle-update": self.bundle_update,
            "nwfile-lbl": self._unhandled_singal,
            "show-preferences": self._unhandled_singal_show_prefs,
        }

        self.builder.connect_signals(signals)

        # Get main window
        self.window1 = self.builder.get_object("window1")

        # Add a HeaderBar
        self.hb = self.gtk_generate_headerbar()
        self.window1.set_titlebar(self.hb)

        # Show Window and HeaderBar
        self.hb.show()
        self.window1.show()

        if not imputfile:
            imputfile = [self.filename]
        print("imputfile+ "+str(imputfile))
        self.updateUI(imputfile)

        if self.window1:
            self.window1.connect("destroy", self.cerrarapp)

    def _unhandled_singal(self, inst, widget, *args, **kwargs):
        print("Se ha producido una señal que no se está gestionando de la "
              "forma adecuada. La ha producido el widget {} "
              "con la lista de argumentos: {}".format(widget, str(args)))
        print(inst)
        print(kwargs)

    def gtk_generate_headerbar(self):
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Pimagizer"

        ############################################
        # *** Buttons About and Preferences
        button_ab = Gtk.Button()
        icon_ab = Gio.ThemedIcon(name="gtk-about")
        image_ab = Gtk.Image.new_from_gicon(icon_ab, Gtk.IconSize.BUTTON)
        button_ab.add(image_ab)
        button_ab.show()
        image_ab.show()
        button_ab.connect("clicked", self.showabout)

        button_st = Gtk.Button()
        icon_st = Gio.ThemedIcon(name="gtk-preferences")
        image_st = Gtk.Image.new_from_gicon(icon_st, Gtk.IconSize.BUTTON)
        button_st.add(image_st)
        button_st.show()
        image_st.show()
        button_st.connect("clicked", self.gtk_prefs.showpreferences)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        box.add(button_ab)
        box.add(button_st)
        box.show()

        hb.pack_start(box)

        ###############################################
        # *** Buttons Pixels(px) and Percent(%)
        big_format = '<span size="xx-large"><b>{}</b></span>'

        self.button_px = Gtk.ToggleButton()
        label_px = Gtk.Label(big_format.format("Px"))
        self.button_px.add(label_px)
        self.button_px.show()
        label_px.set_use_markup(True)
        label_px.show()

        # It is connected below
        self.button_pr = Gtk.ToggleButton()
        label_pr = Gtk.Label(big_format.format("%"))
        self.button_pr.add(label_pr)
        self.button_pr.show()
        label_pr.set_use_markup(True)
        label_pr.show()

        def toggled_px(widget, widget_com):
            # Hide box of Pr (23) and show box of Px(6)
            if widget.get_active():
                self.boxPr.hide()
                if widget_com.get_active():
                    widget_com.set_active(False)
                self.boxPx.show()

        def toggled_pr(widget, widget_com):
            if widget.get_active():
                self.boxPx.hide()
                if widget_com.get_active():
                    widget_com.set_active(False)
                self.boxPr.show()

        # pr => box23
        self.button_pr.connect("toggled", toggled_pr, self.button_px)
        # px => box6
        self.button_px.connect("toggled", toggled_px, self.button_pr)

        if config.get_value("defaultpx") == 1:
            # Si es verdad, esconder el Pr
            self.boxPr.hide()
            self.button_px.set_active(True)
        else:
            # Si no es verdad, esconder el Px
            self.boxPx.hide()
            self.button_pr.set_active(True)

        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box2.get_style_context(), "linked")
        box2.add(self.button_px)
        box2.add(self.button_pr)
        box2.show()

        hb.pack_end(box2)
        return hb

    def _unhandled_singal_show_prefs(self, inst, widget, *args, **kwargs):
        print("PREFSSe ha producido una señal que no se está gestionando de la "
              "forma adecuada. La ha producido el widget {} "
              "con la lista de argumentos: {}".format(widget, str(args)))
        print(inst)
        print(kwargs)

    def gtk_translate_label(self, glade_name):
        """Translates a label present in glade file"""
        label_widget = self.builder.get_object(glade_name)
        label_widget.set_text(_(label_widget.get_text()))

    def cerrarapp(self, widget):
        print(_("Saving preferences data"))
        if self.button_px.get_active():
            config.set_value("defaultpx", 1)
        else:
            config.set_value("defaultpx", 0)

        print(_("Closing program"))
        Gtk.main_quit()

    def showabout(self, widget):
        print(_("About"))
        self.gtkAbout.open()

    def _callback_filechoosen(self, file):
        self.filename = file
        self.listbundle = file
        # How many images are selected? Do different things in each case
        self.updateUI(self.filename)

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
            if self.labelsave.get_text() == "":
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
            if (ext == ".jpg" or ext == ".JPG" or
               ext == ".jpeg" or ext == ".JPEG"):
                ext2 = "JPEG"
            elif ext == ".png" or ext == ".PNG":
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
        if self.isimgbox:
            self.wdgtimg.hide()
            self.isimgbox = False
            self.imgfile.show()
        else:
            self.imgfile.hide()
            self.wdgtimg.show()
            self.isimgbox = True

    def changefile(self, widget, *args):
        self.filech.show()

    def update_sizeUI(self, wid, hei):
        """Updates the resolution on all items on UI and do them global"""

        self.absheight = hei
        self.abswidth = wid
        # self.ratio = int(wid) * math.pow(int(hei),-1)
        try:
            self.ratio = float(wid) / float(hei)
        except:
            self.ratio = 1
        print(self.ratio)

        if self.button_pr.get_active():
            percent = self.height1.get_value_as_int() * 0.01
        else:
            percent = 1
        print(percent)

        (wid, hei) = (int(wid * percent), int(hei * percent))
        print(wid, hei)
        self.lblresol.set_text(str(wid)+"x"+str(hei))  # Sets text on top label
        self.inputheight.set_value(hei)  # set height on imput
        self.inputwidth.set_value(wid)  # set width on input
        self.setlabelsave()  # Changes the imput text for file to save

    def updateUI(self, files):
        """Makes all needed actions to get ui updated"""
        self.filename = files
        print(self.filename)
        self.button_px.set_sensitive(True)

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
            print("La imagen tiene size: ", imagen.size)
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
                self.button_px.set_sensitive(False)

                # Init some helper vars
                self.several = True
                self.listbundle = self.filename
        else:
            print(_("Error"))
            self.lblresol.set_text(_("Error"))

        if self.tipo == 1:
            self.label_under_preview.set_text(_("Click here to update preview"))
            self.label_under_preview.show()
            self.labelsave.hide()
        elif self.tipo == 2:
            self.label_under_preview.set_text(_("The images you selected "
                                   "have different sizes"))
            self.label_under_preview.show()
            self.labelsave.hide()
            self.builder.get_object("box11").hide()
        elif self.tipo == 0:
            self.builder.get_object("box11").show()
            self.label_under_preview.hide()
            self.labelsave.show()
        else:
            self.label_under_preview.set_text(_(self.label_under_preview.get_text()))
            self.label_under_preview.show()

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
        if self.checkprop.get_active():
            print("New width")
            self.inputheight.set_value(self.calcheight())
        nwdth = float(self.inputwidth.get_value_as_int())
        nhght = float(self.inputheight.get_value_as_int())
        self.lblresol.set_text(str(int(nwdth))+"x"+str(int(nhght)))
        self.setlabelsave()
        # self.ad = False

    def heightcursor(self, widget, *args):
        if self.checkprop.get_active():
            print("New height")
            self.inputwidth.set_value(self.calcwidth())
        nwdth = float(self.inputwidth.get_value_as_int())
        nhght = float(self.inputheight.get_value_as_int())
        self.lblresol.set_text(str(int(nwdth))+"x"+str(int(nhght)))
        self.setlabelsave()
        # self.da = False

    def proporcionar(self, widget):
        None

    @staticmethod
    def nwnamefile():  # returns true if file name is image(WxH).png
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
    # def expander_pix(self, widget):
    #     """Esta función hace que se encoja el expand de pixeles,
    #     cuando se expande el de "times"""
    #     if self.exp_times.get_expanded():
    #         self.exp_times.set_expanded(False)
    #
    # def expander_times(self, widget):
    #     """Esta función hace que se encoja el expand de times,
    #     cuando se expande el de pixeles"""
    #     if self.exp_pix.get_expanded():
    #         self.exp_pix.set_expanded(False)
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
        self.label_under_preview.hide()

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




# Ejecucion del programa
if __name__ == '__main__':
    pimagizer = GtkPimagizer([])
    Gtk.main()
