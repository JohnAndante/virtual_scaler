import argparse
import serial
import time

porta_com = 'COM'
baud_rate = 2400
tipo_dado = 'aleatorio'


# print(f"Porta COM escolhida: {porta_com}")

def formatar_peso(peso):
    peso_str = f"{peso:.0f}"
    return f"\x02{peso_str.rjust(5, '0')}\x03"

def gerar_peso_aleatorio(inicio, fim):
    return random.uniform(inicio, fim)

def recuperar_comm_port():
    parser = argparse.ArgumentParser(description='Processa a porta COM.')
    parser.add_argument('-p', '--porta', type=str, help='a porta COM a ser utilizada')
    parser.add_argument('-b', '--baudrate', type=int, help='o baud rate da porta COM')
    parser.add_argument('-t', '--tipo', type=str, help='o tipo de dado a ser enviado')
    parser.add_argument('-f', '--fixo', type=int, help='o peso fixo a ser enviado')
    args = parser.parse_args()

    if args.porta is None:
        args.porta = input("Digite o número da porta COM: ")
        if args.porta.isnumeric():
            args.porta = f"COM{args.porta}"
        else:
            # print("Digite um número válido.")
            return recuperar_comm_port()

    if args.baudrate is None:
        args.baudrate = 2400

    if args.tipo is None:
        args.tipo = 'aleatorio'

    if args.tipo == 'fixo' and args.fixo is None:
        args.fixo = input("Digite o peso fixo (em gramas): ")
        if args.fixo.isnumeric():
            args.fixo = int(args.fixo)
        else:
            # print("Digite um número válido.")
            return recuperar_comm_port()

    return args

def main():
    args = recuperar_comm_port()
    porta_com = args.porta
    baud_rate = args.baudrate
    tipo_dado = args.tipo
    peso_fixo = args.fixo

    # print(f"Porta COM escolhida: {porta_com}")
    # print(f"Baud rate: {baud_rate}\n")

    # print(f"Iniciando comunicação com a balança...")

    try:
        porta_serial = serial.Serial(porta_com, baud_rate, timeout=1)
        # print("Porta COM aberta com sucesso.")
    except serial.SerialException:
        # print(f"Erro ao abrir a porta COM {porta_com}. Certifique-se de que a porta está disponível e tente novamente.")
        exit()

    # print("Enviando dados...")
    try:
        while True:
            if tipo_dado == 'fixo':
                peso = peso_fixo
            else:
                peso = gerar_peso_aleatorio(1000, 9000)

            dados = formatar_peso(peso).encode('utf-8')
            porta_serial.write(dados)
            print(f"Dados enviados: {dados.decode('utf-8')}")
            time.sleep(1)
    except KeyboardInterrupt:
        porta_serial.close()
        # print("\nPrograma encerrado.")
    except serial.SerialException:
        # print(f"Erro ao enviar dados pela porta COM {porta_com}. Certifique-se de que a porta está disponível e tente novamente.")
        exit()
    except Exception as e:
        # print(f"Erro inesperado: {e}")
        exit()

main()
