# virtual_scaler
 Balança virtual que envia informações constantemente para uma porta fixa

## Instalação
Para instalar o programa, basta clonar o repositório, instalar as dependências e executar o arquivo `main.py`:

```bash
git clone
cd virtual_scaler
pip install -r requirements.txt
python main.py
```

Para criar um executável, eu utilizei o `pyinstaller` com esses parâmetros:

```bash
pyinstaller --onefile --noconsole -i icon.ico --add-data "icon.ico;." -n 'Virtual Scaler' main.py
```

## Pré-requisitos

É necessário ter o Python 3.6 ou superior instalado na máquina.

É importante também ter alguma ferramenta para visualizar a comunicação serial, como o [PuTTY](https://www.putty.org/), ou o [com0com](https://sourceforge.net/projects/com0com/).

Em programas como o com0com, criamos duas portas virtuais - uma será utilizada para enviar os dados, e a outra para recever. Assim, podemos testar a comunicação serial sem a necessidade de um dispositivo físico.

## Funcionamento

Ao executar o aplicativo, ele irá procurar por um `config.ini` no diretório onde ele foi executado. Caso não possua, ele irá criar um arquivo com as configurações padrão.

```ini
[CUSTOM]
comm_port = COM2
baud_rate = 9600
weight_type = fixed
weight_min = 0
weight_max = 0
weight_fixed = 1000
update_time = 1
```

Caso o arquivo já exista, ele irá carregar as configurações presentes no arquivo.

Então, caso as configurações estejam corretas, ele irá imediatamente iniciar a comunicação com a porta e enviar os dados.

Caso as configurações estejam incorretas, ele irá acusar o erro e abrir uma janela de configuração para que o usuário possa alterar as configurações.

## Funcionalidades

O programa irá enviar constantemente informações para a porta serial, seguindo o formato apontado via código:

```python
def formatar_peso(self, peso):
    peso_str = f"{peso:.0f}"
    return f"\x02{peso_str.rjust(5, '0')}\x03"
```

Ao iniciar, também é criado um ícone na bandeja do sistema, onde o usuário pode acessar as configurações do programa, ler as configurações gravadas atualmente, ou fechar o programa.


## Configurações
No momento temos algumas opções de inicialização, como:
- **Porta COM** - O programa irá escanear e apontar as portas disponíveis, para então o usuário escolher uma porta específica
- **Baud Rate** - A taxa de transmissão de dados (no momento não tá fazendo a mínima diferença, essa informação não é utilizada na execução)
- **Tipo de peso** - Define se o peso será uma quantidade fixa ou aleatória
- **Peso Fixo** - Define o peso que será enviando caso o tipo seja fixo
- **Peso Mímimo** - Define o peso mínimo que será enviado caso o tipo de peso seja aleatório
- **Peso Máximo** - Define o peso máximo que será enviado caso o tipo de peso seja aleatório
- **Intervalo de envio** - Define o intervalo de tempo que o programa irá enviar as informações na porta serial

## Contribuição
Caso queira contribuir com o projeto, basta fazer um fork do repositório e enviar um pull request com as alterações.

## Licença
Esse projeto está sob a licença MIT.

