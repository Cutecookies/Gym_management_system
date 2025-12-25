from django.shortcuts import render
from .models import Client, Trainer, WorkoutClass

# Create views
def home(request):
    # Amount entries
    context = {
        'total_clients': Client.objects.count(),       # amount clients
        'total_trainers': Trainer.objects.count(),     # amount trainers
        'total_classes': WorkoutClass.objects.count(), # amount classes
    }
    return render(request, 'gym/home.html', context)