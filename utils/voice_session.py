"""
Модуль для управления голосовыми сессиями бота.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
import discord


@dataclass
class VoiceSession:
    """Информация о текущей голосовой сессии бота."""
    
    channel_id: int
    joined_at: datetime
    added_by_mention: str

    def get_duration(self) -> timedelta:
        """Получить длительность сеанса."""
        return discord.utils.utcnow() - self.joined_at

    def is_valid(self, voice_client: discord.VoiceClient) -> bool:
        """
        Проверить, что сессия еще актуальна.
        
        Args:
            voice_client: Текущий голосовой клиент бота
            
        Returns:
            True если сессия соответствует реальному состоянию, False иначе
        """
        if voice_client is None or voice_client.channel is None:
            return False
        
        return voice_client.channel.id == self.channel_id
