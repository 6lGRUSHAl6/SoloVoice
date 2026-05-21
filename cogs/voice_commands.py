"""
Cog с командами управления голосовым каналом бота.
"""

import discord
from discord import app_commands
from discord.ext import commands

from utils.voice_session import VoiceSession
from utils.formatting import format_uptime
from utils.checks import require_admin


class VoiceCommandsCog(commands.Cog):
    """Команды для управления голосовым подключением бота."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        """Отслеживать изменения состояния голоса бота."""
        
        # Проверяем что это именно бот
        if self.bot.user is None or member.id != self.bot.user.id:
            return

        # Логирование для отладки
        print(f"[VOICE] Bot voice state changed: {before.channel} → {after.channel}")

        # Если бот вышел из канала (both before and after indicate disconnection)
        if before.channel is not None and after.channel is None:
            # Удаляем сессию когда бот явно выходит
            if member.guild.id in self.bot.voice_sessions:
                print(f"[VOICE] Session deleted for guild {member.guild.id}")
                self.bot.voice_sessions.pop(member.guild.id, None)

    @app_commands.command(name="join", description="Зайти в голосовой канал по ID")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel_id="ID голосового канала")
    async def join(self, interaction: discord.Interaction, channel_id: str):
        """Подключить бота к голосовому каналу."""
        
        if not await require_admin(interaction):
            return

        try:
            channel_id_int = int(channel_id)
        except ValueError:
            await interaction.response.send_message("❌ Неверный формат ID канала.", ephemeral=True)
            return

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
            return

        channel = guild.get_channel(channel_id_int)

        if channel is None:
            await interaction.response.send_message("❌ Канал не найден. Проверьте ID.", ephemeral=True)
            return

        if not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("❌ Это не голосовой канал.", ephemeral=True)
            return

        await interaction.response.send_message("⏳ Подключаюсь...", ephemeral=True)

        try:
            # Отключаемся от старого канала если были там
            if guild.voice_client is not None:
                await guild.voice_client.disconnect(force=True)

            # Удаляем старую сессию
            self.bot.voice_sessions.pop(guild.id, None)

            # Подключаемся к новому каналу
            await channel.connect(self_mute=True, self_deaf=True)
            
            # Создаем новую сессию
            self.bot.voice_sessions[guild.id] = VoiceSession(
                channel_id=channel.id,
                joined_at=discord.utils.utcnow(),
                added_by_mention=interaction.user.mention,
            )
            
            print(f"[VOICE] Bot joined channel {channel.id} in guild {guild.id}")
            await interaction.edit_original_response(content=f"✅ Зашёл в канал **{channel.name}** (в муте).")
            
        except discord.Forbidden:
            await interaction.edit_original_response(content="❌ Нет прав для входа в этот канал.")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ Ошибка: {e}")

    @app_commands.command(name="leave", description="Выйти из голосового канала")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def leave(self, interaction: discord.Interaction):
        """Отключить бота от голосового канала."""
        
        if not await require_admin(interaction):
            return

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
            return

        if guild.voice_client is None:
            self.bot.voice_sessions.pop(guild.id, None)
            await interaction.response.send_message("❌ Бот не находится в голосовом канале.", ephemeral=True)
            return

        try:
            await guild.voice_client.disconnect(force=True)
            self.bot.voice_sessions.pop(guild.id, None)
            print(f"[VOICE] Bot left channel in guild {guild.id}")
            await interaction.response.send_message("✅ Вышел из голосового канала.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Ошибка: {e}", ephemeral=True)

    @app_commands.command(name="info", description="Показать информацию о подключении бота")
    @app_commands.guild_only()
    async def info(self, interaction: discord.Interaction):
        """Показать информацию о текущем голосовом подключении бота."""
        
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
            return

        # Получаем реальное состояние голоса (источник истины)
        voice_client = guild.voice_client
        uptime = format_uptime(discord.utils.utcnow() - self.bot.bot_started_at)

        embed = discord.Embed(title="Информация о боте", color=discord.Color.blurple())
        embed.add_field(name="Время работы бота", value=uptime, inline=False)

        # КРИТИЧЕСКАЯ ЛОГИКА: voice_client — источник истины!
        if voice_client is None or voice_client.channel is None:
            # Бот не в голосовом канале
            embed.description = "Бот сейчас не находится в голосовом канале."
            # Убираем любую остаточную сессию
            self.bot.voice_sessions.pop(guild.id, None)
        else:
            # Бот находится в канале
            embed.description = f"Сейчас бот находится в канале **{voice_client.channel.name}**."
            
            # Всегда показываем ID канала (это можно получить всегда)
            embed.add_field(name="ID канала", value=str(voice_client.channel.id), inline=False)
            
            # Пытаемся получить дополнительную информацию из сессии
            session = self.bot.voice_sessions.get(guild.id)
            
            if session is not None and session.is_valid(voice_client):
                # Сессия существует и валидна - показываем полную информацию
                embed.add_field(
                    name="Когда бот зашел в канал",
                    value=discord.utils.format_dt(session.joined_at, style="F"),
                    inline=False,
                )
                embed.add_field(
                    name="Кто последний раз добавлял бота в канал",
                    value=session.added_by_mention,
                    inline=False,
                )
            else:
                # Сессии нет или она невалидна - показываем что информация неизвестна
                # но БОТ ТОЧНО В КАНАЛЕ, так что это не ошибка
                embed.add_field(
                    name="Когда бот зашел в канал",
                    value="ℹ️ Информация недоступна (перезагрузка/восстановление)",
                    inline=False,
                )
                embed.add_field(
                    name="Кто добавлял бота в канал",
                    value="ℹ️ Информация недоступна",
                    inline=False,
                )
                
                print(f"[INFO] Session not found or invalid for guild {guild.id}, but voice_client is present")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Загрузить Cog."""
    await bot.add_cog(VoiceCommandsCog(bot))
