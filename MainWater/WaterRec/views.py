import base64
import json
import time
from datetime import datetime
from io import BytesIO
from rest_framework.authtoken.models import Token
from django.db.models import Sum
import torch
import requests
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .serializers import ServiceRecordSerializer, ServiceRecordListSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

model = torch.hub.load(r'/home/dillag/DjangoDiplom/MainWater/WaterRec/Models/yolov5/', 'custom',
                       path=r'/home/dillag/DjangoDiplom/MainWater/WaterRec/Models/best1.pt', source='local')
model2 = torch.hub.load(r'/home/dillag/DjangoDiplom/MainWater/WaterRec/Models/yolov5/', 'custom',
                        path=r'/home/dillag/DjangoDiplom/MainWater/WaterRec/Models/best.pt', source='local')

# model2 = 'E:/yolov5-master'
# model = 'E:/yolov5-master'

for user in User.objects.all():
    a = Token.objects.get_or_create(user=user)
    print(user.username)
    print(a)


@csrf_exempt
def recievephoto(request):
    # Get image from request and decode from base64
    rawimage = request.POST.get('search')
    norawimage = base64.b64decode(rawimage)
    # Convert Image Bytes To Img
    stream = BytesIO(norawimage)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    # Predict first model
    firsttime = time.time()
    results = model(image)
    results.show()
    detect_res = results.pandas().xyxy[0]
    # Crop image with coord after first model
    cropped_image = image.crop(
        (int(detect_res['xmin']), int(detect_res['ymin']), int(detect_res['xmax']), int(detect_res['ymax'])))
    # Predict second model
    results_numbers = model2(cropped_image)
    results_numbers.show()
    # Sort result
    test_detect_res = results_numbers.pandas().xyxy[0]
    test_detect_res = test_detect_res.sort_values(by=['xmin'])
    final_answer = "".join(list(test_detect_res['name']))
    print((time.time() - firsttime))
    print(final_answer)

    return JsonResponse({"555": final_answer}, safe=False, status=status.HTTP_200_OK)


class Login(APIView):
    def get(self, request):
        user = authenticate(username=request.GET.get('username', ''), password=request.GET.get('password', ''))
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            return Response(status=200, data={"token": str(Token.objects.get(user=user)),
                                              "fullname": str(profile.fullname),
                                              "place": str(profile.place),
                                              "number_phone": str(profile.number_phone)})
        else:
            return Response(status=403, data={"message": "Неправильный ввод данных"})


class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response(status=200, data={"message": "Успешный выход из системы"})


class ResetPassword(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user is not None:
            user.set_password(request.GET.get('newpassword'))
            user.save()
            profile = Profile.objects.get(user=user)
            profile.default_password = False
            profile.save()
            Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(status=200, data={"token": str(Token.objects.get(user=user))})
        else:
            return Response(status=403, data={"message": "Неправильный ввод данных"})


class CheckDefaultPassword(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user is not None:
            profile = Profile.objects.get(user=request.user)
            return Response(status=200, data={"defaultpassword": str(profile.default_password)})
        else:
            return Response(status=403, data={"message": "Неавторизованный пользователь"})


class ServiceRecord(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Service_Record.objects.all()
    serializer_class = ServiceRecordSerializer

    def get(self, request):
        print(request.user, request.auth)
        rec = Service_Record.objects.filter(user_id=request.user)
        serializer = ServiceRecordListSerializer(rec, many=True)
        return Response(status=200, data={"hell": serializer.data})

    def post(self, request):
        print(request.user, request.data)
        Service__Record = request.data
        serializer = ServiceRecordSerializer(data=Service__Record)
        serializer.is_valid(raise_exception=True)
        Service_Record.objects.create(user_id=request.user,
                                      service=Service__Record["service"],
                                      description=Service__Record["description"],
                                      DateTime=datetime.now(),
                                      )
        rec = Service_Record.objects.filter(user_id=request.user)
        serializer = ServiceRecordListSerializer(rec, many=True)
        return Response(status=200, data=serializer.data)


class Counters(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer

    def get(self, request):
        print(request.user, request.auth)
        rec = Counter.objects.filter(user_id=request.user)
        serializer = CounterSerializer(rec, many=True)
        return Response(status=200, data={"counters": serializer.data})

    def post(self, request):
        print(request.user, request.data)
        new_counter = request.data
        serializer = CounterSerializer(data=new_counter)
        serializer.is_valid(raise_exception=True)
        Counter.objects.create(id_counter=new_counter["id_counter"],
                               typewater=new_counter["typewater"],
                               user_id=request.user,
                               isclever=new_counter["isclever"],
                               id_modem=new_counter["id_modem"],
                               id_registrator=new_counter["id_registrator"],
                               )
        rec = Counter.objects.filter(user_id=request.user)
        serializer = CounterSerializer(rec, many=True)
        return Response(status=200, data=serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class NewAndLastMetersData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = MetersData.objects.all()
    serializer_class = MetersDataSerializer

    def get(self, request, id_counter):
        print(request.user, request.auth)
        rec = MetersData.objects.filter(id_counter=id_counter).last()
        serializer = MetersDataSerializer(rec)
        return Response(status=200, data={"Metersdata": serializer.data})

    def post(self, request, id_counter):
        print(request.user, request.data)
        new_meterdata = request.data
        serializer = MetersDataSerializer(data=new_meterdata)
        serializer.is_valid(raise_exception=True)
        last_meters = MetersData.objects.filter(id_counter=id_counter).last()
        print(last_meters)
        if last_meters is not None:
            if int(new_meterdata["value"]) > int(str(last_meters)):
                new_water_flow = int(new_meterdata["value"]) - int(str(last_meters))
            else:
                new_water_flow = int("1" + "0"*len(str(last_meters))) - int(str(last_meters)) + int(new_meterdata["value"])
        else:
            new_water_flow = int(new_meterdata["value"])
        MetersData.objects.create(user_id=request.user,
                                  id_counter=Counter.objects.get(id_counter=id_counter),
                                  date=datetime.now(),
                                  year=datetime.now().year,
                                  value=new_meterdata["value"],
                                  water_flow=new_water_flow,
                                  )
        rec = MetersData.objects.filter(id_counter=id_counter).last()
        serializer = MetersDataSerializer(rec)
        return Response(status=200, data=serializer.data)


class CicleDiagrams(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, period):
        print(request.user, request.auth)
        cold_data = 0
        hot_data = 0
        all_hot_counters = Counter.objects.filter(user_id=request.user, typewater=1)
        all_cold_counters = Counter.objects.filter(user_id=request.user, typewater=0)
        for counter in all_hot_counters:
            hot_data += \
                MetersData.objects.filter(id_counter=counter, user_id=request.user).order_by('-id').values_list(
                    'water_flow')[
                :int(period)].aggregate(Sum('water_flow'))['water_flow__sum']
        for counter in all_cold_counters:
            cold_data += \
                MetersData.objects.filter(id_counter=counter, user_id=request.user).order_by('-id').values_list(
                    'water_flow')[
                :int(period)].aggregate(Sum('water_flow'))['water_flow__sum']

        return Response(status=200, data={"hot": str(float(hot_data)), "cold": str(float(cold_data))})


class PurpleDiagrams(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user, request.auth)
        mass_month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                      "Ноябрь", "Декабрь"]
        result = {"Январь": 0, "Февраль": 0, "Март": 0, "Апрель": 0, "Май": 0, "Июнь": 0, "Июль": 0, "Август": 0,
                  "Сентябрь": 0, "Октябрь": 0,
                  "Ноябрь": 0, "Декабрь": 0}
        all_counters = Counter.objects.filter(user_id=request.user)
        this_year = datetime.now().year
        for counter in all_counters:
            counters_value = MetersData.objects.filter(id_counter=counter, user_id=request.user, year=this_year).values(
                "water_flow", "date")
            for value in counters_value:
                result[mass_month[value['date'].month - 1]] += float(value['water_flow'])
        return Response(status=200, data={"result": result})

