# MaDevMax Parser Bot 🛰

Telegram‑бот, который парсит новости с [Habr](https://habr.com/ru/news/)
и присылает их прямо в Telegram.

# ⚙️ Функционал
- `/start` — подписка на авто‑новости  
- `/news` — вывод последних 5 статей  
- `/help` — подсказка  
- Авто‑рассылка каждые 10 минут

# 🧩 Технологии
Python 3.11+, pyTelegramBotAPI, requests, BeautifulSoup4

# 🚀 Запуск
1. Склонировать:
   git clone https://github.com/MaDevMax/MaDevMaxParserBot.git
   cd MaDevMaxParserBot
   
2. Установить зависимости:
pip install -r requirements.txt

3. Вставить свой TOKEN и ADMIN_ID в код.

4. Запустить:python parser_bot.py
