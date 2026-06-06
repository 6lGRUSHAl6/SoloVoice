"""
Cog с командами управления голосовым каналом бота.
"""

import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from utils.voice_session import VoiceSession
from utils.formatting import format_uptime
from utils.checks import require_admin


class VoiceCommandsCog(commands.Cog):
    """Команды для управления голосовым подключением бота."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reconnect_attempt_count = {}  # Track reconnection attempts per guild

    async def connect_to_channel_safe(self, channel: discord.VoiceChannel, max_retries: int = 3) -> bool:
        """
        Безопасное подключение к голосовому каналу с повторными попытками.
        
        Args:
            channel: Голосовой канал для подключения
            max_retries: Максимальное количество попыток подключения
            
        Returns:
            True если подключение успешно, False иначе
        """
        guild = channel.guild
        
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[VOICE] Попытка подключения {attempt}/{max_retries} к каналу {channel.name} (ID: {channel.id})")
                
                # Подключаемся с явным reconnect=True
                voice_client = await channel.connect(
                    self_mute=True, 
                    self_deaf=False,
                    reconnect=True,
                    timeout=15.0  # Timeout для соединения
                )
                
                print(f"[VOICE] ✅ Успешно подключились к каналу {channel.name}")
                return True
                
            except asyncio.TimeoutError:
                print(f"[VOICE] ⚠️  Timeout при попытке {attempt}/{max_retries}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)  # Экспоненциальная задержка
                    
            except discord.ClientException as e:
                print(f"[VOICE] ❌ Client ошибка при попытке {attempt}: {e}")
                if "already connected" in str(e).lower():
                    return True  # Уже подключены
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
                    
            except Exception as e:
                print(f"[VOICE] ❌ Ошибка при попытке {attempt}: {type(e).__name__}: {e}")
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)
        
        print(f"[VOICE] ❌ Не удалось подключиться после {max_retries} попыток")
        return False

    async def _attempt_reconnect(self, guild: discord.Guild, session: VoiceSession, delay: float):
        """
        Попытка переподключения к каналу после разрыва соединения.
        Сохраняет оригинальное время подключения (joined_at).
        
        Args:
            guild: Гильдия где нужно переподключиться
            session: Текущая голосовая сессия
            delay: Задержка перед попыткой переподключения в секундах
        """
        try:
            # Ждем перед переподключением
            await asyncio.sleep(delay)
            
            # Проверяем, не переподключились ли уже
            if guild.voice_client is not None and guild.voice_client.channel is not None:
                print(f"[VOICE] ✅ Бот уже переподключился к {guild.voice_client.channel.name}")
                session.reconnect_attempts = 0  # Сбрасываем счетчик попыток
                return
            
            # Получаем канал из сессии
            channel = guild.get_channel(session.channel_id)
            if channel is None:
                print(f"[VOICE] ❌ Канал {session.channel_id} не найден в гильдии {guild.id}")
                return
            
            if not isinstance(channel, discord.VoiceChannel):
                print(f"[VOICE] ❌ Канал {session.channel_id} не является голосовым каналом")
                return
            
            # Пытаемся переподключиться
            print(f"[VOICE] Переподключаюсь к каналу {channel.name}...")
            if await self.connect_to_channel_safe(channel, max_retries=3):
                print(f"[VOICE] ✅ Успешно переподключились к каналу {channel.name}!")
                print(f"[VOICE] ⏱️  Оригинальное время подключения сохранено: {session.joined_at}")
                session.reconnect_attempts = 0  # Сбрасываем счетчик попыток
            else:
                print(f"[VOICE] ❌ Не удалось переподключиться после разрыва")
                # Если превысили максимум попыток, удаляем сессию
                if session.reconnect_attempts >= 5:
                    print(f"[VOICE] Удаляю сессию после {session.reconnect_attempts} неудачных попыток")
                    self.bot.voice_sessions.pop(guild.id, None)
                    
        except Exception as e:
            print(f"[VOICE] ❌ Ошибка при переподключении: {type(e).__name__}: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        """Отслеживать изменения состояния голоса бота."""
        
        # Проверяем что это именно бот
        if self.bot.user is None or member.id != self.bot.user.id:
            return

        # Логирование для отладки
        print(f"[VOICE] Bot voice state changed: {before.channel} → {after.channel}")

        # Если бот вышел из канала
        if before.channel is not None and after.channel is None:
            session = self.bot.voice_sessions.get(member.guild.id)
            
            # Если это постоянная сессия (бот был явно добавлен через /join), пытаемся переподключиться
            if session is not None and session.is_persistent:
                print(f"[VOICE] ⚠️  Разрыв соединения в гильдии {member.guild.id}. Отмечаю и подготавливаюсь к переподключению...")
                session.mark_disconnect()
                
                # Планируем переподключение через 2-5 секунд (с экспоненциальной задержкой)
                delay = min(2 ** session.reconnect_attempts, 30)
                print(f"[VOICE] Переподключение через {delay}с (попытка {session.reconnect_attempts})")
                
                # Запускаем задачу переподключения в фоне
                asyncio.create_task(self._attempt_reconnect(member.guild, session, delay))
            else:
                # Явный выход (через /leave) или нет сессии
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
                try:
                    await guild.voice_client.disconnect(force=True)
                    await asyncio.sleep(0.5)  # Небольшая задержка перед новым подключением
                except Exception as e:
                    print(f"[VOICE] Ошибка при отключении от старого канала: {e}")

            # Удаляем старую сессию
            self.bot.voice_sessions.pop(guild.id, None)

            # Подключаемся к каналу с повторными попытками
            if await self.connect_to_channel_safe(channel, max_retries=3):
                # Создаем новую сессию
                self.bot.voice_sessions[guild.id] = VoiceSession(
                    channel_id=channel.id,
                    joined_at=discord.utils.utcnow(),
                    added_by_mention=interaction.user.mention,
                )
                
                print(f"[VOICE] Bot joined channel {channel.id} in guild {guild.id}")
                await interaction.edit_original_response(content=f"✅ Зашёл в канал **{channel.name}** (в муте, слушаю).")
            else:
                await interaction.edit_original_response(content="❌ Не удалось подключиться к каналу. Проверьте соединение сервера с Discord.")
            
        except discord.Forbidden:
            await interaction.edit_original_response(content="❌ Нет прав для входа в этот канал.")
        except Exception as e:
            print(f"[VOICE] Необработанная ошибка в /join: {e}")
            await interaction.edit_original_response(content=f"❌ Ошибка: {e}")

    @app_commands.command(name="justjoin", description="Зайти в голосовой канал вместе с вами")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def justjoin(self, interaction: discord.Interaction):
        """Подключить бота к каналу, в котором сейчас находится пользователь."""

        if not await require_admin(interaction):
            return

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ Эта команда доступна только на сервере.", ephemeral=True)
            return

        # Проверяем, что пользователь сейчас в войсе
        member = interaction.user
        if not isinstance(member, discord.Member) or member.voice is None or member.voice.channel is None:
            await interaction.response.send_message("❌ Зайдите сначала в войс.", ephemeral=True)
            return

        channel = member.voice.channel

        if not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("❌ Поддерживаются только обычные голосовые каналы.", ephemeral=True)
            return

        await interaction.response.send_message("⏳ Подключаюсь...", ephemeral=True)

        try:
            # Отключаемся от старого канала если были там
            if guild.voice_client is not None:
                try:
                    await guild.voice_client.disconnect(force=True)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"[VOICE] Ошибка при отключении от старого канала: {e}")

            # Удаляем старую сессию
            self.bot.voice_sessions.pop(guild.id, None)

            # Подключаемся к каналу пользователя
            if await self.connect_to_channel_safe(channel, max_retries=3):
                self.bot.voice_sessions[guild.id] = VoiceSession(
                    channel_id=channel.id,
                    joined_at=discord.utils.utcnow(),
                    added_by_mention=interaction.user.mention,
                    is_persistent=True,
                )

                print(f"[VOICE] Bot justjoined channel {channel.id} in guild {guild.id}")
                await interaction.edit_original_response(content=f"✅ Зашёл в канал **{channel.name}** (в муте, слушаю).")
            else:
                await interaction.edit_original_response(content="❌ Не удалось подключиться к каналу. Проверьте соединение сервера с Discord.")

        except discord.Forbidden:
            await interaction.edit_original_response(content="❌ Нет прав для входа в этот канал.")
        except Exception as e:
            print(f"[VOICE] Необработанная ошибка в /justjoin: {e}")
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
            # Отмечаем сессию как не постоянную перед отключением
            session = self.bot.voice_sessions.get(guild.id)
            if session is not None:
                session.is_persistent = False  # Явное отключение, а не разрыв
            
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