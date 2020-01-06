from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

# dados da api
api_key = 'uqdNgpJHQTXoacRwf0AxmukRU'
api_secret= 'm1EfuZIVlpixBDho6BOdpu8FhsA5dj6HVsvR9GF2u6saJa4Asl'
access_token = '1596057121-PX8LeQFivq8w1d46bsSgep2jD57PpMUTfaZLKdD'
secret_token = 'miIL7Ep4VYAPyLQmNr49H7DhSHLb5wApyAuKkI4u9LiAV'

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