#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt  # for parse args
import gi
from pimagizer import gtkpimagizer


# Load PyGObject for Gtk dialogs
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib


def main():
    # [1:] => Quita el primer argumento ya que es el nombre del programa
    main_with_args(sys.argv[1:])
    # GLib.threads_init()
    # Gdk.threads_init()
    # Gdk.threads_enter()
    Gtk.main()
    # Gdk.threads_leave()
    # GObject.threads_init()


def main_with_args(argv):
    try:
        opt, args = getopt.getopt(argv, "he:dp:",
                                  ["help", "execute=", "dothis", "print="])
        print("Opt (Options?): "+str(opt))
        print("Args (Argumentos?): "+str(args))
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    output = None
    verbose = False

    for option, argument in opt:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option in ("-d", "--dothis"):
            print("dothis")
            sys.exit()
        elif option in ("-p", "--print"):
            print(str(argument))
            sys.exit()
        else:
            assert False, "Unhandled option"

    home = os.path.expanduser("~")

    if not os.path.exists(home+"/.config/pimagizer/conf.db"):
        print("No existe")
        from pimagizer import config
        config.createbase()
    else:
        from pimagizer import config
        config.try_value("newname", 1)
        config.try_value("defaultpx", 1)
        print("Exists")

    if not opt:
        pimagizer = gtkpimagizer.GtkPimagizer(args)


def usage():
    print("""
    -h --help                 Prints this
    -d --dothis               Print dothis
    -p --print (argument)     Print (argument)
    """)


if __name__ == "__main__":
    main()