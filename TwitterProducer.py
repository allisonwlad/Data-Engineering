from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

# dados da api
api_key = <api key>
api_secret= <api secret>
access_token = <api token>
secret_token = <api secret token>

# classe para envio das mensagens ao Kafka
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("twitter", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)
        
# inicia o produtor
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, secret_token)
    # inicia o stream com o twitter
    stream = Stream(auth, listener)
    # assuntos pesquisados
    stream.filter(track=['itau','bolsonaro'])
