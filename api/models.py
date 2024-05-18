from django.db import models
from django.contrib.auth.models import User

class TrashType(models.Model):
    TYPE_CHOICES = [
        ('CAR', 'Carton'),
        ('PLA', 'Plastique'),
        ('VER', 'Verre'),
    ]

    type = models.CharField(max_length=3, choices=TYPE_CHOICES)

    def __str__(self):
        return self.type

class Trash(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(TrashType, on_delete=models.CASCADE)
    poids = models.FloatField()


    def __str__(self):
        return self.type.type

class Ramassage(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    heure = models.TimeField()
    trash = models.ManyToManyField(Trash)
    lieu = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/' , blank=True, null=True)

    def calculate_money(self, weight):
        # Replace this with your actual calculation
        return weight * 0.1

    def __str__(self):
        return self.lieu

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.nom

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    co2_preserved = models.DecimalField(max_digits=10, decimal_places=2)

    def add_money(self, amount):
        self.money += amount
        self.save()

    def __str__(self):
        return f'Balance for {self.user.username}'