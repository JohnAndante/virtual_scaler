import os
import configparser
import re
import sys
import serial
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import serial.tools
import serial.tools.list_ports


class Config:



    config_keys = ['comm_port', 'baud_rate', 'weight_type', 'weight_min', 'weight_max', 'weight_fixed', 'update_time']

    config_labels = {
       'comm_port':'Porta COM',
       'baud_rate': 'Baud Rate',
       'weight_type': 'Tipo de Peso',
       'weight_min': 'Peso Mínimo (g)',
       'weight_max': 'Peso Máximo (g)',
       'weight_fixed': 'Peso Fixo (g)',
       'update_time': 'Tempo de Atualização (s)'
    }

    config_acceptable_values = {
        'comm_port': 'COM[0-9]+',
        'baud_rate': [
            '2400',
            '4800',
            '9600',
            '19200',
            '38400',
            '57600',
            '115200'
        ],
        'weight_type': [
            'fixed',
            'random'
        ],
        'weight_min': '[0-9]+',
        'weight_max': '[0-9]+',
        'weight_fixed': '[0-9]+',
        'update_time': '[0-9]+'
    }

    default_config = {
        'comm_port': 'COM2',
        'baud_rate': '9600',
        'weight_type': 'fixed',
        'weight_min': '0',
        'weight_max': '0',
        'weight_fixed': '1000',
        'update_time': '1'
    }

    def get_base_dir(self):
            if getattr(sys, 'frozen', False):
                base_dir =  sys._MEIPASS
                return os.path.join(base_dir, 'icon.ico')
            else:
                base_dir =  os.path.dirname(__file__)
                return os.path.join(base_dir, 'icon.ico')

    def __init__(self, config_file):
        print("Iniciando configurações...")
        self.config_file = config_file
        print(f"Arquivo de configuração: {self.config_file}")
        self.config_data = self.read_config(config_file)
        print("Configurações lidas.")
        print(self.config_data)
        self.window = None
        self.config_entries = {}
        self.get_available_com_ports()

    def read_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        config_data = {}
        if 'CUSTOM' not in config:
            try:
                print("Arquivo de configuração inválido, criando novo")
                self.delete_file(config_file)

                self.create_config()
                config.read(config_file)
            except Exception as e:
                print(f"Erro ao criar arquivo de configuração: {e}")
            return self.default_config

        is_valid = self.validate_data(config['CUSTOM'])

        if not is_valid:
            print("Valores inválidos, recuperando valores padrão")
            try:
                self.delete_file(config_file)
                self.create_config()
            except Exception as e:
                print(f"Erro ao criar arquivo de configuração: {e}")
            return self.default_config

        for key, value in config['CUSTOM'].items():
            config_data[key] = value
        return config_data

    def delete_file(self, config_file):
        if os.path.exists(config_file) and os.path.isfile(config_file):
            os.remove(config_file)
        return

    def create_config(self):
        configs = self.default_config
        with open(self.config_file, 'w') as configfile:
            config = configparser.ConfigParser()
            config['CUSTOM'] = configs
            config.write(configfile)
        return

    def save_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        entries_data = {}
        config['CUSTOM'] = {}

        for key, value in self.config_entries.items():
            if isinstance(value, tk.Entry) or isinstance(value, ttk.Combobox):
                entries_data[key] = value.get()
            else:
                entries_data[key] = value

        print("ENTRIES DATA: ", entries_data)
        is_valid = self.validate_data(entries_data)

        if not is_valid:
            messagebox.showerror('Erro', 'Valores inválidos. Verifique os campos e tente novamente.')
            return

        for key, value in entries_data.items():
            config['CUSTOM'][key] = value

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

        messagebox.showinfo('Sucesso', 'Configurações salvas com sucesso.')
        self.window.destroy()

        messagebox.showinfo('Atenção', 'As alterações só terão efeito após reiniciar o programa.')
        return

    def validate_data(self, widget):
        print("WIDGETO: ", widget)

        for key, value in widget.items():
            print(f"Validando {key}: {value}")
            if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                value = widget.get()


            if key not in self.config_keys:
                return False
            if key == 'comm_port':
                if not re.match('COM[0-9]+', value):
                    print(f"Porta COM inválida: {value}")
                    return False
            if key == 'baud_rate':
                if value not in self.config_acceptable_values['baud_rate']:
                    print(f"Baud rate inválido: {value}")
                    return False
            if key == 'weight_type':
                if value not in self.config_acceptable_values['weight_type']:
                    print(f"Tipo de peso inválido: {value}")
                    return False
            if key == 'weight_min':
                if not re.match('[0-9]+', value):
                    print(f"Peso mínimo inválido: {value}")
                    return False
            if key == 'weight_max':
                if not re.match('[0-9]+', value):
                    print(f"Peso máximo inválido: {value}")
                    return False
            if key == 'weight_fixed':
                if not re.match('[0-9]+', value):
                    print(f"Peso fixo inválido: {value}")
                    return False
            if key == 'update_time':
                if not re.match('[0-9]+', value):
                    print(f"Tempo de atualização inválido: {value}")
                    return False
        return True

    def create_config_window(self):

        if self.window is not None:
            self.window.destroy()

        self.window = tk.Tk()
        self.window.iconbitmap(self.get_base_dir())
        self.window.focus_force()
        self.window.title('Configurações')
        self.window.geometry('300x300')


        main_frame = tk.LabelFrame(self.window, text='Configurações', bd=2, font=('Arial', 9))
        main_frame.pack(fill='both', expand='yes', padx=10, pady=10)

        for key in self.config_keys:
            row = tk.Frame(main_frame)
            label = tk.Label(row, text=self.config_labels[key], width=22, anchor='w', justify='left', font=('Arial', 8))

            if (key == 'comm_port'):
                self.config_entries[key] = ttk.Combobox(row, values=self.get_available_com_ports(), textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].set(self.config_data[key])
                self.config_entries[key]['state'] = 'readonly'
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'baud_rate'):
                self.config_entries[key] = ttk.Combobox(row, values=self.config_acceptable_values[key], textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].set(self.config_data[key])
                self.config_entries[key]['state'] = 'readonly'
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'weight_type'):
                self.config_entries[key] = ttk.Combobox(row, values=self.config_acceptable_values[key], textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].set(self.config_data[key])
                self.config_entries[key]['state'] = 'readonly'
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'weight_min'):
                self.config_entries[key] = tk.Entry(row, textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].insert(0, self.config_data[key])
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'weight_max'):
                self.config_entries[key] = tk.Entry(row, textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].insert(0, self.config_data[key])
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'weight_fixed'):
                self.config_entries[key] = tk.Entry(row, textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].insert(0, self.config_data[key])
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            elif (key == 'update_time'):
                self.config_entries[key] = tk.Entry(row, textvariable=tk.StringVar(), width=5, font=('Arial', 8))
                self.config_entries[key].insert(0, self.config_data[key])
                self.config_entries[key].pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

            else:
                print(f"Erro ao criar campo para a chave {key}")
                continue

            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)

        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES, padx=5, pady=5)
        button_save = tk.Button(buttons_frame,
                                text='Salvar',
                                command=lambda: self.save_config(),
                                font=('Arial', 8),
                                width=15, height=3)
        button_save.pack(side=tk.RIGHT, padx=5, pady=5)
        button_config = tk.Button(buttons_frame,
                                text='Cancelar',
                                command=lambda: self.destroy_window(),
                                font=('Arial', 8),
                                width=15, height=3)
        button_config.pack(side=tk.RIGHT, padx=5, pady=5)

        tk.mainloop()

    def create_about_window(self):
        self.window = tk.Tk()
        self.window.iconbitmap(self.get_base_dir())
        self.window.focus_force()
        self.window.title('Sobre')
        self.window.geometry('300x300')

        main_frame = tk.LabelFrame(self.window, text='Virtual Scaler v0.0.2', bd=2, font=('Arial', 9))
        main_frame.pack(fill='both', expand='yes', padx=10, pady=10)

        for key in self.config_keys:
            row = tk.Frame(main_frame)
            label = tk.Label(row, text=self.config_labels[key], width=22, anchor='w', justify='left', font=('Arial', 8))
            entry = tk.Entry(row, width=5, font=('Arial', 8))
            entry.insert(0, self.config_data[key])
            entry.config(state='readonly')
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES, padx=5, pady=5)

        button_close = tk.Button(buttons_frame,
                                 text='Fechar',
                                 command=self.window.destroy(),
                                 font=('Arial', 8),
                                 width=15, height=3)
        button_close.pack(side=tk.RIGHT, padx=5, pady=5)
        button_config = tk.Button(buttons_frame,
                                  text='Configurações',
                                  command=self.create_config_window(),
                                  font=('Arial', 8),
                                  width=15, height=3)
        button_config.pack(side=tk.RIGHT, padx=5, pady=5)


        tk.mainloop()

    def get_available_com_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def destroy_window(self):
        if self.window is not None:
            self.window.destroy()
            self.window = None









