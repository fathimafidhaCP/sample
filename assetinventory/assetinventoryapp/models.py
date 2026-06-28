from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.username
    
User = settings.AUTH_USER_MODEL

class Asset(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('repair', 'Repair'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField()

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    item_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    threshold = models.IntegerField()

    def __str__(self):
        return self.item_type


class Assignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date_assigned = models.DateField()
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset} → {self.employee}"


class RepairTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    issue = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.asset} - {self.status}"