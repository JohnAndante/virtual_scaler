import os
import config
from pystray import MenuItem as item
from pystray import Icon as icon_pys
from PIL import Image

from logger import logger

class TrayIcon:
    def __init__(self, image_path, scale_instance):
        self.image_path = image_path
        self.icon = self.create_icon(self.image_path)
        self.scale = scale_instance


    def show_icon(self):
        logger.info("Mostrando o icon")
        self.icon.run_detached()
        logger.info("Icon mostrado")
        return self.icon

    def exit_icon(self):
        logger.info("Escondendo o icon")
        self.icon.stop()
        logger.info("Fechando a aplicação")
        os._exit(0)

    def restart_scale(self):
        logger.info("Reiniciando comunicação com a balança")
        self.scale.restart_scale()

    def open_config_gui(self):
        logger.info("Recuperando configurações")
        config.Config('config.ini').create_config_window()
        logger.info("GUI de configuração fechada")

    def open_about_gui(self):
        logger.info("Abrindo a GUI de sobre")
        config.Config('config.ini').create_about_window()
        logger.info("GUI de sobre fechada")

    def create_icon(self, image_path):
        logger.info("Criando o icon")
        image = Image.open(image_path)
        menu = (
            item('Configurações', self.open_config_gui),
            item('Reiniciar comunicação', self.restart_scale),
            item('Sobre', self.open_about_gui),
            item('Fechar aplicação', self.exit_icon),
            )
        icon = icon_pys("name", image, "Virtual Scaler", menu)

        logger.info("Icon criado")
        return icon
