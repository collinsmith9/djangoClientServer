from django.db import models

class Post(models.Model):
    user = models.ForeignKey("CodeUser", on_delete=models.CASCADE)
    problemDescription = models.CharField(max_length=150)
    problem = models.CharField(max_length=150)
