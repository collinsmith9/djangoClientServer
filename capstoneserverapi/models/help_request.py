from django.db import models

class HelpRequest(models.Model):
    user = models.ForeignKey("CodeUser", on_delete=models.CASCADE)
    employee = models.ForeignKey("CodeUser", on_delete=models.CASCADE, related_name="employee")
    problemDescription = models.CharField(max_length=150)
    problem = models.CharField(max_length=150)