from django.db import models

# Create your models here.

class Distributor(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at','-updated_at')

    def __str__(self):
        return self.name