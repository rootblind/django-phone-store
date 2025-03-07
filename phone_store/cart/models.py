from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payment', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateTimeField()
    payment_value = models.FloatField()

    def __str__(self):
        return f"{self.first_name}_{self.last_name}"