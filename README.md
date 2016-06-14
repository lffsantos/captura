# captura

O objetivo deste código é criar um crawler que visite o site epocacosmeticos.com.br e salve um arquivo .csv com o nome do produto, o título e a url de cada página de produto encontrada.

Regras:
 - Esse arquivo não deve conter entradas duplicadas;
 
 
# Necessário
 - Python 3.5
 - RabbitMq (https://www.rabbitmq.com/)
 
# Como Desenvolver

 1. clone o respositório.
 2. crie uma virtualenv com Python 3.5. (https://virtualenv.pypa.io/en/stable/)
 3. Ative o virtualenv.
 4. Instale as dependências.
 5. Instale o projeto
 6. Execute os testes.
 
 ```console
 git clone git@github.com:lffsantos/captura.git
 cd captura
 virtualenv -p python3 .venv
 source .virtualenv/bin/activate
 pip install -r requirements.txt
 python setup.py install
 py.test
```

# Como Executar:
 - Iniciar o servidor de fila rabbitMQ
 
 - Instalar Requirements e a Aplicação;  
 
        pip install -r requirements.txt  
        python setup.py install
 
 - Criar  Banco de dados da Aplicação;
    
        python core/db/database.py
 
 - Rodar Crawler e Enfileirar mensagens;  
    
    `N`: Número de links por mensagem. ex: 7  
    `queue_name`: nome da fila. ex: produtos 
    
    Opção 1:  
    
        python core/modules/crawler.py
        python core/modules/enqueuer.py -l `N` -q `queue_name`
        
    Opção 2:
        
        python flow.py -l `N` -q `queue_name`

- Rodar o Processor: (pode ser rodado em background, ele fica olhando a fila indicada esperando msg)  
    `N`: Número de workers por aplicação.   
    `queue_name`: nome da fila. ex: produtos
     
        python core/modules/processor.py -w `N` -q `queue_name`

- Rodar o Indexer:
  
        python core/modules/indexer.py

## Módulos (core/modules) 
 
### crawler.py (MultiThread) 
   - Responsável por capturar os links da url informada.  
 
### enqueuer.py (SingleProcess) 
   - Responsável por enfileirar as mensagens que precisam ter atualizada as informações título e nome  
 
### processor.py (Multiprocess)
   - Responsável por ler as mensagens da fila indicada e atualizar as informações no banco de dados.
   - Essa é uma aplicação multiprocess, pode ficar rodando em background e é possível subir quantas aplicações quiser, é possível adicionar mais maquinas e/ou mais processos para aumentar a velocidade de processamento das mensagens.
   - O processor fica olhando para a fila indicada assim que chega uma mensagem algum processo livre pega ela e consome.

### indexer.py (SingleProcess)
   - Responsável por gerar o arquivo `csv` , faz a consulta no banco de dados por todos os registros processados e indexa em uma planilha `csv`.  
   - O indexer pode ser rodado sempre que desejado, atualizar os dados da planilha. caso não tenha dados novos que tenham sido processados nada sera indexado. Mas caso o processor tenha consumido novas mensagens e atualizado informações a planilha sera atualizado com esses novos valores.  

## Configuração    
   - Configurações da aplicação estão no arquivo `default_config.yaml` e podem ser alteradas de acordo com a sua configuração local  
   
        raabbitmq_server: localhost  
        database: postgresql://postgres:123@localhost:5432/captura  
        local_file_name: products.csv  

