from django.db import models

class Satellite(models.Model):
    norad_id = models.IntegerField()
    name = models.CharField(max_length=100)
    tle_line1 = models.CharField(max_length=100)
    tle_line2 = models.CharField(max_length=100)

    def __str__(self):
        return self.name
