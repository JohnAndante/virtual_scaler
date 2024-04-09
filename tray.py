import os
import config
from pystray import MenuItem as item
from pystray import Icon as icon_pys
from PIL import Image

class TrayIcon:
    def __init__(self, image_path, scale_instance):
        self.image_path = image_path
        self.icon = self.create_icon(self.image_path)
        self.scale = scale_instance


    def show_icon(self):
        print("Mostrando o icon")
        self.icon.run_detached()
        print("Icon mostrado")
        return self.icon

    def exit_icon(self):
        print("Escondendo o icon")
        self.icon.stop()
        print("Fechando a aplicação")
        os._exit(0)

    def open_config_gui(self):
        print("Recuperando configurações")
        curr_config = config.Config('config.ini').config_data
        print("Abrindo a GUI de configuração")
        config.Config('config.ini').create_config_window()
        print("GUI de configuração fechada")

    def open_about_gui(self):
        print("Abrindo a GUI de sobre")
        config.Config('config.ini').create_about_window()
        print("GUI de sobre fechada")

    def create_icon(self, image_path):
        print("Criando o icon")
        image = Image.open(image_path)
        menu = (
            item('Configurações', self.open_config_gui),
            item('Sobre', self.open_about_gui),
            item('Fechar aplicação', self.exit_icon),
            )
        icon = icon_pys("name", image, "Virtual Scaler", menu)

        print("Icon criado")
        return icon
