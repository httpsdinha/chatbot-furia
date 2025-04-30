import tweepy
from dotenv import load_dotenv
import os
import time

# Carregar variáveis do arquivo .env
load_dotenv()

# Substitua pelas variáveis carregadas
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Autenticação com a API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Extrair tweets de um perfil com as hashtags #FURIACS ou #CS2
try:
    user = client.get_user(username="FURIA")
    query = f"from:{user.data.username} (#FURIACS OR #CS2)"  # Filtrar tweets com #FURIACS ou #CS2
    tweets = client.search_recent_tweets(query=query, max_results=10)

    for tweet in tweets.data:
        print(f"Data: {tweet.created_at}")
        print(f"Tweet: {tweet.text}")
        print("-" * 50)

except tweepy.errors.TooManyRequests:
    print("Limite de requisições excedido. Aguardando...")
    time.sleep(900)  # Aguarde 15 minutos antes de tentar novamente
except tweepy.errors.TweepyException as e:
    print(f"Erro ao acessar a API do Twitter: {e}")