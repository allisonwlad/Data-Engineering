import sys
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars python-twitter/jars/mongo-spark-connector_2.11-2.4.1.jar,python-twitter/jars/mongo-java-driver-3.12.0.jar --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 pyspark-shell'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.streaming.kafka import KafkaUtils
import json


def empty_rdd():
    print('RDD Vazio')

## Singleton Spark (rodei local pois meu zookeeper teve problemas para gerenciar as requisicoes, mas existe um cluster stand alone spark://localhost:7077)
def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config("spark.mongodb.output.uri", 'mongodb://root:example@localhost:27017/admin') \
            .config("spark.mongodb.input.uri", 'mongodb://root:example@localhost:27017/admin') \
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

# metodo main da aplicacao
if __name__ == "__main__":
    sc = SparkContext(appName="PythonSqlNetworkWordCount")
    #batch de 10s
    ssc = StreamingContext(sc, 10)

    # inicia o stream com o Kafka no topico 'twitter'
    kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'twitterGroup', {'twitter':1})
    
    # recebe do kafka os dados e guarda o value na variave parsed ja em Json
    parsed = kafkaStream.map(lambda v: json.loads(v[1]))
    
    # Converte o RDD para Dataframe 
    def process(time, rdd):
        print("========= %s =========" % str(time))

        if(rdd.count() >0):
            try:
                # Cria o Singleton do spark 
                spark = getSparkSessionInstance(rdd.context.getConf())

                # Converte RDD[String] para um RDD[Row] e depois para um Dataframe
                tweets = rdd.map(lambda w: Row(screen_name=w['user']['screen_name'], location=w['user']['location'], text=w['text'], timestamp=str(time)))
                tweetsDF = spark.createDataFrame(tweets)

                # Cria uma view em Memoria
                tweetsDF.createOrReplaceTempView("tweets")

                # Usa o Spark Sql para manipular os dados
                query = spark.sql("select screen_name, location, text, timestamp from tweets")
                
                query.\
                    write.format('com.mongodb.spark.sql.DefaultSource').\
                    mode('append').\
                    option('database', 'twitter').\
                    option('collection','authors').\
                    save()
                
                query.show()
            
            except:
                print(sys.exc_info[0])
        else:
            empty_rdd()

    # inicia o streming 
    parsed.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()