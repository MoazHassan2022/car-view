from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class View(models.Model):
    viewsCount = models.IntegerField(default=0, blank=True, null=True)


class CarModel(models.Model):
    modelText = models.CharField(max_length=2000, default="", blank=True)

    def __str__(self):
        return f"{self.modelText}"


class Sort(models.Model):
    sortText = models.CharField(max_length=2000, default="", blank=True)

    def __str__(self):
        return f"{self.sortText}"


class Comment(models.Model):
    CommentText = models.CharField(max_length=2000, default="")
    username = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"{self.CommentText}"


class Ad(models.Model):
    name = models.CharField(max_length=1000, default="", blank=True)
    carID = models.IntegerField(default=0, blank=True, null=True)
    username = models.CharField(max_length=1000, default="", blank=True)
    image = models.CharField(max_length=10485759, default="", blank=True)
    image1 = models.CharField(max_length=10485759, default="", blank=True)
    image2 = models.CharField(max_length=10485759, default="", blank=True)
    image3 = models.CharField(max_length=10485759, default="", blank=True)
    image4 = models.CharField(max_length=10485759, default="", blank=True)
    video = models.CharField(max_length=1000, default="", blank=True)
    videoID = models.CharField(max_length=50, default="", blank=True)
    date = models.CharField(max_length=100, default="", blank=True)
    country = models.CharField(max_length=50, default="", blank=True)
    mobile = models.CharField(max_length=50, default="", blank=True)
    advertiser = models.CharField(max_length=100, default="", blank=True)
    paymentWay = models.CharField(max_length=50, default="", blank=True)
    carColor = models.CharField(max_length=50, default="", blank=True)
    fuel = models.CharField(max_length=50, default="", blank=True)
    status = models.CharField(max_length=50, default="", blank=True)
    driver = models.CharField(max_length=50, default="", blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    sold = models.BooleanField(default=False, blank=True, null=True)


class Car(models.Model):
    name = models.CharField(max_length=1000, default="", blank=True)
    details = models.TextField(max_length=10485759, default="", blank=True)
    flaws = models.TextField(max_length=10485759, default="", blank=True)
    image = models.CharField(max_length=10485759, default="", blank=True)
    logo = models.CharField(max_length=10485759, default="", blank=True)
    video = models.CharField(max_length=1000, default="", blank=True)
    videoID = models.CharField(max_length=50, default="", blank=True)
    date = models.CharField(max_length=100, default="", blank=True)
    ads = models.ManyToManyField(Ad, blank=True, related_name="cars")
    motorSt = models.CharField(max_length=1000, default="", blank=True)
    commentList = models.ManyToManyField(Comment, blank=True, related_name="commentItems")
    modelText = models.CharField(max_length=2000, default="", blank=True)
    sortText = models.CharField(max_length=2000, default="", blank=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    sendingVery = models.IntegerField(default=0, blank=True, null=True)
    sendingGood = models.IntegerField(default=0, blank=True, null=True)
    sendingMed = models.IntegerField(default=0, blank=True, null=True)
    sendingBad = models.IntegerField(default=0, blank=True, null=True)
    bodyVery = models.IntegerField(default=0, blank=True, null=True)
    bodyGood = models.IntegerField(default=0, blank=True, null=True)
    bodyMed = models.IntegerField(default=0, blank=True, null=True)
    bodyBad = models.IntegerField(default=0, blank=True, null=True)
    insideVery = models.IntegerField(default=0, blank=True, null=True)
    insideGood = models.IntegerField(default=0, blank=True, null=True)
    insideMed = models.IntegerField(default=0, blank=True, null=True)
    insideBad = models.IntegerField(default=0, blank=True, null=True)
    wheelsVery = models.IntegerField(default=0, blank=True, null=True)
    wheelsGood = models.IntegerField(default=0, blank=True, null=True)
    wheelsMed = models.IntegerField(default=0, blank=True, null=True)
    wheelsBad = models.IntegerField(default=0, blank=True, null=True)
    drivingVery = models.IntegerField(default=0, blank=True, null=True)
    drivingGood = models.IntegerField(default=0, blank=True, null=True)
    drivingMed = models.IntegerField(default=0, blank=True, null=True)
    drivingBad = models.IntegerField(default=0, blank=True, null=True)
    glassVery = models.IntegerField(default=0, blank=True, null=True)
    glassGood = models.IntegerField(default=0, blank=True, null=True)
    glassMed = models.IntegerField(default=0, blank=True, null=True)
    glassBad = models.IntegerField(default=0, blank=True, null=True)
    motorVery = models.IntegerField(default=0, blank=True, null=True)
    motorGood = models.IntegerField(default=0, blank=True, null=True)
    motorMed = models.IntegerField(default=0, blank=True, null=True)
    motorBad = models.IntegerField(default=0, blank=True, null=True)
    condVery = models.IntegerField(default=0, blank=True, null=True)
    condGood = models.IntegerField(default=0, blank=True, null=True)
    condMed = models.IntegerField(default=0, blank=True, null=True)
    condBad = models.IntegerField(default=0, blank=True, null=True)
    commentVery = models.IntegerField(default=0, blank=True, null=True)
    commentGood = models.IntegerField(default=0, blank=True, null=True)
    commentMed = models.IntegerField(default=0, blank=True, null=True)
    commentBad = models.IntegerField(default=0, blank=True, null=True)
    outsideVery = models.IntegerField(default=0, blank=True, null=True)
    outsideGood = models.IntegerField(default=0, blank=True, null=True)
    outsideMed = models.IntegerField(default=0, blank=True, null=True)
    outsideBad = models.IntegerField(default=0, blank=True, null=True)
    electricVery = models.IntegerField(default=0, blank=True, null=True)
    electricGood = models.IntegerField(default=0, blank=True, null=True)
    electricMed = models.IntegerField(default=0, blank=True, null=True)
    electricBad = models.IntegerField(default=0, blank=True, null=True)
    seatVery = models.IntegerField(default=0, blank=True, null=True)
    seatGood = models.IntegerField(default=0, blank=True, null=True)
    seatMed = models.IntegerField(default=0, blank=True, null=True)
    seatBad = models.IntegerField(default=0, blank=True, null=True)
    breakVery = models.IntegerField(default=0, blank=True, null=True)
    breakGood = models.IntegerField(default=0, blank=True, null=True)
    breakMed = models.IntegerField(default=0, blank=True, null=True)
    breakBad = models.IntegerField(default=0, blank=True, null=True)
    fuelVery = models.IntegerField(default=0, blank=True, null=True)
    fuelGood = models.IntegerField(default=0, blank=True, null=True)
    fuelMed = models.IntegerField(default=0, blank=True, null=True)
    fuelBad = models.IntegerField(default=0, blank=True, null=True)
    lightVery = models.IntegerField(default=0, blank=True, null=True)
    lightGood = models.IntegerField(default=0, blank=True, null=True)
    lightMed = models.IntegerField(default=0, blank=True, null=True)
    lightBad = models.IntegerField(default=0, blank=True, null=True)
    tawgeehVery = models.IntegerField(default=0, blank=True, null=True)
    tawgeehGood = models.IntegerField(default=0, blank=True, null=True)
    tawgeehMed = models.IntegerField(default=0, blank=True, null=True)
    tawgeehBad = models.IntegerField(default=0, blank=True, null=True)
    tabreedVery = models.IntegerField(default=0, blank=True, null=True)
    tabreedGood = models.IntegerField(default=0, blank=True, null=True)
    tabreedMed = models.IntegerField(default=0, blank=True, null=True)
    tabreedBad = models.IntegerField(default=0, blank=True, null=True)
    aademVery = models.IntegerField(default=0, blank=True, null=True)
    aademGood = models.IntegerField(default=0, blank=True, null=True)
    aademMed = models.IntegerField(default=0, blank=True, null=True)
    aademBad = models.IntegerField(default=0, blank=True, null=True)
    qabedVery = models.IntegerField(default=0, blank=True, null=True)
    qabedGood = models.IntegerField(default=0, blank=True, null=True)
    qabedMed = models.IntegerField(default=0, blank=True, null=True)
    qabedBad = models.IntegerField(default=0, blank=True, null=True)
    totalEv = models.IntegerField(default=0, blank=True, null=True)


class User(AbstractUser):
    phoneNumber = models.CharField(max_length=100, default="", blank=True)
    favList = models.ManyToManyField(Car, blank=True, related_name="users")
    evaluatedCars = models.ManyToManyField(Car, blank=True, related_name="carItems")
    pic = models.CharField(max_length=10485759, default="", blank=True)
    banned = models.BooleanField(default=False, blank=True, null=True)


class FavCar(models.Model):
    name = models.CharField(max_length=1000, default="", blank=True)
    image = models.CharField(max_length=10485759, default="", blank=True)
    logo = models.CharField(max_length=10485759, default="", blank=True)
    userPic = models.CharField(max_length=10485759, default="", blank=True)
    userID = models.IntegerField(default=0, blank=True, null=True)
    username = models.CharField(max_length=1000, default="", blank=True)
    carID = models.IntegerField(default=0, blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="carLikesUsers")
    likesCount = models.IntegerField(default=0, blank=True, null=True)
    commentList = models.ManyToManyField(Comment, blank=True, related_name="favCarCommentItems")