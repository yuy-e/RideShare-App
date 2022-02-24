from django.urls import path
from . import views

urlpatterns = [
    path('', views.accountLogin, name='login'),
    path('signup', views.accountSignup, name='signup'),
    path('logout', views.accountLogout, name='logout'),
    path('portal', views.accountPortal, name='portal'),

    path('riderentry', views.riderEntry, name='riderentry'),
    path('riderrides', views.riderRides, name='riderrides'),
    path('riderrequest', views.riderRequest, name='riderrequest'),
    path('ridersearch', views.riderSearch, name='ridersearch'),
    
    path('driverrides', views.driverRides, name='driverrides'),
    path('driverentry', views.driverEntry, name='driverentry'),
    path('driversignup', views.driverSignup, name='driversignup'),
    path('driverupdate', views.driverUpdate, name='driverupdate'),
    path('driversearch', views.driverSearch, name="driversearch"),
    path('driverconfirm/<int:rideID>', views.driverConfirm, name='driverconfirm'),
    path('drivercomplete/<int:rideID>', views.driverComplete, name='drivercomplete'),
    
    path('rideedit/<int:rideID>', views.rideEdit, name='rideedit'),
    path('ridejoin/<int:rideID>/<int:passengerNumber>', views.rideJoin, name='ridejoin')
]
