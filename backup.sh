#!/bin/bash
# Автобэкап базы данных HandshakeDealBot
# Добавьте в cron: crontab -e
# 0 */6 * * * /home/botuser/HandshakeDealBot/backup.sh

BACKUP_DIR="/home/botuser/backups"
DB_PATH="/home/botuser/HandshakeDealBot/database.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# SQLite online backup (безопасно при работающем боте)
sqlite3 "$DB_PATH" ".backup $BACKUP_DIR/database_$DATE.db"

# Удалить бэкапы старше 30 дней
find "$BACKUP_DIR" -name "database_*.db" -mtime +30 -delete

echo "Backup done: $BACKUP_DIR/database_$DATE.db"
