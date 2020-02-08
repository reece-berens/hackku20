from django.shortcuts import render
from django.http import HttpResponse

import json

from garage.models import Vehicle, Garage, GaragePass, GateCheck

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def test(request):
    return HttpResponse(status=200, content="Test for Nathan")

@csrf_exempt
def addVehicle(request):
    plate = request.GET.get("plate")
    state = request.GET.get("state")
    vin = request.GET.get("vin")

    validStates = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Foreign","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Other","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    if (state not in validStates):
        return HttpResponse(status=400, content="Bad state")
    if (len(vin) != 17):
        return HttpResponse(status=400, content="Bad VIN")
    if (len(plate) > 10):
        return HttpResponse(status=400, content="Bad plate")

    tempVehicle = Vehicle()
    tempVehicle.licensePlate = plate
    tempVehicle.licensePlateState = state
    tempVehicle.vin = vin
    tempVehicle.save()
    return HttpResponse(status=200, content="Vehicle added")

@csrf_exempt
def addGarage(request):
    print(request.GET)
    spacesStr = request.GET.get("openSpaces")
    location = request.GET.get("streetLocation")

    isLocationTaken = Garage.objects.filter(streetLocation=location).count()
    print(isLocationTaken)
    if (isLocationTaken == 1):
        return HttpResponse(status=400, content="Location taken")

    spacesInt = int(spacesStr)
    tempGarage = Garage()
    tempGarage.openSpaces = spacesInt
    tempGarage.streetLocation = location

    tempGarage.save()
    return HttpResponse(status=200, content="Garage added")

@csrf_exempt
def addGaragePass(request):
    vin = request.GET.get("vin")
    assocVehicle = Vehicle.objects.filter(vin=vin).latest('vehicleID')
    if (assocVehicle is None):
        return HttpResponse(status=400, content="Vehicle not found")
    print(assocVehicle)
    passExists = GaragePass.objects.filter(vehicleID=assocVehicle.vehicleID).count()
    if (passExists == 1):
        return HttpResponse(status=400, content="Pass given for this vehicle")
    print("Creating garage pass")
    garagePass = GaragePass()
    garagePass.vehicleID = assocVehicle
    garagePass.save()
    return HttpResponse(status=200, content="Garage pass added")

@csrf_exempt
def gateCheck(request):
    garageID = request.GET.get("garageID")
    passID = request.GET.get("passID")
    status = request.GET.get("checkStatus")
    garageIDint = 0
    passIDint = 0
    try:
        garageIDint = int(garageID)
        passIDint = int(passID)
    except:
        return HttpResponse(status=400, content="Invalid garage or pass ID")
    if (not(status == "In" or status == "Out")):
        return HttpResponse(status=400, content="Invalid status type")

    tempGarage = Garage.objects.filter(garageID=garageIDint).latest('garageID')
    if (tempGarage == 0):
        return HttpResponse(status=400, content="Garage does not exist")
    if (tempGarage.openSpaces == 0 and status != "Out"):
        return HttpResponse(status=400, content="This garage is full")

    recentCheck = 90

    recentCheck = GateCheck.objects.filter(checkedGarageID=garageID).filter(checkedPassID=passID).count()
    print(recentCheck)
    if (recentCheck == 0):
        tempGateCheck = GateCheck()
        tempGateCheck.checkedGarageID = Garage.objects.get(garageID=garageIDint)
        tempGateCheck.checkedPassID = GaragePass.objects.get(passID=passIDint)
        tempGateCheck.inOrOut = "In"
        tempGateCheck.save()

        tempGarage.openSpaces -= 1
        tempGarage.save()
        return HttpResponse(status=200, content="Car checked in")

    recentCheck = GateCheck.objects.filter(checkedGarageID=garageID).filter(checkedPassID=passID).latest('checkID')
    print(recentCheck)
    print(recentCheck.inOrOut)
    if (recentCheck == None and status == "In"):
        tempGateCheck = GateCheck()
        tempGateCheck.checkedGarageID = Garage.objects.get(garageID=garageIDint)
        tempGateCheck.checkedPassID = GaragePass.objects.get(passID=passIDint)
        tempGateCheck.inOrOut = "In"
        tempGateCheck.save()

        tempGarage.openSpaces -= 1
        tempGarage.save()
        return HttpResponse(status=200, content="Car checked in")

    if (recentCheck.inOrOut == "In" and status == "Out"):
        tempGateCheck = GateCheck()
        tempGateCheck.checkedGarageID = Garage.objects.get(garageID=garageIDint)
        tempGateCheck.checkedPassID = GaragePass.objects.get(passID=passIDint)
        tempGateCheck.inOrOut = "Out"
        tempGateCheck.save()

        tempGarage.openSpaces += 1
        tempGarage.save()
        return HttpResponse(status=200, content="Car checked out")

    if (recentCheck.inOrOut == "Out" and status == "In"):
        tempGateCheck = GateCheck()
        tempGateCheck.checkedGarageID = Garage.objects.get(garageID=garageIDint)
        tempGateCheck.checkedPassID = GaragePass.objects.get(passID=passIDint)
        tempGateCheck.inOrOut = "In"
        tempGateCheck.save()

        tempGarage.openSpaces -= 1
        tempGarage.save()
        return HttpResponse(status=200, content="Car checked in")

    return HttpResponse(status=400, content="Bad in/out and car combo")

def getOpenSpaces(request):
    location = request.GET.get("streetLocation")
    garage = Garage.objects.filter(streetLocation=location).latest('garageID')
    if (garage is None):
        return HttpResponse(status=400, content="Garage does not exist")
    return HttpResponse(status=200, content=garage.openSpaces)

def showAllGarages(request):
    garageList = Garage.objects.all()
    dictionary = {}
    for garage in garageList:
        dictionary[garage.streetLocation] = garage.openSpaces
    return HttpResponse(status=200, content=json.dumps(dictionary), content_type="application/json")

def landingPage(request):
    return render(request, 'landing.html')
