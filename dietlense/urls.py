"""
URL configuration for dietlense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken
from diet_app.views import SignUpView,UserProfileCreateView,UserProfileretrieveUpdateView,UserRetrieveview,FoodlogcreatelistView,FoodLogRetrieveUpdateDestroyView,SummaryView,GetdietplanViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/',ObtainAuthToken.as_view()),
    path('register/',SignUpView.as_view()),
    path("profile/",UserProfileCreateView.as_view()),
    path("profile/<int:pk>/",UserProfileretrieveUpdateView.as_view()),
    path('user/<int:pk>/',UserRetrieveview.as_view()),
    path('foodlog/',FoodlogcreatelistView.as_view()),
    path('foodlog/<int:pk>/',FoodLogRetrieveUpdateDestroyView.as_view()),
    path('summary/',SummaryView.as_view()),
    path('diet/',GetdietplanViews.as_view()),
]
