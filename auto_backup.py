import os
import subprocess
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def create_backup():
	# Создаёт бэкап БД
	timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
	filename = f"gym_backup_{timestamp}.sql"
	backup_path = os.path.join('backups', filename)

	os.makedirs('backups', exist_ok=True)

	db_password = os.getenv('DB_PASSWORD')

	# Формирование команды
	cmd_str = f'pg_dump -U postgres -h localhost gym_db -f "{backup_path}"'

	env = os.environ.copy()
	env['PGPASSWORD'] = db_password

	result = subprocess.run(
		cmd_str,
		shell=True,
		env=env,
		capture_output=True,
		text=True,
		encoding='cp866'
	)

	if result.returncode == 0:
		cleanup_old_backups()
		return backup_path
	else:
		# Ошибка
		return None


def cleanup_old_backups():
	"""Удаляет старые бэкапы"""
	import glob
	backups = sorted(glob.glob('backups/*.sql'), key=os.path.getmtime)

	if len(backups) > 10:
		for old_backup in backups[:-10]:
			os.remove(old_backup)
			print(f"Удалён: {os.path.basename(old_backup)}")


def start_backup_service():
	print("Папка: backups/")
	print("Каждые 15 минут")

	# Первый бэкап
	create_backup()

	# Расписание
	schedule.every(15).minutes.do(create_backup)

	while True:
		schedule.run_pending()
		time.sleep(60)

