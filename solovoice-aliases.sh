#!/bin/bash

# Быстрые команды для управления SoloVoice ботом

alias solovoice-start="sudo systemctl start solovoice"
alias solovoice-stop="sudo systemctl stop solovoice"
alias solovoice-restart="sudo systemctl restart solovoice"
alias solovoice-status="sudo systemctl status solovoice"
alias solovoice-logs="sudo journalctl -u solovoice -f"
alias solovoice-logs-tail="sudo journalctl -u solovoice -n 50"
alias solovoice-enable="sudo systemctl enable solovoice"
alias solovoice-disable="sudo systemctl disable solovoice"

# Функция для просмотра логов с фильтром
solovoice-logs-grep() {
    sudo journalctl -u solovoice | grep "$1"
}

# Функция для быстрого редактирования конфига
solovoice-edit-env() {
    sudo nano /opt/solovoice/.env
}

# Функция для проверки процесса
solovoice-ps() {
    ps aux | grep solovoice | grep -v grep
}

echo "✅ SoloVoice команды загружены! Доступные команды:"
echo "  solovoice-start       - Запустить бота"
echo "  solovoice-stop        - Остановить бота"
echo "  solovoice-restart     - Перезагрузить бота"
echo "  solovoice-status      - Статус бота"
echo "  solovoice-logs        - Логи в реальном времени"
echo "  solovoice-logs-tail   - Последние 50 строк логов"
echo "  solovoice-logs-grep   - Поиск в логах (используйте: solovoice-logs-grep 'ERROR')"
echo "  solovoice-edit-env    - Редактировать конфиг"
echo "  solovoice-ps          - Проверить процесс"
echo "  solovoice-enable      - Включить автозагрузку"
echo "  solovoice-disable     - Отключить автозагрузку"
