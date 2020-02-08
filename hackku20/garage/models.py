from django.db import models

# Create your models here.

class Vehicle(models.Model):
    vehicleID = models.IntegerField(primary_key=True)
    licensePlate = models.CharField(default="", max_length=10)
    statesList = (("Alabama","Alabama"),("Alaska","Alaska"),("Arizona","Arizona"),("Arkansas","Arkansas"),("California","California"),("Colorado","Colorado"),("Connecticut","Connecticut"),("Delaware","Delaware"),("Florida","Florida"),("Foreign", "Foreign"),("Georgia","Georgia"),("Hawaii","Hawaii"),("Idaho","Idaho"),("Illinois","Illinois"),("Indiana","Indiana"),("Iowa","Iowa"),("Kansas","Kansas"),("Kentucky","Kentucky"),("Louisiana","Louisiana"),("Maine","Maine"),("Maryland","Maryland"),("Massachusetts","Massachusetts"),("Michigan","Michigan"),("Minnesota","Minnesota"),("Mississippi","Mississippi"),("Missouri","Missouri"),("Montana","Montana"),("Nebraska","Nebraska"),("Nevada","Nevada"),("New Hampshire","New Hampshire"),("New Jersey","New Jersey"),("New Mexico","New Mexico"),("New York","New York"),("North Carolina","North Carolina"),("North Dakota","North Dakota"),("Ohio","Ohio"),("Oklahoma","Oklahoma"),("Oregon","Oregon"),("Other", "Other"),("Pennsylvania","Pennsylvania"),("Rhode Island","Rhode Island"),("South Carolina","South Carolina"),("South Dakota","South Dakota"),("Tennessee","Tennessee"),("Texas","Texas"),("Utah","Utah"),("Vermont","Vermont"),("Virginia","Virginia"),("Washington","Washington"),("West Virginia","West Virginia"),("Wisconsin","Wisconsin"),("Wyoming","Wyoming"))
    licensePlateState = models.CharField(default="", choices=statesList, max_length=40)
    vin = models.CharField(default="", max_length=17)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['licensePlate', 'licensePlateState', 'vin'], name='Unique vehicle')
        ]

class Garage(models.Model):
    garageID = models.IntegerField(primary_key=True)
    openSpaces = models.IntegerField(default=100)
    streetLocation = models.CharField(default="", max_length=200, unique=True)

class GaragePass(models.Model):
    passID = models.IntegerField(primary_key=True)
    vehicleID = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class GateCheck(models.Model):
    checkID = models.IntegerField(primary_key=True)
    checkedGarageID = models.ForeignKey(Garage, on_delete=models.CASCADE)
    checkedPassID = models.ForeignKey(GaragePass, on_delete=models.CASCADE)
    inOrOut = models.CharField(default="", choices=(("In", "In"), ("Out", "Out")), max_length=3)