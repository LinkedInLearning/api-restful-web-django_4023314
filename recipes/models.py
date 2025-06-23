from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.order} - {self.name}"
