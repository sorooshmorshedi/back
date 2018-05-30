from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    explanation = models.CharField(max_length=255, blank=True, null=True)




