"""
Модуль для проверок прав и разрешений.
"""

import discord


async def require_admin(interaction: discord.Interaction) -> bool:
    """
    Проверить, что пользователь является администратором сервера.
    
    Args:
        interaction: Discord взаимодействие
        
    Returns:
        True если пользователь админ, False иначе (с отправкой сообщения об ошибке)
    """
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Эта команда доступна только на сервере.",
            ephemeral=True
        )
        return False

    permissions = getattr(interaction.user, "guild_permissions", None)
    if permissions is not None and permissions.administrator:
        return True

    await interaction.response.send_message(
        "❌ Только администраторы могут использовать эту команду.",
        ephemeral=True
    )
    return False
