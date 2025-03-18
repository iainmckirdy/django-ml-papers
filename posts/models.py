from django.db import models

# Create your models here.

class Week(models.Model):
    date = models.CharField(max_length=17)

    def __str__(self):
        return f'Papers from week begining {self.date}'

class Paper(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    link = models.URLField()
    week = models.ForeignKey(Week, related_name="papers", on_delete=models.CASCADE)

    def __str__(self):
        return self.title