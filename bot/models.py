from django.db import models


class UserBid(models.Model):
    name = models.CharField(
        max_length=256
    )
    surname = models.CharField(
        max_length=256
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=14
    )
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.id}---{self.name}"
