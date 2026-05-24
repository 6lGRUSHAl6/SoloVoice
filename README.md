<div align="center">

# 🎙️ SoloVoice Discord Bot

**Бот для накрутки часов в войсе в Discord**

Современный Python-бот для управления голосовым каналом Discord с использованием модульной архитектуры на основе Cogs.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)

</div>

---

## 📋 Команды

| Команда | Описание | Права |
|---------|----------|-------|
| `/join <ID канала>` | Подключить бота к голосовому каналу | 🔐 Администратор |
| `/leave` | Отключить бота от голосового канала | 🔐 Администратор |
| `/info` | Показать информацию о текущем подключении | ✅ Все |

---

## 🗂️ Структура проекта

```
SoloVoice/
├── main.py                    # 🎯 Точка входа бота
├── config.py                  # ⚙️ Конфигурация и переменные окружения
├── requirements.txt           # 📦 Зависимости Python
├── env.example                # 📋 Пример конфигурации (.env)
├── .gitignore                 # 🚫 Файлы для исключения из Git
│
├── cogs/                      # 🔧 Расширения (Cogs) бота
│   ├── __init__.py
│   └── voice_commands.py      # 🎧 Команды управления голосовым каналом
│
└── utils/                     # 🛠️ Утилиты
    ├── __init__.py
    ├── voice_session.py       # 💾 Управление сессией голоса
    ├── formatting.py          # 📝 Форматирование данных
    └── checks.py              # ✔️ Проверки прав доступа
```

---

## 📁 Описание модулей

### `main.py`
Основной файл приложения. Инициализирует бота, загружает конфиги и Cogs.

### `config.py`
Управление конфигурацией и переменными окружения. Валидирует наличие необходимых переменных при старте.

### `cogs/voice_commands.py`
Cog со всеми голосовыми командами:
- Безопасное подключение к каналу
- Отслеживание состояния голоса
- Информация о сессии

### `utils/voice_session.py`
Модель данных для управления голосовой сессией бота. Хранит ID канала, время присоединения и информацию о добавившем боте.

### `utils/formatting.py`
Утилиты для форматирования данных (например, форматирование времени работы).

### `utils/checks.py`
Функции проверки прав доступа (например, проверка администратора).

---

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- pip (Python package manager)

### 1️⃣ Клонируем репозиторий
```bash
git clone https://github.com/6lGRUSHAl6/SoloVoice.git
cd SoloVoice
```

### 2️⃣ Создаём конфигурацию
```bash
cp env.example .env
```

Откройте файл `.env` и вставьте ваш Discord токен:
```env
DISCORD_TOKEN=your_discord_token_here
```

### 3️⃣ Локальный запуск

**С venv (рекомендуется):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python main.py
```

### 4️⃣ Запуск на Linux Home Server (systemd)

**Автоматический запуск при загрузке сервера:**

```bash
# 1. Перейти в папку проекта
cd /path/to/SoloVoice

# 2. Запустить скрипт установки
sudo bash setup-systemd.sh

# 3. После установки управлять ботом:
sudo systemctl start solovoice      # Запустить
sudo systemctl stop solovoice       # Остановить
sudo systemctl status solovoice     # Статус
sudo journalctl -u solovoice -f     # Логи
```

Подробные инструкции: [README_SYSTEMD.md](README_SYSTEMD.md) и [INSTALL_SYSTEMD.md](INSTALL_SYSTEMD.md)

---

## 🔑 Получение Discord токена

1. Перейдите на [discord.com/developers/applications](https://discord.com/developers/applications)
2. Нажмите **New Application** → дайте любое имя
3. Раздел **Bot** → **Add Bot** → скопируйте **Token**
4. В разделе **Bot** включите интенты:
   - ✅ `Server Members Intent`
   - ✅ `Voice States Intent` — **обязательно**
5. Раздел **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `View Channels`, `Connect`, `Speak`
6. Скопируйте ссылку → откройте в браузере → добавьте бота на сервер

> ⚠️ **Никогда не публикуйте `.env` в git!**

---

## 🔍 Как получить ID голосового канала

1. Откройте **Discord** → **Настройки** → **Расширенные**
2. Включите **Режим разработчика**
3. Правой кнопкой на голосовой канал → **Копировать ID**

---

##  Зависимости

| Пакет | Версия | Назначение |
|-------|--------|------------|
| `discord.py[voice]` | ≥ 2.3.0 | Основная библиотека бота |
| `PyNaCl` | ≥ 1.5.0 | Шифрование голосового соединения |

---

## 🐛 Решение проблем

**Бот не появляется на сервере**
→ Проверьте, что токен скопирован правильно и у бота есть нужные разрешения.

**Бот не подключается к голосовому каналу**
→ Проверьте ID канала (`/info`) и убедитесь, что у бота есть разрешение `Connect`.

**Команды не появляются в Discord**
→ Подождите до 1 минуты — slash-команды синхронизируются глобально. Можно также перезагрузить Discord (`Ctrl+R`).

**Ошибка `DISCORD_TOKEN не задана`**
→ Убедитесь, что файл `.env` существует и токен в нём без лишних пробелов и кавычек.

**Бот не запускается на Linux**
→ Проверьте логи: `sudo journalctl -u solovoice -n 100`. Обычно проблема в конфигурации `.env` или зависимостях Python.

---

## 📝 Лицензия

GPL 3.0 License

---

<div align="center">

Сделано с ❤️ by 6llgrushall6

</div>