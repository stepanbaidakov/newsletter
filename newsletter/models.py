from django.db import models

# Create your models here.

class Client(models.Model):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        db_table = "client"

