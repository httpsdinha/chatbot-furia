import sys
import os

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import tweepy
import time
import requests
from src.config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN

class TwitterScraper:
    def __init__(self):
        # Autenticação com a API v2
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN)
        self.processed_tweet_ids = set()

    def get_new_tweets(self, username="ABalcacar", hashtags="#FURIACS OR #CS2", max_results=10):
        """Busca novos tweets de um usuário com as hashtags especificadas."""
        try:
            user = self.client.get_user(username=username)
            query = f"from:{user.data.username} ({hashtags})"
            tweets = self.client.search_recent_tweets(query=query, max_results=max_results)

            new_tweets = []
            if tweets.data:
                for tweet in tweets.data:
                    if tweet.id not in self.processed_tweet_ids:
                        self.processed_tweet_ids.add(tweet.id)
                        new_tweets.append(tweet)

            return new_tweets

        except tweepy.errors.TooManyRequests:
            print("Limite de requisições excedido. Aguardando...")
        except tweepy.errors.TweepyException as e:
            print(f"Erro ao acessar a API do Twitter: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        return []

# Instanciar o scraper
scraper = TwitterScraper()

# Loop para executar continuamente
while True:
    try:
        # Buscar novos tweets
        new_tweets = scraper.get_new_tweets()

        # Verificar se há tweets antes de iterar
        if new_tweets:
            for tweet in new_tweets:
                print(f"Data: {tweet.created_at}")
                print(f"Tweet: {tweet.text}")
                print("-" * 50)
        else:
            print("Nenhum tweet encontrado.")

    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Tentando novamente em 30 segundos...")
        time.sleep(30)  # Aguarda 30 segundos antes de tentar novamente
    except Exception as e:
        print(f"Erro inesperado: {e}")

    # Aguarda 15 segundos antes de buscar novamente
    time.sleep(15)