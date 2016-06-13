# captura

O objetivo deste código é criar um crawler que visite o site epocacosmeticos.com.br e salve um arquivo .csv com o nome do produto, o título e a url de cada página de produto encontrada.

Regras:
 - Esse arquivo não deve conter entradas duplicadas;
 
 
# Necessário
 - Python 3.5
 - RabbitMq (https://www.rabbitmq.com/)
 
# Como Desenvolver

 1. clone o respositório.
 2. crie um virtualenvo com Python 3.5.
 3. Ative o virtualenv.
 4. Instale as dependências.
 5. Execute os testes.
 
 ```console
git clone git@github.com:lffsantos/captura.git captura
cd captura
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
py.test
```

# Como Executar a aplicação

 ```console
 python database.py
 ```
