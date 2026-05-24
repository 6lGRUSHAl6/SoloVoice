# Установка SoloVoice с systemd на Linux

## Шаг 1: Подготовка системы

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить зависимости
sudo apt install -y python3 python3-pip python3-venv git libopus0 libffi-dev
```

## Шаг 2: Создание пользователя и директории

```bash
# Создать пользователя solovoice (без доступа к shell)
sudo useradd -r -s /bin/false -d /opt/solovoice solovoice

# Создать директорию для проекта
sudo mkdir -p /opt/solovoice
sudo chown solovoice:solovoice /opt/solovoice
sudo chmod 750 /opt/solovoice
```

## Шаг 3: Копирование проекта

```bash
# Скопировать все файлы проекта в /opt/solovoice
# (замените на ваш способ копирования)
sudo cp -r /path/to/SoloVoice/* /opt/solovoice/
sudo chown -R solovoice:solovoice /opt/solovoice
```

## Шаг 4: Создание виртуального окружения

```bash
# Переключиться на пользователя solovoice
sudo -u solovoice bash

# Перейти в директорию проекта
cd /opt/solovoice

# Создать виртуальное окружение
python3 -m venv venv

# Активировать его
source venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Выйти из окружения
deactivate
exit
```

## Шаг 5: Настройка переменных окружения

```bash
# Создать файл .env
sudo nano /opt/solovoice/.env
```

Добавьте:
```
DISCORD_TOKEN=your_token_here
```

Сохраните (Ctrl+O, Enter, Ctrl+X).

```bash
# Установить права на .env
sudo chmod 600 /opt/solovoice/.env
sudo chown solovoice:solovoice /opt/solovoice/.env
```

## Шаг 6: Установка systemd сервиса

```bash
# Скопировать unit файл
sudo cp /opt/solovoice/solovoice.service /etc/systemd/system/

# Установить права
sudo chmod 644 /etc/systemd/system/solovoice.service

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автоматический запуск
sudo systemctl enable solovoice

# Запустить сервис
sudo systemctl start solovoice
```

## Проверка статуса

```bash
# Посмотреть статус
sudo systemctl status solovoice

# Просмотр логов в реальном времени
sudo journalctl -u solovoice -f

# Просмотр последних 50 строк логов
sudo journalctl -u solovoice -n 50
```

## Основные команды

```bash
# Запустить бота
sudo systemctl start solovoice

# Остановить бота
sudo systemctl stop solovoice

# Перезагрузить бота
sudo systemctl restart solovoice

# Отключить автозагрузку
sudo systemctl disable solovoice

# Полная переустановка (если нужно)
sudo systemctl stop solovoice
sudo systemctl disable solovoice
sudo systemctl daemon-reload
```

## Решение проблем

### Ошибка "No module named 'discord'"
```bash
# Проверить, установлены ли зависимости
sudo -u solovoice /opt/solovoice/venv/bin/pip list

# Переустановить зависимости
sudo -u solovoice /opt/solovoice/venv/bin/pip install -r /opt/solovoice/requirements.txt
```

### Ошибка "DISCORD_TOKEN not found"
```bash
# Проверить содержимое .env файла
sudo cat /opt/solovoice/.env

# Проверить права доступа
sudo ls -la /opt/solovoice/.env
```

### Ошибка при загрузке cogs
```bash
# Проверить логи подробнее
sudo journalctl -u solovoice -n 100
```

### Сервис не запускается
```bash
# Проверить синтаксис unit файла
sudo systemd-analyze verify /etc/systemd/system/solovoice.service

# Просмотреть подробные логи
sudo journalctl -u solovoice -n 50 --all
```

## Мониторинг

### Автоматический перезапуск при краше
✅ Уже включен в конфигурации (`Restart=always`, `RestartSec=10`)

### Логирование
- Логи доступны через: `sudo journalctl -u solovoice`
- Сохраняются в journald (обычно `/var/log/journal/`)

### Проверка использования ресурсов
```bash
# Просмотреть процесс бота
ps aux | grep solovoice

# Проверить использование памяти
top -u solovoice
```

## Удаление сервиса

```bash
# Остановить и отключить сервис
sudo systemctl stop solovoice
sudo systemctl disable solovoice

# Удалить unit файл
sudo rm /etc/systemd/system/solovoice.service

# Перезагрузить systemd
sudo systemctl daemon-reload

# Удалить проект и пользователя (если нужно)
sudo rm -rf /opt/solovoice
sudo userdel solovoice
```
