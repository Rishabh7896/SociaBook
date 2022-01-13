from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200)
    profilepic=models.ImageField(default='profilepic/default.jpg',upload_to='profilepic')
    userid=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    emailid=models.CharField(max_length=200)
    postct=models.IntegerField(default=0)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    logintime=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.userid)

class FndF(models.Model):
    fuserid=models.CharField(max_length=200)
    tuserid=models.CharField(max_length=200)

    def __str__(self):
        return str(self.fuserid)+"-"+str(self.tuserid)

class Post(models.Model):
    userid=models.CharField(max_length=200)
    postid=models.CharField(max_length=200)
    picture=models.ImageField(upload_to='post')
    caption=models.CharField(max_length=500)
    likecount=models.IntegerField(default=0)
    commentcount=models.IntegerField(default=0)
    datetime=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.userid)+"-"+str(self.postid)
    
class Like(models.Model):
    postid=models.CharField(max_length=200)
    userid=models.CharField(max_length=200)

    def __str__(self):
        return str(self.postid)+"-"+str(self.userid)

class Comment(models.Model):
    postid=models.CharField(max_length=200)
    userid=models.CharField(max_length=200)
    comment=models.CharField(max_length=200)

    def __str__(self):
        return str(self.postid)+"-"+str(self.userid)

class Message(models.Model):
    fuserid=models.CharField(max_length=200)
    tuserid=models.CharField(max_length=200)
    textmessage=models.CharField(max_length=500,default='NULL')
    picturemessage=models.ImageField(upload_to='message',null=True)
    audiomessage=models.FileField(null=True)
    linkmessage=models.URLField(max_length=200,default='NULL')
    datetime=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.fuserid)+"-"+str(self.tuserid)+"-"+str(self.datetime)

class online(models.Model):
    userid=models.CharField(max_length=200)

    def __str__(self):
        return str(self.userid)