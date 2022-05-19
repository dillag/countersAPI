import base64
import json
import time
from datetime import datetime
from io import BytesIO
from rest_framework.authtoken.models import Token
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

# model2 = torch.hub.load('E:/yolov5-master', 'custom', path="E:/yolov5-master/runs/train/exp16/weights/best.pt",
#                         source='local')  # or yolov5m, yolov5l, yolov5x, custom
# model = torch.hub.load('E:/yolov5-master', 'custom', path="E:/yolov5-master/runs/train/exp16/weights/best1.pt",
#                        source='local')  # or yolov5m, yolov5l, yolov5x, c

model2 = 'E:/yolov5-master'
model = 'E:/yolov5-master'

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
    detect_res = results.pandas().xyxy[0]
    # Crop image with coord after first model
    cropped_image = image.crop(
        (int(detect_res['xmin']), int(detect_res['ymin']), int(detect_res['xmax']), int(detect_res['ymax'])))
    # Predict second model
    results_numbers = model2(cropped_image)
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


class NewAndLastMetersData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = MetersData.objects.all()
    serializer_class = MetersDataSerializer

    def get(self, request, id_counter):
        print(request.user, request.auth)
        profile = Profile.objects.get(user=request.user)
        counter = Counter.objects.get(id_counter=id_counter)
        if counter.isclever:
            api_body_request = "https://lk.waviot.ru/api.data/get_values/?modem_id=" + counter.id_modem
            api_key = "&key=" + profile.api_key
            main_request = requests.get(api_body_request+api_key)
            last_value = int(json.loads(main_request.text)["registrators"][str(counter.id_registrator)]["values"][-1]["value"])
            return Response(status=200, data={"Metersdata": {"id_counter": counter.id_counter, "user_id": str(counter.user_id), "value": str(last_value)}})
        else:
            rec = MetersData.objects.filter(id_counter=id_counter).last()
            serializer = MetersDataSerializer(rec)
            return Response(status=200, data={"Metersdata": serializer.data})

    def post(self, request, id_counter):
        print(request.user, request.data)
        new_meterdata = request.data
        serializer = MetersDataSerializer(data=new_meterdata)
        serializer.is_valid(raise_exception=True)
        MetersData.objects.create(user_id=request.user,
                                  id_counter=Counter.objects.get(id_counter=id_counter),
                                  date=datetime.now(),
                                  value=new_meterdata["value"],
                                  )
        rec = MetersData.objects.filter(id_counter=id_counter).last()
        serializer = MetersDataSerializer(rec)
        return Response(status=200, data=serializer.data)
