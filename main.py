import os
import sys
from tkinter import messagebox
import config
import tray
import scale

class Main:
    def __init__(self):
        self.config = None
        self.tray = None
        self.scale = None

    def iniciar(self):
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(__file__)

        icon_path = os.path.join(base_dir, 'icon.ico')

        print("Iniciando virtual scale")
        print("Recuperando configurações...")
        self.config = config.Config('config.ini').config_data
        print("Configurações recuperadas.")

        self.scale = scale.Scale(self.config)
        self.tray = tray.TrayIcon(icon_path, scale)

        print("Iniciando tray icon...")
        self.tray.show_icon()
        print("Tray icon iniciado.")

        print("Iniciando comunicação com a balança...")
        respo = self.scale.start_scale()

        if respo is None:
            print("Falha ao iniciar a comunicação com a balança.")
            messagebox.showerror("Erro", "Falha ao iniciar a comunicação com a balança.")
            return
        elif respo == 0:
            print("Comunicação encerrada.")
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
