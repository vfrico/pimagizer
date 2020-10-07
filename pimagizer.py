#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt  # for parse args
import gi


def inject_env(main_file):
    """Find where the pimagizer lib is installed."""
    # Test if we are under a bin directory
    script_path = os.path.realpath(main_file)
    path, file = os.path.split(script_path)
    print(path)
    print(not path.startswith("/usr/local/lib/py"))
    print(path not in ("/bin", "/usr/bin", "/usr/local/bin"))
    if path.startswith("/opt/extras.ubuntu.com/"):
        final_path = "/opt/extras.ubuntu.com/pimagizer"
    elif path not in ("/bin", "/usr/bin", "/usr/local/bin") and\
            not path.startswith("/usr/local/lib/py"):
        final_path = os.path.join(path, "src")
    else:
        final_path = "/usr/share/pimagizer"

    if "PIMAGIZER_SRC" not in os.environ:
        os.environ["PIMAGIZER_SRC"] = final_path


# Load pimagizer library
inject_env(__file__)
sys.path.insert(0, os.environ["PIMAGIZER_SRC"])
from pimagizer import gtkpimagizer


# Load PyGObject for Gtk dialogs
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GLib


def main(argv):
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
    # [1:] => Quita el primer argumento ya que es el nombre del programa
    main(sys.argv[1:])
    # GLib.threads_init()
    # Gdk.threads_init()
    # Gdk.threads_enter()
    Gtk.main()
    # Gdk.threads_leave()
    # GObject.threads_init()
