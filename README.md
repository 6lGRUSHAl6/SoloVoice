<div align="center">

# 🎙️ SoloVoice Discord Bot

**Бот для накрутки часов в войсе в discord**

Современный Python-бот для управления голосовым каналом Discord с использованием модульной архитектуры на основе Cogs.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## 📋 Команды

| Команда | Описание | Права |
|---------|---------|-------|
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
├── Dockerfile                 # 🐳 Образ для Docker
├── docker-compose.yml         # 🐳 Конфигурация Docker Compose
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

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- Docker и Docker Compose (опционально)

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

**С pip:**
```bash
pip install -r requirements.txt
python main.py
```

**С venv (рекомендуется):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python main.py
```

### 4️⃣ Запуск через Docker

```bash
docker-compose up -d
```

Просмотр логов:
```bash
docker-compose logs -f
```

Остановка:
```bash
docker-compose down
```

---

## 🔑 Получение Discord токена

1. Перейдите на https://discord.com/developers/applications
2. Нажмите "New Application"
3. Перейдите в раздел "Bot" → "Add Bot"
4. Нажмите "Copy Token" под именем бота
5. Вставьте токен в файл `.env`

### Требуемые привилегии (Intents)
- ✅ Server Members Intent
- ✅ Voice States Intent

### Разрешения (Permissions)
- ✅ View Channels
- ✅ Connect
- ✅ Speak

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

## 🐛 Решение проблем

### Бот не появляется на сервере
- ✅ Проверьте, что токен скопирован правильно
- ✅ Убедитесь, что у бота есть нужные разрешения

### Бот не подключается к голосовому каналу
- ✅ Проверьте ID канала (`/info`)
- ✅ Убедитесь, что бот имеет разрешение "Connect"
- ✅ Посмотрите логи: `docker-compose logs`

### Команды не появляются
- ✅ Перезагрузите сервер Discord (Ctrl+R)
- ✅ Пересоздайте приложение в Developers Portal

---

## 📝 Лицензия

GPL 3.0 License

---

## 🤝 Автор

by 6llgrushall6

## 🗂️ Структура проекта

```
SoloVoice/
├── main.py                    # Точка входа бота
├── requirements.txt           # Зависимости Python
├── Dockerfile                 # Образ для Docker
├── docker-compose.yml         # Конфигурация Docker Compose
├── env.example                # Пример конфигурации (.env)
│
├── cogs/                      # Расширения (Cogs) бота
│   ├── __init__.py
│   └── voice_commands.py      # Команды управления голосовым каналом
│
└── utils/                     # Утилиты
    ├── __init__.py
    ├── voice_session.py       # Управление сессией голоса
    ├── formatting.py          # Форматирование данных
    └── checks.py              # Проверки прав доступа
```

---

## 🚀 Запуск через Docker (Ubuntu)

### 1. Установка Docker и Docker Compose

```bash
# Обновить пакеты
sudo apt update && sudo apt upgrade -y

# Установить зависимости
sudo apt install -y ca-certificates curl gnupg lsb-release

# Добавить официальный GPG-ключ Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Добавить репозиторий Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Добавить текущего пользователя в группу docker (чтобы не писать sudo)
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
docker compose version
```

---

### 2. Получить токен бота

1. Перейти на [discord.com/developers/applications](https://discord.com/developers/applications)
2. **New Application** → дать любое имя
3. Раздел **Bot** → **Add Bot** → скопировать **Token**
4. В разделе **Bot** включить интенты:
   - ✅ `Server Members Intent`
   - ✅ `Voice States` - **обязательно**
5. Раздел **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Connect`, `Speak`
6. Скопировать ссылку → открыть в браузере → добавить бота на сервер

---

### 3. Скачать файлы проекта

```bash
# Если используете git
git clone https://github.com/6lGRUSHAl6/SoloVoice.git
cd SoloVoice
```

---

### 4. Создать файл `.env` с токеном

```bash
cp env.example .env
nano .env
```

Вставьте ваш токен:

```env
DISCORD_TOKEN=ваш_токен_здесь
```

Сохранить: `Ctrl+O` → `Enter` → `Ctrl+X`

> ⚠️ **Никогда не публикуйте `.env` в git!

---

### 5. Собрать образ и запустить

```bash
docker compose up -d --build
```

Проверить, что бот запустился:

```bash
docker compose logs -f
```

Вы должны увидеть:

```
discord_voice_bot  | Бот запущен как YourBot#1234
discord_voice_bot  | Slash-команды синхронизированы
```

---

## 🛠️ Управление контейнером

```bash
# Посмотреть логи в реальном времени
docker compose logs -f

# Остановить бота
docker compose stop

# Запустить снова
docker compose start

# Перезапустить
docker compose restart

# Остановить и удалить контейнер
docker compose down

# Пересобрать после изменений в коде
docker compose up -d --build
```

---

## 🔍 Как получить ID голосового канала

1. Открыть **Discord** → **Настройки** → **Расширенные**
2. Включить **Режим разработчика**
3. Правой кнопкой на голосовой канал → **Копировать ID**

---

## ❓ Частые проблемы

**Бот не заходит в канал**
→ Проверьте, что у бота есть права `Connect` и `Speak` в нужном канале.

**Команды не появляются в Discord**
→ Подождите до 1 минуты после запуска - slash-команды синхронизируются глобально.

**Ошибка `DISCORD_TOKEN не задана`**
→ Убедитесь, что файл `.env` существует и токен в нём без лишних пробелов и кавычек.

**Контейнер падает сразу после старта**
→ Проверьте логи: `docker compose logs`. Скорее всего проблема в токене.

---

## 📦 Зависимости

| Что требуется | Версия/зависимость | Назначение |
|---|---|---|
| `discord.py[voice]` | ≥ 2.3.0 | Основная библиотека бота |
| `PyNaCl` | ≥ 1.5.0 | Шифрование голосового соединения |
| `uptime` | ~99.99% | Постоянный онлайн бота в войсе |

---

<div align="center">

Сделано с ❤️ by 6llgrushall6

</div>