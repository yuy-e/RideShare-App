from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import Driver, RideInfo, Rider
from .forms import DriverSearchForm, DriverSignUpForm, RiderForm, RiderRequestForm, SharerSearchForm, UserSignUpForm


# Create your views here.

@csrf_exempt
def accountLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return render(request, 'portal.html', {'username': username})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    
@csrf_exempt
def accountSignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            render(request, 'signup.html', {})
        else:
            return render(request, 'signup.html', {'form': form})
    return render(request, 'signup.html', {})

def accountLogout(request):
    logout(request)
    return redirect('account:login')

def accountPortal(request):
    return render(request, 'portal.html', {'username': request.user.username})

def riderEntry(request):
    return render(request, 'riderEntry.html', {'username': request.user.username})

def riderRequest(request):
    if request.method == 'POST':
        form = RiderRequestForm(data=request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.rideStatus = 'OPEN'
            ride.save()

            associatedForm = RiderForm()
            rider = associatedForm.save(commit=False)
            rider.user = request.user
            rider.rideID = ride.rideID
            rider.passengerNumber = ride.passengerNumber
            rider.ownership = 'OWNER'
            rider.save()
            messages.success(request, f'Your request has been created!')
        else:
            return render(request, 'riderRequest.html', {'username': request.user.username, 'form': form})
    return render(request, 'riderRequest.html', {'username': request.user.username})

def riderSearch(request):
    if request.method == 'POST':
        form = SharerSearchForm(data=request.POST)
        if form.is_valid():
            destination = form.cleaned_data.get("destination")
            vehicleType = form.cleaned_data.get("vehicleType")
            arriveTimeTo = form.cleaned_data.get("arriveTimeTo")
            arriveTimeFrom = form.cleaned_data.get("arriveTimeFrom")
            passengerNumber = form.cleaned_data.get("passengerNumber")
            candidates = RideInfo.objects.filter(Q(shareable='YES'), Q(rideStatus='OPEN'), Q(destination=destination), Q(vehicleType=vehicleType), Q(arriveTime__lte=arriveTimeTo), Q(arriveTime__gte=arriveTimeFrom))
            rides = []
            for candidate in candidates:
                records = Rider.objects.filter(Q(rideID=candidate.rideID), Q(user=request.user))
                if len(records) == 0:
                    rides.append(candidate)
            return render(request, 'riderSearchResult.html', {'rides': rides, 'passengerNumber': passengerNumber, 'username': request.user.username})
        else:
            return render(request, 'riderSearch.html', {'username': request.user.username, 'form': form})
    return render(request, 'riderSearch.html', {'username': request.user.username})
    
def riderRides(request):
    records = Rider.objects.filter(user=request.user)
    nonCompletedRides = []
    for record in records:
        ride = RideInfo.objects.get(rideID=record.rideID)
        if ride.rideStatus != 'COMPLETED':
            nonCompletedRides.append(ride)
    return render(request, 'riderRides.html', {'username': request.user.username, 'rides': nonCompletedRides, 'records': records})

def driverEntry(request):
    driver = Driver.objects.filter(user=request.user)
    if len(driver) > 0:
        return render(request, 'driverSearch.html', {'username': request.user.username})
    else:
        return render(request, 'driverSignup.html', {'username': request.user.username})

def driverSignup(request):
    if request.method == 'POST':
        form = DriverSignUpForm(data=request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            return render(request, 'driverSearch.html', {'username': request.user.username})
        else:
            return render(request, 'driverSignup.html', {'username': request.user.username, 'form': form})
    return render(request, 'driverSignup.html', {'username': request.user.username})

def driverUpdate(request):
    driver = Driver.objects.get(user=request.user)
    if request.method == 'POST':
        form = DriverSignUpForm(data=request.POST)
        if form.is_valid():
            driver.firstname = form.cleaned_data.get("firstname")
            driver.lastname = form.cleaned_data.get("lastname")
            driver.vehicleType = form.cleaned_data.get("vehicleType")
            driver.licenseNumber = form.cleaned_data.get("licenseNumber")
            driver.capacity = form.cleaned_data.get("capacity")
            driver.save()
            messages.success(request, f'Your account has been updated!')
        else:
            return render(request, 'driverProfile.html', {'username': request.user.username, 'driver': driver, 'form': form})
    return render(request, 'driverProfile.html', {'username': request.user.username, 'driver': driver})

def rideEdit(request, rideID):
    ride = RideInfo.objects.get(rideID=rideID)
    rider = Rider.objects.get(Q(rideID=rideID), Q(user=request.user))
    if request.method == 'POST':
        form = RiderRequestForm(data=request.POST)
        if form.is_valid():
            updatedRide = form.save(commit=False)
            ride.destination = updatedRide.destination
            ride.arriveTime = updatedRide.arriveTime
            ride.passengerNumber = ride.passengerNumber - rider.passengerNumber + updatedRide.passengerNumber
            ride.vehicleType = updatedRide.vehicleType
            ride.shareable = updatedRide.shareable
            ride.save()

            rider.passengerNumber = updatedRide.passengerNumber
            rider.save()
            messages.success(request, f'Your request has been edited!')
        else:
            return render(request, 'rideEdit.html', {'ride': ride, 'rider': rider, 'username': request.user.username, 'form': form})
    return render(request, 'rideEdit.html', {'ride': ride, 'rider': rider, 'username': request.user.username})

def rideJoin(request, rideID, passengerNumber):
    form = RiderForm()
    rider = form.save(commit=False)
    rider.user = request.user
    rider.rideID = rideID
    rider.passengerNumber = passengerNumber
    rider.ownership = 'SHARER'
    rider.save()
    return render(request, 'riderSearch.html', {'username': request.user.username})

def driverSearch(request):
    if request.method == 'POST':
        form = DriverSearchForm(data=request.POST)
        if form.is_valid():
            destination = form.cleaned_data.get("destination")
            shareable = form.cleaned_data.get("shareable")
            arriveTimeTo = form.cleaned_data.get("arriveTimeTo")
            arriveTimeFrom = form.cleaned_data.get("arriveTimeFrom")

            driver = Driver.objects.get(user=request.user)
            vehicleType = driver.vehicleType
            capacity = driver.capacity

            candidates = RideInfo.objects.filter(Q(shareable=shareable), Q(rideStatus='OPEN'), Q(destination=destination), Q(vehicleType=vehicleType), Q(arriveTime__lte=arriveTimeTo), Q(arriveTime__gte=arriveTimeFrom), Q(passengerNumber__lte=capacity))
            rides = []
            for candidate in candidates:
                records = Rider.objects.filter(Q(rideID=candidate.rideID), Q(user=request.user))
                if len(records) == 0:
                    rides.append(candidate)
            return render(request, "driverOrders.html", {"username": request.user.username, 'rides': rides})
        else:
            render(request, 'driverSearch.html', {'username': request.user.username, 'form': form}) 
    return render(request, 'driverSearch.html', {'username': request.user.username})

def driverConfirm(request, rideID):
    ride = RideInfo.objects.get(rideID=rideID)
    driver = Driver.objects.get(user=request.user)
    ride.rideStatus = 'CONFIRMED'
    ride.driver = driver
    ride.save()

    records = Rider.objects.filter(rideID=rideID)
    for record in records:
        print(record.user.email)
        send_mail(
            'Ride Confirmation Reminder',
            'Hi. The ride you requested has been confirmed by a driver successfully. Have a good trip!',
            'Ride Sharing',
            [record.user.email],
            fail_silently=False,
        )
    return render(request, 'driverSearch.html', {'username': request.user.username})

def driverRides(request):
    driver = Driver.objects.get(user=request.user)
    records = RideInfo.objects.filter(driver=driver)
    return render(request, 'driverRides.html', {'username': request.user.username, 'rides': records})

def driverComplete(request, rideID):
    record = RideInfo.objects.get(rideID=rideID)
    record.rideStatus = 'COMPLETED'
    record.save()
    return render(request, 'driverSearch.html', {'username': request.user.username})
