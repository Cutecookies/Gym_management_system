from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv
import json
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

@admin.action(description="Экспортировать всех клиентов в CSV")
def export_all_clients_csv(modeladmin, request, queryset):
    clients = Client.objects.all()

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    # "attachment" = "скачать как вложение"
    # filename="clients.csv" = "сохранить под именем clients.csv"

    writer = csv.writer(response, delimiter=';')
    # writer = специальный объект для создания CSV
    writer.writerow(['ID', 'ФИО', 'Телефон', 'Дата рождения', 'Email'])
    for client in clients:
        writer.writerow([
			client.id,
			f"{client.user.first_name} {client.user.last_name}",
			client.phone,
			client.birth_date,
			client.user.email
        ])

    return response

@admin.action(description="Экспортировать всех клиентов в JSON")
def export_all_clients_json(modeladmin, request, queryset):
    clients = Client.objects.all()
    data = []
    for client in clients:
        data.append({
            'id': client.id,
            'full_name': f"{client.user.first_name} {client.user.last_name}",
            'phone': client.phone,
            'birth_date': str(client.birth_date),
            'email': client.user.email
        })

    response = HttpResponse(json.dumps(data, indent=2, ensure_ascii=False),
                            content_type='application/json; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="trainers.json"'
    return response

@admin.action(description="Экспортировать всех тренеров в CSV")
def export_all_trainers_csv(modeladmin, request, queryset):
    trainers = Trainer.objects.all()

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="trainers.csv"'

    writer = csv.writer(response, delimiter=';')
    # writer = специальный объект для создания CSV
    writer.writerow(['ID', 'ФИО', 'Телефон', 'Email', 'Специализация'])
    for trainer in trainers:
        writer.writerow([
            trainer.id,
            f"{trainer.user.first_name} {trainer.user.last_name}",
            trainer.phone,
            trainer.user.email,
            trainer.specialization
        ])

    return response

@admin.action(description="Экспортировать всех тренеров в JSON")
def export_all_trainers_json(modeladmin, request, queryset):
    trainers = Trainer.objects.all()
    data = []
    for trainer in trainers:
        data.append({
            'id': trainer.id,
            'full_name': f"{trainer.user.first_name} {trainer.user.last_name}",
            'phone': trainer.phone,
            'email': trainer.user.email,
            'specialization': trainer.specialization
        })

    response = HttpResponse(json.dumps(data, indent=2, ensure_ascii=False),
                            content_type='application/json; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="trainers.json"'
    return response

@admin.action(description="Экспортировать все классы в CSV")
def export_all_classes_csv(modeladmin, request, queryset):
    classes = WorkoutClass.objects.all()

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

    writer = csv.writer(response, delimiter=';')
    # writer = специальный объект для создания CSV
    writer.writerow(['ID', 'Название', 'Тип', 'Тренер', 'Дата и время', 'Длительность'])
    for cls in classes:
        writer.writerow([
            cls.id,
            cls.name,
            cls.workout_type.name,
            f"{cls.trainer.user.first_name} {cls.trainer.user.last_name}",
            cls.start_time,
            cls.duration
        ])

    return response

@admin.action(description="Экспортировать все классы в JSON")
def export_all_classes_json(modeladmin, request, queryset):
    classes = WorkoutClass.objects.all()
    data = []
    for cls in classes:
        data.append({
            'id': cls.id,
            'name': cls.name,
            'workout_type': cls.workout_type.name,
            'full_name': f"{cls.trainer.user.first_name} {cls.trainer.user.last_name}",
            'start_time': str(cls.start_time),
            'duration': cls.duration
        })

    response = HttpResponse(json.dumps(data, indent=2, ensure_ascii=False),
                            content_type='application/json; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="trainers.json"'
    return response


def quick_backup():
    # Создает быстрый бэкап
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/backup_{timestamp}.sql"

        os.makedirs('backups', exist_ok=True)

        cmd = f"pg_dump -U postgres gym_db > {backup_file}"
        env = os.environ.copy()
        env['PGPASSWORD'] = os.getenv('DB_PASSWORD', '')

        subprocess.run(cmd, shell=True, env=env, check=True)
        return f"Бэкап создан: {backup_file}"
    except Exception as e:
        return f"Ошибка: {e}"

@admin.action(description="Создать бэкап БД")
def backup_action(modeladmin, request, queryset):
    msg = quick_backup()
    print(msg)

# Настройка админки для каждой модели
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date']
    actions = [export_all_clients_csv, export_all_clients_json, backup_action]

class TrainerAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience']
    actions = [export_all_trainers_csv, export_all_trainers_json, backup_action]

class WorkoutClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'workout_type', 'trainer', 'start_time']
    actions = [export_all_classes_csv, export_all_classes_json, backup_action]

# Добавляем действие ко всем моделям
class BackupAdmin(admin.ModelAdmin):
    actions = [backup_action]

# Register models
admin.site.register(Client, ClientAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(MembershipType, BackupAdmin)
admin.site.register(ClientMembership, BackupAdmin)
admin.site.register(WorkoutType, BackupAdmin)
admin.site.register(WorkoutClass, WorkoutClassAdmin)
admin.site.register(ClassRegistration, BackupAdmin)
admin.site.register(Visit, BackupAdmin)
admin.site.register(Payment, BackupAdmin)