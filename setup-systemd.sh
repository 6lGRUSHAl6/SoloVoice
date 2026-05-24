#!/bin/bash

# Скрипт автоматической установки SoloVoice с systemd
# Использование: sudo bash setup-systemd.sh

set -e

echo "🚀 Установка SoloVoice Discord Bot на systemd..."

# Проверка прав
if [[ $EUID -ne 0 ]]; then
   echo "❌ Скрипт должен запускаться с правами root (используйте sudo)"
   exit 1
fi

# Шаг 1: Установка зависимостей
echo "📦 Установка системных зависимостей..."
apt update
apt install -y python3 python3-pip python3-venv libopus0 libffi-dev

# Шаг 2: Создание пользователя
echo "👤 Создание пользователя solovoice..."
if ! id "solovoice" &>/dev/null; then
    useradd -r -s /bin/false -d /opt/solovoice solovoice
    echo "✅ Пользователь создан"
else
    echo "ℹ️ Пользователь уже существует"
fi

# Шаг 3: Создание директории
echo "📁 Создание директории /opt/solovoice..."
mkdir -p /opt/solovoice
chown solovoice:solovoice /opt/solovoice
chmod 750 /opt/solovoice

# Шаг 4: Копирование проекта (если запускается из папки SoloVoice)
if [ -f "main.py" ]; then
    echo "📋 Копирование файлов проекта..."
    cp -r . /opt/solovoice/
    chown -R solovoice:solovoice /opt/solovoice
    chmod 755 /opt/solovoice/main.py
fi

# Шаг 5: Создание виртуального окружения
echo "🐍 Создание виртуального окружения Python..."
sudo -u solovoice bash << EOF
cd /opt/solovoice
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
EOF

# Шаг 6: Копирование unit файла
echo "⚙️ Установка systemd сервиса..."
if [ -f "solovoice.service" ]; then
    cp solovoice.service /etc/systemd/system/
else
    echo "❌ Файл solovoice.service не найден!"
    exit 1
fi
chmod 644 /etc/systemd/system/solovoice.service

# Шаг 7: Проверка .env файла
echo "🔑 Проверка файла конфигурации..."
if [ ! -f "/opt/solovoice/.env" ]; then
    if [ -f ".env" ]; then
        cp .env /opt/solovoice/.env
    else
        echo "⚠️ Файл .env не найден. Создайте его вручную:"
        echo "   echo 'DISCORD_TOKEN=your_token' | sudo tee /opt/solovoice/.env"
    fi
fi
chmod 600 /opt/solovoice/.env
chown solovoice:solovoice /opt/solovoice/.env

# Шаг 8: Перезагрузка systemd
echo "🔄 Перезагрузка systemd..."
systemctl daemon-reload

# Шаг 9: Включение сервиса
echo "✅ Включение сервиса..."
systemctl enable solovoice

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Установка завершена!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📝 Следующие шаги:"
echo "1. Проверить .env файл:"
echo "   sudo cat /opt/solovoice/.env"
echo ""
echo "2. Запустить бота:"
echo "   sudo systemctl start solovoice"
echo ""
echo "3. Проверить статус:"
echo "   sudo systemctl status solovoice"
echo ""
echo "4. Просмотреть логи:"
echo "   sudo journalctl -u solovoice -f"
echo ""
