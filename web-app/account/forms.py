from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Driver, RideInfo, Rider


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DriverSignUpForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ['user']

class RiderRequestForm(forms.ModelForm):
    class Meta:
        model = RideInfo
        exclude = ['rideID', 'driver', 'rideStatus']

class RiderForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = "__all__"

class SharerSearchForm(forms.ModelForm):
    arriveTimeFrom = forms.DateTimeField()
    arriveTimeTo = forms.DateTimeField()

    class Meta:
        model = RideInfo
        exclude = ['rideID', 'driver', 'rideStatus', 'arriveTime', 'shareable']

class DriverSearchForm(forms.ModelForm):
    arriveTimeFrom = forms.DateTimeField()
    arriveTimeTo = forms.DateTimeField()
    
    class Meta:
        model = RideInfo
        fields = ['destination', 'shareable']