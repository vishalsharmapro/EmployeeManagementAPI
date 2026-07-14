from django.db import models
from department.models import Department



class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo=models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True
    )