from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    photo = models.TextField()
    experience = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    class Meta:
        db_table = 'user_profiles'

    def add_balance(self, amount):
        self.balance += amount
        self.save()