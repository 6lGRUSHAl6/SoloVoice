# Быстрая установка SoloVoice с systemd

## ⚡ Один скрипт (самый простой способ)

```bash
# 1. Откройте терминал на сервере
# 2. Перейдите в папку проекта
cd /path/to/SoloVoice

# 3. Запустите скрипт установки (нужны права root)
sudo bash setup-systemd.sh

# 4. Готово! Бот установлен и готов к запуску
```

## 🚀 Управление ботом после установки

### Запуск/Остановка
```bash
sudo systemctl start solovoice      # Запустить
sudo systemctl stop solovoice       # Остановить
sudo systemctl restart solovoice    # Перезагрузить
```

### Просмотр логов
```bash
sudo journalctl -u solovoice -f     # Логи в реальном времени
sudo journalctl -u solovoice -n 50  # Последние 50 строк
```

### Проверка статуса
```bash
sudo systemctl status solovoice
```

## 📋 Что произойдет после установки?

✅ Бот будет **автоматически запускаться при загрузке сервера**  
✅ Если бот упадет, он **автоматически перезагрузится**  
✅ Все логи будут записаны в **journald** (просмотр через journalctl)  
✅ Бот будет запускаться от отдельного пользователя `solovoice` (безопаснее)

## 🔧 Удобные команды

Добавьте алиасы для быстрого управления:
```bash
source /opt/solovoice/solovoice-aliases.sh
```

После этого можно использовать:
```bash
solovoice-start        # Запустить
solovoice-stop         # Остановить
solovoice-restart      # Перезагрузить
solovoice-status       # Статус
solovoice-logs         # Логи (live)
solovoice-logs-tail    # Последние логи
solovoice-edit-env     # Редактировать .env
```

## 🆘 Если что-то не работает

### Бот не запускается?
```bash
# 1. Проверить логи
sudo journalctl -u solovoice -n 100

# 2. Проверить, существует ли .env файл
sudo cat /opt/solovoice/.env

# 3. Проверить права доступа
sudo ls -la /opt/solovoice/
```

### Нет DISCORD_TOKEN?
```bash
# Отредактировать .env
sudo nano /opt/solovoice/.env

# Добавить строку:
# DISCORD_TOKEN=your_token_here

# Перезагрузить бота
sudo systemctl restart solovoice
```

### Зависимости не установились?
```bash
# Переустановить зависимости вручную
sudo -u solovoice /opt/solovoice/venv/bin/pip install -r /opt/solovoice/requirements.txt
```

## 📂 Структура после установки

```
/opt/solovoice/           # Основная папка (пользователь: solovoice)
├── main.py
├── config.py
├── requirements.txt
├── .env                   # Конфиг с токеном (600 прав, только чтение)
├── cogs/
├── utils/
└── venv/                  # Python виртуальное окружение
    ├── bin/
    │   ├── python
    │   └── pip
    └── lib/

/etc/systemd/system/
└── solovoice.service     # Конфиг systemd
```

## 🔐 Безопасность

- ✅ Бот запускается от непривилегированного пользователя `solovoice`
- ✅ Файл `.env` имеет права 600 (только чтение владельцем)
- ✅ Переменные окружения не видны в `/proc`
- ✅ Логи сохраняются в journald

## 📊 Мониторинг

### Использование ресурсов
```bash
# Просмотреть процесс
ps aux | grep solovoice

# Использование памяти
top -u solovoice
```

### Проверка статуса сервиса
```bash
systemctl list-units --all | grep solovoice
```

## 🗑️ Удаление

```bash
# Если нужно удалить все
sudo systemctl stop solovoice
sudo systemctl disable solovoice
sudo rm /etc/systemd/system/solovoice.service
sudo systemctl daemon-reload
sudo rm -rf /opt/solovoice
sudo userdel solovoice
```
