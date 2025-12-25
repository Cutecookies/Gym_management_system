from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv
import json

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
    writer.writerow(['ID', 'ФИО', 'Телефон', 'Дата рождения', 'Email', 'Специализация'])
    for trainer in trainers:
        writer.writerow([
            trainer.id,
            f"{trainer.user.first_name} {trainer.user.last_name}",
            trainer.phone,
            trainer.birth_date,
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
            'birth_date': str(trainer.birth_date),
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

# Настройка админки для каждой модели
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date']
    actions = [export_all_clients_csv, export_all_clients_json]  # ← наши действия!

class TrainerAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience']
    actions = [export_all_trainers_csv]

class WorkoutClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'workout_type', 'trainer', 'start_time']
    actions = [export_all_classes_csv]

# Register models
admin.site.register(Client, ClientAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(MembershipType)
admin.site.register(ClientMembership)
admin.site.register(WorkoutType)
admin.site.register(WorkoutClass, WorkoutClassAdmin)
admin.site.register(ClassRegistration)
admin.site.register(Visit)
admin.site.register(Payment)