from django.db import models


from django.db import models

class Test(models.Model):
    content = models.CharField(max_length=255,default ="")
    objects = models.Manager()


class weathers(models.Model):
    City=models.CharField(max_length=20)
    Date =models.CharField(max_length=20)
    Weather=models.CharField(max_length=80)
    Teap=models.CharField(max_length=40)
    objects=models.Manager
class dontai(models.Model):
    title=models.CharField(max_length=50)
    url=models.CharField(max_length=80)
    img=models.CharField(max_length=80)
    author=models.CharField(max_length=80)
    summary=models.CharField(max_length=80)
    content=models.CharField(max_length=80)

