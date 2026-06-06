#!/bin/bash

# Скрипт автоматической установки SoloVoice с systemd
# Использование: sudo bash setup-systemd.sh

set -e

echo "🚀 Установка SoloVoice Discord Bot..."

# ─── Проверка прав ────────────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
   echo "❌ Запустите скрипт с правами root:"
   echo "   sudo bash setup-systemd.sh"
   exit 1
fi

# ─── Проверка что мы в папке проекта ─────────────────────────────────────────
if [ ! -f "main.py" ]; then
    echo "❌ Файл main.py не найден."
    echo "   Запустите скрипт из папки SoloVoice:"
    echo "   cd /path/to/SoloVoice && sudo bash setup-systemd.sh"
    exit 1
fi

# ─── Шаг 1: Системные зависимости ────────────────────────────────────────────
echo ""
echo "📦 [1/8] Установка системных зависимостей..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv libopus0 libffi-dev git

# ─── Шаг 2: Пользователь solovoice ───────────────────────────────────────────
echo "👤 [2/8] Создание системного пользователя..."
if ! id "solovoice" &>/dev/null; then
    useradd -r -s /bin/false -d /opt/solovoice solovoice
    echo "   ✅ Пользователь solovoice создан"
else
    echo "   ℹ️  Пользователь solovoice уже существует"
fi

# ─── Шаг 3: Директория ───────────────────────────────────────────────────────
echo "📁 [3/8] Подготовка директории /opt/solovoice..."
mkdir -p /opt/solovoice
chown solovoice:solovoice /opt/solovoice
chmod 750 /opt/solovoice

# ─── Шаг 4: Копирование файлов ───────────────────────────────────────────────
echo "📋 [4/8] Копирование файлов проекта..."
rsync -a --exclude='.git' --exclude='venv' --exclude='__pycache__' . /opt/solovoice/
chown -R solovoice:solovoice /opt/solovoice

# Инициализируем git в /opt/solovoice для будущих git pull
if [ ! -d "/opt/solovoice/.git" ]; then
    cd /opt/solovoice
    sudo -u solovoice git init -q
    # Получаем remote origin из исходной папки
    ORIGIN=$(git -C "$(dirname "$0")" remote get-url origin 2>/dev/null || echo "")
    if [ -n "$ORIGIN" ]; then
        sudo -u solovoice git remote add origin "$ORIGIN"
        sudo -u solovoice git fetch -q origin
        sudo -u solovoice git checkout -q -b main --track origin/main 2>/dev/null || true
        echo "   ✅ Git репозиторий настроен (origin: $ORIGIN)"
    fi
    cd - > /dev/null
fi

# ─── Шаг 5: Python окружение ─────────────────────────────────────────────────
echo "🐍 [5/8] Создание Python окружения..."
sudo -u solovoice bash << EOF
cd /opt/solovoice
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
deactivate
EOF
echo "   ✅ Зависимости установлены"

# ─── Шаг 6: .env файл ────────────────────────────────────────────────────────
echo "🔑 [6/8] Настройка конфигурации..."
if [ ! -f "/opt/solovoice/.env" ]; then
    if [ -f ".env" ]; then
        cp .env /opt/solovoice/.env
        echo "   ✅ Файл .env скопирован"
    else
        echo "   ⚠️  Файл .env не найден — создайте его вручную после установки:"
        echo "      sudo nano /opt/solovoice/.env"
        echo "      Содержимое: DISCORD_TOKEN=ваш_токен"
        # Создаём пустой чтобы не сломать chown ниже
        echo "DISCORD_TOKEN=" > /opt/solovoice/.env
    fi
fi
chmod 600 /opt/solovoice/.env
chown solovoice:solovoice /opt/solovoice/.env

# ─── Шаг 7: systemd сервис ───────────────────────────────────────────────────
echo "⚙️  [7/8] Установка systemd сервиса..."
if [ ! -f "solovoice.service" ]; then
    echo "❌ Файл solovoice.service не найден в папке проекта!"
    exit 1
fi
cp solovoice.service /etc/systemd/system/solovoice.service
chmod 644 /etc/systemd/system/solovoice.service
systemctl daemon-reload
systemctl enable solovoice
echo "   ✅ Сервис зарегистрирован и включён в автозапуск"

# ─── Шаг 8: Финальная проверка ───────────────────────────────────────────────
echo "🔍 [8/8] Проверка установки..."

PROBLEMS=0

if [ ! -f "/opt/solovoice/main.py" ]; then
    echo "   ❌ main.py не найден в /opt/solovoice"
    PROBLEMS=1
fi

if [ ! -f "/opt/solovoice/venv/bin/python" ]; then
    echo "   ❌ Python окружение не создано"
    PROBLEMS=1
fi

TOKEN=$(grep "DISCORD_TOKEN" /opt/solovoice/.env | cut -d'=' -f2)
if [ -z "$TOKEN" ] || [ "$TOKEN" = "ваш_токен" ]; then
    echo "   ⚠️  DISCORD_TOKEN не задан в .env"
    PROBLEMS=1
fi

if [ $PROBLEMS -eq 0 ]; then
    echo "   ✅ Всё в порядке"
fi

# ─── Итог ─────────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════════"

if [ $PROBLEMS -eq 0 ]; then
    echo "✅ Установка завершена успешно!"
    echo ""
    echo "Запустите бота:"
    echo "   sudo systemctl start solovoice"
else
    echo "⚠️  Установка завершена с предупреждениями. Исправьте проблемы выше,"
    echo "   затем запустите бота:"
    echo "   sudo systemctl start solovoice"
fi

echo ""
echo "Полезные команды:"
echo "   sudo systemctl start solovoice       # запустить"
echo "   sudo systemctl stop solovoice        # остановить"
echo "   sudo systemctl restart solovoice     # перезапустить"
echo "   sudo systemctl status solovoice      # статус"
echo "   sudo journalctl -u solovoice -f      # логи в реальном времени"
echo "   sudo git -C /opt/solovoice pull      # обновить код с GitHub"
echo "══════════════════════════════════════════════════════════════"