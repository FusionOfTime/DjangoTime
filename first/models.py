from django.db import models
from django.contrib.auth.models import User


class StringRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField()
    request_time = models.TimeField()
    input_string = models.CharField(max_length=255)
    word_count = models.IntegerField()
    char_count = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.request_date} {self.request_time}"
class StudentStats(models.Model):
    DoesNotExist = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hp = models.IntegerField(default=10)
    iq = models.IntegerField(default=10)
    happiness = models.IntegerField(default=10)
    last_update = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - HP: {self.hp}, IQ: {self.iq}, Happiness: {self.happiness}"