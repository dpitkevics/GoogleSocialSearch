from django.db import models
from django.contrib.auth.models import User, Group

from Jooglin.settings import MAX_EXPERIENCE


class UserExperienceLevel(models.Model):
    experience_from = models.FloatField(db_index=True)
    experience_till = models.FloatField(db_index=True)
    title = models.CharField(max_length=64)
    user_group = models.ForeignKey(Group)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'user_experience_levels'


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    photo = models.TextField()
    balance = models.FloatField(default=0)
    experience_level = models.ForeignKey(UserExperienceLevel, null=True)

    _experience = models.FloatField(default=0, db_column='experience')

    @property
    def experience(self):
        return min(self._experience, MAX_EXPERIENCE)

    class Meta:
        db_table = 'user_profiles'

    def add_balance(self, amount):
        self.balance += amount
        self.save()

    def remove_balance(self, amount):
        self.balance -= amount
        self.save()

    def add_experience(self, amount):
        if self.experience < MAX_EXPERIENCE:
            self._experience += amount
            self.save()

            self.try_level_up()

    def try_level_up(self):
        if self.experience >= self.experience_level.experience_till:
            self.level_up()

    def level_up(self):
        if self.experience == 0:
            experience_level = UserExperienceLevel.objects.get(experience_from=0)
        else:
            try:
                experience_level = UserExperienceLevel.objects.filter(experience_from__lte=self.experience,
                                                                      experience_till__gte=self.experience).order_by('-experience_from')[:1][0]
            except IndexError:
                return False

        self.experience_level = experience_level
        self.save()

        self.experience_level.user_group.user_set.add(self.user)