"""
Конфигурация для Discord бота.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Валидация конфигурации
if not DISCORD_TOKEN:
    raise ValueError("Переменная окружения DISCORD_TOKEN не задана!")
