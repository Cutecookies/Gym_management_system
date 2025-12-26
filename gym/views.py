from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Client, Trainer, WorkoutClass, ClassRegistration


def signup(request):
    # Регистрация нового клиента
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически входим после регистрации
            return redirect('home')  # перенаправляет на главную
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

# Create views
def home(request):
    # Все занятия для расписания
    all_classes = WorkoutClass.objects.all().order_by('start_time')

    # Статистика для админа
    client_count = Client.objects.count()
    trainer_count = Trainer.objects.count()
    class_count = all_classes.count()
    has_client_profile = False

    # Для клиента: его занятия
    my_classes = []
    if request.user.is_authenticated:
        try:
            client_profile = request.user.client
            has_client_profile = True
            # Занятия клиента через ClassRegistration
            registrations = ClassRegistration.objects.filter(client=client_profile)
            my_classes = [reg.workout_class for reg in registrations]
        except Client.DoesNotExist:
            has_client_profile = False

    context = {
        'all_classes': all_classes,
        'my_classes': my_classes,
        'total_clients': client_count,       # amount clients
        'total_trainers': trainer_count,     # amount trainers
        'total_classes': class_count, # amount classes
        'has_client_profile': has_client_profile,
    }
    return render(request, 'gym/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправляет на главную после выхода


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')