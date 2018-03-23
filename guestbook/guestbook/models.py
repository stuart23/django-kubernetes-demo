from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=500)
    hash = models.BinaryField(default=b'')
