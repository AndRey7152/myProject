from django.db import models

# Create your models here.
class Catalog(models.Model):
    STATUS_CHOICES = (
        (True, 'True'),
        (False, 'False')
    )

    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(choices=STATUS_CHOICES, default=False)

    def __str__(self):
        return self.title
