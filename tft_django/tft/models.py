from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=2)
    tag = models.CharField(max_length=5)

    def __str__(self):
        return self.name + '/' + self.tag + '/' + self.region

class Game(models.Model):
    gameID = models.CharField(max_length=20,primary_key=True)
    queue = models.CharField(max_length=10)
    placement = models.IntegerField()
    level = models.IntegerField()
    length = models.CharField(max_length=10)
    round = models.CharField(max_length=10)
    augments = models.CharField(max_length=100)
    headliner = models.CharField(max_length=20)
    traits = models.CharField(max_length=100)
    units = models.CharField(max_length=1000)

    def __str__(self):
        return self.gameID + "|" + self.units +"\n"
