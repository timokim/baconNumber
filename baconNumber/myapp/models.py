from django.db import models

class BaconNumber(models.Model):
	name = models.CharField(max_length = 100)
	baconNumber = models.IntegerField()