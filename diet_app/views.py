from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from diet_app.serializers import UserSerializer

# Create your views here.
class SignUpView(CreateAPIView):

    serializer_class=UserSerializer