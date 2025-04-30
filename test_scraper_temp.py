from src.bot.scraper import get_cs_updates

if __name__ == "__main__":
    print("=== Teste do Scraper ===")
    updates = get_cs_updates()
    print(f"Tweets encontrados: {len(updates)}")
    for idx, tweet in enumerate(updates, 1):
        print(f"\nTweet #{idx}:")
        print(tweet["text"])
        print(tweet["url"])