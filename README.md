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

# Como Executar:

 - Criar  Banco e dados da Aplicação;
    
        pip install rows
 
 - Rodar Crawler e Enfileirar mensagens;  

    `N`: Número de links por mensagem. ex: 7  
    `queue_name`: nome da fila. ex: produtos 
    
    Opção 1:  
    
        python crawler.py
        python enqueuer.py -l `N` -q `queue_name`
        
    Opção 2:
        
        python flow.py -l `N` -q `queue_name`

- Rodar o Processor:
    `N`: Número de workers por aplicação.   
    `queue_name`: nome da fila. ex: produtos
     
        python processor.py -w `N` -q `queue_name`

- Rodar o Indexer:
  
        python indexer.py
        
        