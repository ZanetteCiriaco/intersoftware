from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Client(models.Model):
    cpf = models.CharField(max_length=14, unique=True, validators=[MinLengthValidator(14)])
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Sales(models.Model):
    created_at = models.DateTimeField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

