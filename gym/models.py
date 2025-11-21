from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20)
	birth_date = models.DateField(null=True, blank=True)
	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name}"

class Trainer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20)
	specialization = models.CharField(max_length=100)
	experience = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name}"

class MembershipType(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	duration_days = models.IntegerField()
	visits_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class ClientMembership(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	remaining_visits = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.client} - {self.membership_type}"

class WorkoutType(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name

class WorkoutClass(models.Model):
	name = models.CharField(max_length=100)
	workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
	trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
	start_time = models.DateTimeField()
	duration = models.IntegerField()   # in minutes

	def __str__(self):
		return f"{self.name} ({self.start_time})"

class ClassRegistration(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	workout_class = models.ForeignKey(WorkoutClass, on_delete=models.CASCADE)
	registration_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.client} - {self.workout_class}"

class Visit(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	check_in = models.DateTimeField(default=timezone.now)
	check_out = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.client} - {self.check_in}"

class Payment(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	payment_date = models.DateTimeField(default=timezone.now)
	description = models.TextField()

	def __str__(self):
		return f"{self.client} - {self.amount}"




