import os


def config_translations():
    import gettext
    # For translations:
    APP = "pimagizer"
    DIR = "/home/vfrico/Documentos/development/pimagizer/src/i18n/"
    # Esto permite traducir los textos escritos en el .py (no en glade)
    gettext.textdomain(APP)
    gettext.bindtextdomain(APP, DIR)
    # Y con esto podemos marcar las cadenas a traducir de la forma _("cadena")
    # _ = gettext.gettext
    # End translations
    return gettext.gettext


def get_base_src():
    if "PIMAGIZER_SRC" in os.environ:
        return os.environ["PIMAGIZER_SRC"]
    else:
        return "/usr/share/pimagizer"
