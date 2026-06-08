"""
Модуль для управления голосовыми сессиями бота.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import discord


@dataclass
class VoiceSession:
    """Информация о текущей голосовой сессии бота."""
    
    channel_id: int
    joined_at: datetime
    added_by_mention: str
    is_persistent: bool = True  # Флаг: продолжать ли оставаться в канале при разрывах
    last_disconnect_time: datetime = field(default_factory=lambda: None)  # Время последнего разрыва
    reconnect_attempts: int = 0  # Количество попыток переподключения

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
    
    def get_reconnect_delay(self) -> float:
        """
        Получить задержку перед следующей попыткой переподключения.
        Задержка рассчитывается ПЕРЕД инкрементом счётчика, чтобы
        первая попытка была максимально быстрой (0.5с).
        
        Returns:
            Задержка в секундах
        """
        # attempts=0 → 0.5с, attempts=1 → 2с, attempts=2 → 4с, и т.д. до 30с
        if self.reconnect_attempts == 0:
            return 0.5
        return min(2 ** self.reconnect_attempts, 30)

    def mark_disconnect(self):
        """Отметить время разрыва соединения и увеличить счётчик попыток."""
        self.last_disconnect_time = discord.utils.utcnow()
        self.reconnect_attempts += 1