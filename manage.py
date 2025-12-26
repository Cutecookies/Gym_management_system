#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

def start_backup():
    # Запускает сервис бэкапов в отдельном потоке
    try:
        print("Запуск сервиса автобэкапов...")

        from auto_backup import start_backup_service

        start_backup_service()
    except ImportError as e:
        print(f"Не удалось импортировать auto_backup: {e}")
    except Exception as e:
        print(f"Ошибка в сервисе бэкапов: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        backup_thread = threading.Thread(target=start_backup, daemon=True)
        backup_thread.start()
    except KeyboardInterrupt:
        print("\nОстановлено")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
