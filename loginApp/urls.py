from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"), 
	path('logout/', views.logoutUser, name="logout"), 
	path('emailsent/', views.sendEmail, name="emailsent"),
]