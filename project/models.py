from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    create_date = models.DateField(auto_now_add=True)


class Project_Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=False)
    time = models.IntegerField(validators=[MinValueValidator(1)])
    comment = models.CharField(max_length=20, blank=True)
