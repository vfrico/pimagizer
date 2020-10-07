from pimagizer import utils
from pimagizer import config
from pimagizer import gtkpimagizer

_ = utils.config_translations()


class GtkPimagizerPreferences():
    def __init__(self, glade_builder):

        # Preferences Window
        self.wpref = glade_builder.get_object("preferences")
        self.wpref.connect('delete-event', gtkpimagizer.gtk_hide)
        self.ntbkpref = glade_builder.get_object("notebook1")

        # On Preferences window
        # Right now, Pimagizer suports JPG and PNG formats
        self.label10 = glade_builder.get_object("label10")
        self.label10.set_text(_(self.label10.get_text()))
        self.label8 = glade_builder.get_object("label8")  # Works with
        self.label8.set_text(_(self.label8.get_text()))
        self.label7 = glade_builder.get_object("label7")  # Launchpad
        self.label7.set_text(_(self.label7.get_text()))
        self.linkbutton1 = glade_builder.get_object("linkbutton1")  # Translate
        self.linkbutton1.set_label(_(self.linkbutton1.get_label()))
        self.linkbutton2 = glade_builder.get_object("linkbutton2")  # Bugs
        self.linkbutton2.set_label(_(self.linkbutton2.get_label()))
        self.linkbutton3 = glade_builder.get_object("linkbutton3")  # Questions
        self.linkbutton3.set_label(_(self.linkbutton3.get_label()))
        self.label9 = glade_builder.get_object("label9")  # Size of preview
        self.label9.set_text(_(self.label9.get_text()))
        # Here you can set the size of the image preview on main window
        self.label13 = glade_builder.get_object("label13")
        self.label13.set_text(_(self.label13.get_text()))
        # Is recommended to set a value near to 300px
        self.label12 = glade_builder.get_object("label12")
        self.label12.set_text(_(self.label12.get_text()))
        self.label11 = glade_builder.get_object("label11")  # Height
        self.label11.set_text(_(self.label11.get_text()))
        self.label4 = glade_builder.get_object("label4")  # Information
        self.label4.set_text(_(self.label4.get_text()))
        self.label5 = glade_builder.get_object("label5")  # Interface
        self.label5.set_text(_(self.label5.get_text()))
        # preferences -> (tab) saving
        # Switch for new file name
        self.switch_newfilename = glade_builder.get_object("switch1")
        self.label15 = glade_builder.get_object("label15")  # label on tab
        self.label15.set_text(_(self.label15.get_text()))
        # title frame: <b>Saving options</b>
        self.label16 = glade_builder.get_object("label16")
        self.label16.set_text(_(self.label16.get_text()))
        self.label16.set_use_markup(True)
        # Do you want to save the new file with a
        self.label17 = glade_builder.get_object("label17")
        # new name as image(widthxheight).jpg?
        self.label17.set_text(_(self.label17.get_text()))
        # save images with new name
        self.label18 = glade_builder.get_object("label18")
        self.label18.set_text(_(self.label18.get_text()))
        # If you <b>turn off</b> this option, you will
        # <b>overwrite</b> all you save with Pimagizer
        self.label19 = glade_builder.get_object("label19")
        textohelp = _(("If you <b>turn off</b> this option, you will \n"
                       "<b>overwrite</b> all you save with Pimagizer"))
        self.label19.set_text(textohelp)
        self.label19.set_use_markup(True)

        # Preview size
        self.spinprew = glade_builder.get_object("spinbutton1")
        self.spinprew.set_value(config.get_value("height"))

        self.prefs_signals = {
            "show-preferences": self.showpreferences,
            "prefer-cancel": self.cancelpref,
            "preferences_close_cb": self.cancelpref,
            "nwfile-lbl": self.pref_saving,
            "prefer-acept": self.aceptpref
        }

    def get_signals(self):
        return self.prefs_signals

    def showpreferences(self, widget):
        "Shows preferences window"
        value = gtkpimagizer.GtkPimagizer.nwnamefile()
        print("newname file", value)
        self.switch_newfilename.set_active(value)

        # Translate window title
        self.wpref.set_title(_("Pimagizer preferences"))
        self.wpref.show()
        # config.get_value("height")
        print("Window wpref:", self.wpref)

    def cancelpref(self, widget):
        self.wpref.hide()
        return True

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
