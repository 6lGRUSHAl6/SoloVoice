import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    print(f"Бот запущен как {bot.user}")
    print(f"Slash-команды синхронизированы")


@tree.command(name="join", description="Зайти в голосовой канал по ID")
@app_commands.describe(channel_id="ID голосового канала")
async def join(interaction: discord.Interaction, channel_id: str):
    await interaction.response.defer(ephemeral=True)

    try:
        channel_id_int = int(channel_id)
    except ValueError:
        await interaction.followup.send("❌ Неверный формат ID канала.", ephemeral=True)
        return

    channel = bot.get_channel(channel_id_int)

    if channel is None:
        await interaction.followup.send("❌ Канал не найден. Проверьте ID.", ephemeral=True)
        return

    if not isinstance(channel, discord.VoiceChannel):
        await interaction.followup.send("❌ Это не голосовой канал.", ephemeral=True)
        return

    # Еели уже в канале на этом сервере - отключиться сначала
    guild = interaction.guild
    if guild.voice_client is not None:
        await guild.voice_client.disconnect(force=True)

    try:
        vc = await channel.connect()
        # мут: бот не будет передавать аудио
        await guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
        await interaction.followup.send(f"✅ Зашёл в канал **{channel.name}** (в муте).", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ Нет прав для входа в этот канал.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Ошибка: {e}", ephemeral=True)


@tree.command(name="leave", description="Выйти из голосового канала")
async def leave(interaction: discord.Interaction):
    guild = interaction.guild
    if guild.voice_client is None:
        await interaction.response.send_message("❌ Бот не находится в голосовом канале.", ephemeral=True)
        return

    await guild.voice_client.disconnect(force=True)
    await interaction.response.send_message("✅ Вышел из голосового канала.", ephemeral=True)


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения DISCORD_TOKEN не задана!")

bot.run(TOKEN)