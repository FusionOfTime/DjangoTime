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