<div align="center">

# 🎙️ SoloVoice Discord Bot

**Бот для накрутки часов в войсе в Discord**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)

</div>

---

## 📋 Команды

| Команда | Описание | Права |
|---------|----------|-------|
| `/join <ID канала>` | Зайти в голосовой канал по ID | 🔐 Администратор |
| `/justjoin` | Зайти в канал, где сейчас находитесь вы | 🔐 Администратор |
| `/leave` | Выйти из голосового канала | 🔐 Администратор |
| `/info` | Информация о текущем подключении | ✅ Все |

> `/justjoin` удобен с телефона — не нужно вводить ID канала вручную. Просто зайдите в войс и напишите команду.

---

## 🚀 Установка на Linux сервер (рекомендуется)

### Что нужно заранее
- Linux сервер (Ubuntu 20.04+)
- Доступ по SSH с правами `sudo`
- Discord токен (см. раздел [Получение токена](#-получение-discord-токена))

### 1️⃣ Клонируем репозиторий

```bash
git clone https://github.com/6lGRUSHAl6/SoloVoice.git
cd SoloVoice
```

### 2️⃣ Создаём файл с токеном

```bash
cp env.example .env
nano .env
```

Заменяем `your_discord_token_here` на ваш реальный токен:

```env
DISCORD_TOKEN=ваш_токен_здесь
```

Сохраняем: `Ctrl+O` → `Enter` → `Ctrl+X`

### 3️⃣ Запускаем установку

```bash
sudo bash setup-systemd.sh
```

Скрипт сам установит все зависимости, создаст окружение и зарегистрирует бота как системный сервис.

### 4️⃣ Запускаем бота

```bash
sudo systemctl start solovoice
```

### 5️⃣ Проверяем что всё работает

```bash
sudo systemctl status solovoice
```

Должно быть `active (running)`. Если нет — смотрим логи:

```bash
sudo journalctl -u solovoice -f
```

---

## 🔄 Обновление бота

Когда вышла новая версия — обновить на сервере одной командой:

```bash
sudo git -C /opt/solovoice pull && sudo systemctl restart solovoice
```

> **Важно:** обновлять нужно именно в `/opt/solovoice`, а не в папке куда клонировали репозиторий. Там живёт рабочая версия бота.

---

## 🖥️ Локальный запуск (для разработки)

```bash
git clone https://github.com/6lGRUSHAl6/SoloVoice.git
cd SoloVoice

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# или
venv\Scripts\activate      # Windows

pip install -r requirements.txt

cp env.example .env
# отредактируйте .env и вставьте токен

python main.py
```

---

## 🔑 Получение Discord токена

1. Откройте [discord.com/developers/applications](https://discord.com/developers/applications)
2. Нажмите **New Application** → введите любое имя
3. Раздел **Bot** → скопируйте **Token**
4. В разделе **Bot** включите интенты:
   - ✅ `Voice States Intent` — **обязательно**
   - ✅ `Server Members Intent`
5. Раздел **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `View Channels`, `Connect`, `Speak`
6. Скопируйте ссылку → откройте в браузере → добавьте бота на сервер

> ⚠️ **Никогда не публикуйте `.env` файл и не вставляйте токен в код!**

---

## 🔍 Как получить ID голосового канала

1. Discord → **Настройки** → **Расширенные** → включить **Режим разработчика**
2. Правой кнопкой на голосовой канал → **Копировать ID**

---

## 🛠️ Управление ботом

```bash
sudo systemctl start solovoice       # запустить
sudo systemctl stop solovoice        # остановить
sudo systemctl restart solovoice     # перезапустить
sudo systemctl status solovoice      # статус
sudo journalctl -u solovoice -f      # логи в реальном времени
sudo journalctl -u solovoice -n 100  # последние 100 строк логов
```

---

## 🐛 Решение проблем

**Команды не появляются в Discord**
→ Подождите 1-2 минуты и перезапустите Discord (`Ctrl+R`). Slash-команды синхронизируются при каждом старте бота.

**Бот не подключается к голосовому каналу**
→ Проверьте что у бота есть права `Connect` и `View Channels` на сервере.

**Бот вылетает из войса**
→ Проверьте права `Speak` — без него некоторые серверы выкидывают ботов автоматически. Также проверьте качество интернет-соединения сервера.

**Ошибка `DISCORD_TOKEN не задана`**
→ Проверьте файл `/opt/solovoice/.env` — токен должен быть без пробелов и кавычек:
```bash
sudo cat /opt/solovoice/.env
```

**Бот не запускается после `git pull`**
→ Убедитесь что делаете pull в правильной папке:
```bash
sudo git -C /opt/solovoice pull
sudo systemctl restart solovoice
```

**Нужно посмотреть ошибку подробнее**
```bash
sudo journalctl -u solovoice -n 50 --no-pager
```

**Если у вас нету сервера, а бот нужен**
→ Рекомендую добавить на свой сервер уже готового бота ```https://discord.com/oauth2/authorize?client_id=1506947810208251994```

**Если проблема не решается - создайте issue с подробным описанием и логами.**
---

## 🗂️ Структура проекта

```
SoloVoice/
├── main.py                    # Точка входа бота
├── config.py                  # Конфигурация и переменные окружения
├── requirements.txt           # Зависимости Python
├── env.example                # Пример .env файла
├── setup-systemd.sh           # Скрипт установки на Linux сервер
├── solovoice.service          # systemd unit файл
│
├── cogs/
│   └── voice_commands.py      # Все голосовые команды (/join, /justjoin, /leave, /info)
│
└── utils/
    ├── voice_session.py       # Управление голосовой сессией
    ├── formatting.py          # Форматирование данных
    └── checks.py              # Проверки прав доступа
```

---

## 📦 Зависимости

| Пакет | Версия | Назначение |
|-------|--------|------------|
| `discord.py[voice]` | ≥ 2.3.0 | Основная библиотека бота |
| `PyNaCl` | ≥ 1.5.0 | Шифрование голосового соединения |
| `python-dotenv` | ≥ 1.0.0 | Чтение .env файла |

---

## 📝 Лицензия

GPL 3.0 License

---

<div align="center">

Сделано с ❤️ by 6llgrushall6

</div>