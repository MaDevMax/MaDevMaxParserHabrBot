"""
MaDevMax Notifier Bot
Author: MaDevMax (Matveichuk Maxim)
GitHub: https://github.com/MaDevMax
Year: 2025
"""

import requests
from bs4 import BeautifulSoup
import telebot
import asyncio
import time

# === Основные настройки ===
TOKEN = "YOUR_TOKEN_HERE"   # токен от @BotFather
ADMIN_ID = 123456789        # твой Telegram ID (@userinfobot -> Your Telegram ID)
CHECK_INTERVAL = 600        # раз в 10 минут проверяет новости

bot = telebot.TeleBot(TOKEN)
HABR_URL = "https://habr.com/ru/news/"

# Память — кто подписан и какие новости уже были
subscribers = set()
latest_titles = set()


# === Функция парсинга новостей ===
def get_habr_news(limit=5):
    """Парсит последние новости с Habr."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MaDevMaxParser/1.0)"}
    response = requests.get(HABR_URL, headers=headers)

    if response.status_code != 200:
        print(f"[LOG] Ошибка запроса ({response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_blocks = soup.find_all("a", class_="tm-title__link", limit=limit)

    news_list = []
    for item in news_blocks:
        title = item.text.strip()
        link = "https://habr.com" + item["href"]
        news_list.append((title, link))

    return news_list


# === Команда /start ===
@bot.message_handler(commands=['start'])
def start_cmd(message):
    """Регистрация нового подписчика"""
    subscribers.add(message.chat.id)
    msg = (
        f"👋 Привет, {message.from_user.first_name or 'друг'}!\n\n"
        "Я — MaDevMax Parser Bot 🚀.\n"
        "Следи за последними IT‑новостями с Habr.\n\n"
        "📄 /news — свежие публикации\n"
        "🕓 Авто‑рассылка — каждые 10 минут\n"
        "ℹ️ /help — справка\n"
    )
    bot.send_message(message.chat.id, msg)
    print(f"[LOG] Новый пользователь: {message.chat.id}")


# === Команда /help ===
@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = (
        "💡 Краткая справка:\n"
        "/news — показать последние 5 новостей с Habr.\n"
        "🕓 Новые новости приходят автоматически каждые 10 минут."
    )
    bot.send_message(message.chat.id, text)


# === Команда /news ===
@bot.message_handler(commands=['news'])
def news_cmd(message):
    """Показывает последние новости"""
    bot.send_message(message.chat.id, "📡 Собираю свежие новости... секундочку.")
    news = get_habr_news()
    if not news:
        bot.send_message(message.chat.id, "⚠️ Не удалось получить новости.")
        return

    text = "\n\n".join([f"🔹 {t}\n{l}" for t, l in news])
    bot.send_message(message.chat.id, text)


# === Автоматическая проверка новостей ===
async def auto_news_checker():
    global latest_titles
    while True:
        try:
            news = get_habr_news()
            new_posts = []
            for title, link in news:
                if title not in latest_titles:
                    latest_titles.add(title)
                    new_posts.append((title, link))

            if new_posts:
                feed = "\n\n".join([f"🆕 {t}\n{l}" for t, l in new_posts])
                for uid in subscribers or [ADMIN_ID]:
                    try:
                        bot.send_message(uid, f"📢 Новые статьи на Habr:\n\n{feed}")
                    except Exception as e:
                        print(f"[LOG] Ошибка отправки пользователю {uid}: {e}")

            print(f"[LOG] Проверка завершена — новых статей: {len(new_posts)}")

        except Exception as e:
            print(f"[LOG] Ошибка авто‑проверки: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


# === Главная точка запуска ===
def main():
    print("🔹 MaDevMax Parser Bot запущен и слушает Habr...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(auto_news_checker())
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
