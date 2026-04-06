from django.db import models

# Create your models here.


class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=100)
    salary = models.IntegerField()
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.emp_id} - {self.name}"