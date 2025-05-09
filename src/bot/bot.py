import sys
import os

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from src.config import TELEGRAM_TOKEN
from src.bot.scraper import TwitterScraper

# Configuração básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self):
        self.scraper = TwitterScraper()  # Instância do scraper
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        # Registra os handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("ultimos", self.get_latest_updates))
        self.application.add_handler(MessageHandler(filters.TEXT, self.echo))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mensagem de boas-vindas"""
        await update.message.reply_text(
            "🦁 FURIA CS Updates Bot\n\n"
            "Comandos disponíveis:\n"
            "/ultimos - Mostra as últimas atualizações\n"
            "/start - Mostra esta mensagem"
        )

    async def get_latest_updates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Busca e envia os últimos tweets da FURIA"""
        try:
            tweets = self.scraper.get_new_tweets()
            
            if not tweets:
                await update.message.reply_text("⚠️ Nenhum tweet recente encontrado.")
                return

            for tweet in tweets[-3:]:  # Limita a 3 tweets para não floodar
                await update.message.reply_text(
                    f"{tweet.text}\n\n"
                    f"📅 {tweet.created_at.strftime('%d/%m/%Y %H:%M')}\n"
                    f"🔗 https://twitter.com/furiagg/status/{tweet.id}"
                )
                
        except Exception as e:
            logging.error(f"Erro ao buscar tweets: {e}")
            await update.message.reply_text("❌ Erro ao buscar atualizações. Tente novamente mais tarde.")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Responde mensagens não comandos"""
        await update.message.reply_text("Use /start para ver os comandos disponíveis.")

    def run(self):
        """Inicia o bot"""
        self.application.run_polling()

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()