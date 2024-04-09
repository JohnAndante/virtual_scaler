import random
import time
import serial
from tkinter import messagebox

config_bkp = {}

class Scale:
    instances = []

    def __init__(self, config_data):
        self.config = config_data
        self.serial = None
        self.running = False
        Scale.instances.append(self)
        pass

    @classmethod
    def stop_all(cls):
        for instance in cls.instances:
            instance.running = False
            instance.stop_scale()

        cls.instances.clear()
        return

    @classmethod
    def restart_all(cls):
        for instance in cls.instances:
            instance.restart_scale()

        return

    def stop_scale(self):
        if self.serial is not None:
            print("\nEncerrando a recepção de dados...")
            self.serial.close()
            self.serial = None
            self.running = False

    def restart_scale(self):
        print("\nParando a balança...")
        self.stop_scale()
        self.start_scale()
        return

    def gerar_peso_aleatorio(self, inicio, fim):
        return random.uniform(inicio, fim)

    def formatar_peso(self, peso):
        peso_str = f"{peso:.0f}"
        return f"\x02{peso_str.rjust(5, '0')}\x03"

    def start_scale(self):
        self.running = True

        if self.serial is not None:
            self.serial.close()

        try:
            print("\nIniciando a recepção de dados...")
            porta_com = self.config['comm_port']
            baud_rate = int(self.config['baud_rate'])
            tipo_dado = self.config['weight_type']
            peso_fixo = int(self.config['weight_fixed'])
            peso_min = int(self.config['weight_min'])
            peso_max = int(self.config['weight_max'])

            print("Dados recebidos.---------------------")
            print(f"Porta COM escolhida: {porta_com}")
            print(f"Baud rate: {baud_rate}")
            print(f"Tipo de dado: {tipo_dado}")
            print(f"Peso fixo: {peso_fixo}")
            print(f"Peso mínimo: {peso_min}")
            print(f"Peso máximo: {peso_max}")
        except KeyError as e:
            print(f"Erro ao recuperar dados do arquivo de configuração: {e}")
            messagebox.showerror("Erro", f"Erro ao recuperar dados do arquivo de configuração: {e}")
            return 1

        try:
            print("\nAbrindo porta COM...")
            self.serial = serial.Serial(porta_com, baud_rate, timeout=1)
        except serial.SerialException as e:
            print(f"Erro ao abrir a porta COM {porta_com}. Certifique-se de que a porta está disponível e tente novamente.")
            messagebox.showerror("Erro", f"Erro ao abrir a porta COM {porta_com}. Certifique-se de que a porta está disponível e tente novamente.")
            return 2

        print("Porta COM aberta com sucesso.")

        print("\nEnviando dados...")
        while self.running:
            try:
                if tipo_dado == 'fixed':
                    print(f"Peso fixo: {peso_fixo}")
                    peso = peso_fixo
                else:
                    peso = self.gerar_peso_aleatorio(peso_min, peso_max)
                    print(f"Peso aleatório: {peso}")

                peso_formatado = self.formatar_peso(peso)
                self.serial.write(peso_formatado.encode())
                print(f"Dados enviados: {peso_formatado}")

                time.sleep(int(self.config['update_time']))

            except KeyboardInterrupt:
                print("\nPrograma encerrado.")
                self.serial.close()
                return 0

            except serial.SerialException as e:
                print(f"Erro ao enviar dados: {e}")
                messagebox.showerror("Erro", f"Erro ao enviar dados:\n{e}").run_detached()
                self.serial.close()
                return 0

            except Exception as e:
                print(f"Erro inesperado: {e}")
                messagebox.showerror("Erro", f"Erro inesperado:\n{e}").run_detached()
                return 0


