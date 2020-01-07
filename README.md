# Data Engineering
Projeto exemplo de um produtor Kafka lendo dados do Twitter em tempo real com Python e um Consumidor utilizando Spark Streaming, Spark SQL e MongoDB Spark Connector. 
Projeto de análise exploratória de transações de cartões de crédito (fonte: https://www.kaggle.com/darpan25bajaj/credit-card-exploratory-data-analysis/data)

# Pasta python-twitter
# docker-compose.yml
Infra para subir os servicos necessarios para rodar o projeto, contem:
    - Zookeeper (porta 2181)
    - Kafka (porta 9092)
    - MongoDB (porta 21017)
    - MongoDB Express (porta 8081)
    
# TwitterProducer
Cria um streaming com o Twitter e envia os dados para o topico `twitter` no Kafka

# TwitterConsumer
Cria um Consumidor Kafka e inica um streaming via Spark Streaming, recebe os dados, filtra e transforma o streaming e insere no MongoDB.
Depende dos jars
mongo-spark-connector_2.11-2.4.1.jar
mongo-java-driver-3.12.0.jar 
spark-streaming-kafka-0-8_2.11:2.4.4.jar

# requirements.txt
Dependencias do Python

# Arquitetura de referência

![alt text](https://i1.wp.com/sparkbyexamples.com/wp-content/uploads/2019/03/spark-structured-streaming-kafka.png)

# Pasta CreditCardAnalisys (Em desenvolvimento)
# CreditCardAnalisys.ipynb
Notebook com a importação dos arquivos e algumas análises preliminares

# DataSets
Customer Acqusition.csv - cadastro de clientes
Repayment.csv - pagamento de fatura
spend.cvs - gasto com o cartão
