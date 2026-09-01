import os
import sys


def get_bundle_dir():
    """Diretório com os arquivos empacotados pelo PyInstaller (icon.ico, VERSION)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_app_dir():
    """Diretório do executável, usado para arquivos graváveis (config.ini, log)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
