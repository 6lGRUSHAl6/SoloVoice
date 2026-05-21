import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Инициализация интентов
intents = discord.Intents.default()
intents.voice_states = True

# Инициализация бота
bot = commands.Bot(command_prefix="!", intents=intents)

# Глобальное состояние бота
bot.bot_started_at = discord.utils.utcnow()
bot.voice_sessions: dict[int, any] = {}


async def load_cogs():
    """Загрузить все Cogs из папки cogs."""
    try:
        await bot.load_extension("cogs.voice_commands")
        print("✅ Cog 'voice_commands' загружен")
    except Exception as e:
        print(f"❌ Ошибка при загрузке cogs: {e}")


@bot.event
async def on_ready():
    """Событие готовности бота."""
    await bot.tree.sync()
    print(f"✅ Бот запущен как {bot.user}")
    print(f"✅ Slash-команды синхронизированы")
    print(f"✅ Время запуска: {bot.bot_started_at}")


async def setup_hook():
    """Загрузить все Cogs при запуске."""
    await load_cogs()


bot.setup_hook = setup_hook


# Получение токена и запуск бота
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения DISCORD_TOKEN не задана!")

bot.run(TOKEN)


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения DISCORD_TOKEN не задана!")

bot.run(TOKEN)