"""
SoloVoice - Discord Voice Bot
Бот для управления голосовыми каналами Discord.
"""

import discord
from discord.ext import commands
from config import DISCORD_TOKEN

# ============================================================================
# Инициализация интентов
# ============================================================================

intents = discord.Intents.default()
intents.voice_states = True

# ============================================================================
# Инициализация бота
# ============================================================================

bot = commands.Bot(command_prefix="!", intents=intents)

# Глобальное состояние бота
bot.bot_started_at = discord.utils.utcnow()
bot.voice_sessions: dict[int, any] = {}

# ============================================================================
# Загрузка расширений (Cogs)
# ============================================================================


async def load_cogs():
    """Загрузить все Cogs из папки cogs."""
    try:
        await bot.load_extension("cogs.voice_commands")
        print("✅ Cog 'voice_commands' загружен")
    except Exception as e:
        print(f"❌ Ошибка при загрузке cogs: {e}")


# ============================================================================
# События бота
# ============================================================================


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

# ============================================================================
# Запуск бота
# ============================================================================

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)