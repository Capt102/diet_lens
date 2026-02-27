from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from diet_app.serializers import UserSerializer,UserProfileSerializer,FoodLogSerializer
from diet_app.models import UserProfile,User,FoodLog
from rest_framework import permissions,authentication
from diet_app.utility_fun import daily_calorie_consumption
from diet_app.permissions import IsOwner,profileRequired
from diet_app.get_diet_plan import generate_kerala_diet_plan

# Create your views here.
class SignUpView(CreateAPIView):

    serializer_class=UserSerializer

class UserProfileCreateView(CreateAPIView):
    serializer_class=UserProfileSerializer

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        validated_data=serializer.validated_data
        """

        cal=daily_calorie_consumption(height=validated_data.get("height"),
                                      weight=validated_data.get("weight"),
                                      age=validated_data.get("age"),
                                      gender=validated_data.get("gender"),
                                      activity_level=float(validated_data.get("activity_level",1.2)),
                                      )
                                      """
        serializer.save(owner=self.request.user)

class UserProfileretrieveUpdateView(RetrieveAPIView,UpdateAPIView):
    serializer_class=UserProfileSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[profileRequired,IsOwner]
    queryset = UserProfile.objects.all()

class UserRetrieveview(RetrieveAPIView):
    serializer_class=UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]
    queryset = User.objects.all()

class FoodlogcreatelistView(CreateAPIView,ListAPIView):
    serializer_class=FoodLogSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,profileRequired]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    #queryset = FoodLog.objects.all()
    def get_queryset(self):
        return FoodLog.objects.filter(owner = self.request.user)
    
class FoodLogRetrieveUpdateDestroyView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    serializer_class=FoodLogSerializer
    queryset = FoodLog.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner,profileRequired]


from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Sum


class SummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,profileRequired]

    def get(self,request,*args,**kwargs):
        cur_date=timezone.now().date()
        qs=FoodLog.objects.filter(owner = request.user,created_at__date=cur_date)

        consumed=qs.values("calories").aggregate(total=Sum("calories"))

        meal_type_summary=qs.values("meal_type").annotate(total=Sum("calories"))


        context={"total":request.user.profile.bmr,
                 "total_consumption":consumed.get("total",0),
                 "remainig":request.user.profile.bmr - consumed.get("total",0) 
                 }

        return Response(data=context)
    
class GetdietplanViews(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,profileRequired]
    def post(self,request,*args,**kwargs):

        goal = request.data.get("goal")
        age=request.user.profile.age
        weight=request.user.profile.weight
        gender=request.user.profile.gender
        target_weight=request.data.get("target_weight")
        duration=request.data.get("duration")

        print(goal,age,weight,gender,target_weight,duration)

        result=generate_kerala_diet_plan(goal=goal,age=age,weight=weight,gender=gender,target_weight=target_weight,duration=duration)

        return Response(data=result)


    





    









