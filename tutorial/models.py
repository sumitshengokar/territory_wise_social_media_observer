from django.db import models
from django.utils.timezone import datetime

class Tweets(models.Model):
    tweet = models.CharField(max_length=1000)
    created_time = models.DateTimeField(default=datetime.now,blank=True)
    retweet_count = models.IntegerField()
    location= models.CharField(max_length=1000)
    source = models.CharField(max_length=1000)
    likes=models.IntegerField()
    retweeted = models.CharField(max_length=100,default=False)
    reply = models.CharField(max_length=100,default=False)

    class Meta:
        db_table = "Tweets"

