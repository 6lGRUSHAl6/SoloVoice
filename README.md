<div align="center">

# 🎙️ Discord Voice Bot

**Бот для накрутки часов в голосовых каналах Discord**

Заходит в канал, сидит в полном муте - тихо и незаметно.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)

</div>

---

## 📋 Команды

| Команда | Описание |
|---|---|
| `/join <ID канала>` | Зайти в голосовой канал (в муте) |
| `/leave` | Выйти из голосового канала |

---

## 🗂️ Структура проекта

```
discord_voice_bot/
├── bot.py               # Основной код бота
├── Dockerfile           # Docker-образ
├── docker-compose.yml   # Compose-конфиг
├── requirements.txt     # Python-зависимости
├── .env.example         # Пример файла с токеном
└── .env                 # Ваш токен (создать вручную, не коммитить!)
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
git clone https://github.com/yourname/discord-voice-bot.git
cd discord-voice-bot

# Или просто создайте папку вручную
mkdir discord-voice-bot && cd discord-voice-bot
# и скопируйте туда все файлы проекта
```

---

### 4. Создать файл `.env` с токеном

```bash
cp .env.example .env
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

| Пакет | Версия | Назначение |
|---|---|---|
| `discord.py[voice]` | ≥ 2.3.0 | Основная библиотека бота |
| `PyNaCl` | ≥ 1.5.0 | Шифрование голосового соединения |

---

<div align="center">

Сделано с ❤️ by 6llgrushall6

</div>