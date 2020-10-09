import os
import pkg_resources

def get_base_src():
    return pkg_resources.resource_filename(__name__, 'src/')

def config_translations():
    import gettext
    # For translations:
    APP = "pimagizer"
    DIR = pkg_resources.resource_filename(__name__, 'i18n/')

    # Esto permite traducir los textos escritos en el .py (no en glade)
    gettext.textdomain(APP)
    gettext.bindtextdomain(APP, DIR)
    # Y con esto podemos marcar las cadenas a traducir de la forma _("cadena")
    # _ = gettext.gettext
    # End translations

    return gettext.gettext        
