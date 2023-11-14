from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due_date = models.DateField()
    assigned_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)