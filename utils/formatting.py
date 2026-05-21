"""
Модуль для форматирования данных.
"""

from datetime import timedelta


def format_uptime(duration: timedelta) -> str:
    """
    Форматировать длительность в читаемый вид.
    
    Args:
        duration: Временная длительность
        
    Returns:
        Строка в формате "X дн. Y ч. Z мин."
    """
    total_minutes = max(0, int(duration.total_seconds() // 60))
    days, remainder = divmod(total_minutes, 24 * 60)
    hours, minutes = divmod(remainder, 60)
    return f"{days} дн. {hours} ч. {minutes} мин."
