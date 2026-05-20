import discord
from discord import app_commands
from discord.ext import commands
from dataclasses import dataclass
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class VoiceSession:
    channel_id: int
    joined_at: datetime
    added_by_mention: str


bot_started_at = discord.utils.utcnow()
voice_sessions: dict[int, VoiceSession] = {}

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


def format_uptime(duration: timedelta) -> str:
    total_minutes = max(0, int(duration.total_seconds() // 60))
    days, remainder = divmod(total_minutes, 24 * 60)
    hours, minutes = divmod(remainder, 60)
    return f"{days} дн. {hours} ч. {minutes} мин."


async def require_admin(interaction: discord.Interaction) -> bool:
    if interaction.guild is None:
        await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
        return False

    permissions = getattr(interaction.user, "guild_permissions", None)
    if permissions is not None and permissions.administrator:
        return True

    await interaction.response.send_message("❌ Только администраторы могут использовать эту команду.", ephemeral=True)
    return False


@bot.event
async def on_ready():
    await tree.sync()
    print(f"Бот запущен как {bot.user}")
    print(f"Slash-команды синхронизированы")


@bot.event
async def on_voice_state_update(member, before, after):
    if bot.user is None or member.id != bot.user.id:
        return

    if before.channel is not None and after.channel is None:
        voice_sessions.pop(member.guild.id, None)


@tree.command(name="join", description="Зайти в голосовой канал по ID")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe(channel_id="ID голосового канала")
async def join(interaction: discord.Interaction, channel_id: str):
    if not await require_admin(interaction):
        return

    await interaction.response.defer(ephemeral=True)

    try:
        channel_id_int = int(channel_id)
    except ValueError:
        await interaction.followup.send("❌ Неверный формат ID канала.", ephemeral=True)
        return

    guild = interaction.guild
    if guild is None:
        await interaction.followup.send("❌ Эта команда доступна только на сервере.", ephemeral=True)
        return

    channel = guild.get_channel(channel_id_int)

    if channel is None:
        await interaction.followup.send("❌ Канал не найден. Проверьте ID.", ephemeral=True)
        return

    if not isinstance(channel, discord.VoiceChannel):
        await interaction.followup.send("❌ Это не голосовой канал.", ephemeral=True)
        return

    try:
        if guild.voice_client is not None:
            await guild.voice_client.disconnect(force=True)

        voice_sessions.pop(guild.id, None)

        await channel.connect(self_mute=True, self_deaf=True)
        voice_sessions[guild.id] = VoiceSession(
            channel_id=channel.id,
            joined_at=discord.utils.utcnow(),
            added_by_mention=interaction.user.mention,
        )
        await interaction.followup.send(f"✅ Зашёл в канал **{channel.name}** (в муте).", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ Нет прав для входа в этот канал.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Ошибка: {e}", ephemeral=True)


@tree.command(name="leave", description="Выйти из голосового канала")
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def leave(interaction: discord.Interaction):
    if not await require_admin(interaction):
        return

    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
        return

    if guild.voice_client is None:
        voice_sessions.pop(guild.id, None)
        await interaction.response.send_message("❌ Бот не находится в голосовом канале.", ephemeral=True)
        return

    try:
        await guild.voice_client.disconnect(force=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Ошибка: {e}", ephemeral=True)
        return

    voice_sessions.pop(guild.id, None)
    await interaction.response.send_message("✅ Вышел из голосового канала.", ephemeral=True)


@tree.command(name="info", description="Показать информацию о подключении бота")
@app_commands.guild_only()
async def info(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
        return

    voice_client = guild.voice_client
    uptime = format_uptime(discord.utils.utcnow() - bot_started_at)

    embed = discord.Embed(title="Информация о боте", color=discord.Color.blurple())
    embed.add_field(name="Время работы бота", value=uptime, inline=False)

    if voice_client is None or voice_client.channel is None:
        embed.description = "Бот сейчас не находится в голосовом канале."
    else:
        session = voice_sessions.get(guild.id)
        embed.description = f"Сейчас бот находится в канале **{voice_client.channel.name}**."
        embed.add_field(
            name="Когда бот зашел в канал",
            value=discord.utils.format_dt(session.joined_at, style="F") if session is not None else "Неизвестно",
            inline=False,
        )
        embed.add_field(name="ID канала", value=str(voice_client.channel.id), inline=False)
        embed.add_field(
            name="Кто последний раз добавлял бота в канал",
            value=session.added_by_mention if session is not None else "Неизвестно",
            inline=False,
        )

    await interaction.response.send_message(embed=embed)


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения DISCORD_TOKEN не задана!")

bot.run(TOKEN)