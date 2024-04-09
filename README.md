# virtual_scaler
 Balança virtual que envia informações constantemente para uma porta fixa

## Instalação
Para instalar o programa, basta clonar o repositório e executar o arquivo `main.py`:

```bash
git clone
cd virtual_scaler
python main.py
```

Para instalar as dependências, basta executar o comando:

```bash
pip install -r requirements.txt
```

## Configurações
No momento temos algumas opções de inicialização, como:
- **Porta COM** - O programa irá escanear e apontar as portas disponíveis, para então o usuário escolher uma porta específica
- **Baud Rate** - A taxa de transmissão de dados (no momento não tá fazendo a mínima diferença, essa informação não é utilizada na execução)
- **Tipo de peso** - Define se o peso será uma quantidade fixa ou aleatória
- **Peso Fixo** - Define o peso que será enviando caso o tipo seja fixo
- **Peso Mímimo** - Define o peso mínimo que será enviado caso o tipo de peso seja aleatório
- **Peso Máximo** - Define o peso máximo que será enviado caso o tipo de peso seja aleatório
- **Intervalo de envio** - Define o intervalo de tempo que o programa irá enviar as informações na porta serial
