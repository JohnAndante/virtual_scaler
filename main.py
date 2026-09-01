import os
from tkinter import messagebox
import config
import tray
import scale
import paths
from logger import logger

class Main:
    def __init__(self):
        self.config = None
        self.tray = None
        self.scale = None

    def iniciar(self):
        icon_path = os.path.join(paths.get_bundle_dir(), 'icon.ico')

        logger.info("Iniciando virtual scale")
        logger.info("Recuperando configurações...")
        self.config = config.Config('config.ini').config_data
        logger.info("Configurações recuperadas.")

        self.scale = scale.Scale(self.config)
        self.tray = tray.TrayIcon(icon_path, self.scale)

        logger.info("Iniciando tray icon...")
        self.tray.show_icon()
        logger.info("Tray icon iniciado.")

        logger.info("Iniciando comunicação com a balança...")
        respo = self.scale.start_scale()

        if respo is None:
            logger.error("Falha ao iniciar a comunicação com a balança.")
            messagebox.showerror("Erro", "Falha ao iniciar a comunicação com a balança.")
            return
        elif respo == 0:
            logger.info("Comunicação encerrada.")
            self.tray.exit_icon()
            return
        elif respo == 1 or respo == 2:
            config.Config('config.ini').create_config_window()
            self.tray.exit_icon()
            return
        return

if __name__ == '__main__':
    main = Main()
    main.iniciar()
