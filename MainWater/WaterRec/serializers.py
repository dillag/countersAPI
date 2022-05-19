from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import Service_Record


class MetersDataSerializer(serializers.Serializer):
    id_counter = serializers.CharField()
    user_id = serializers.CharField()
    value = serializers.CharField(max_length=6)


class CounterSerializer(serializers.Serializer):
    id_counter = serializers.IntegerField()
    typewater = serializers.IntegerField()
    user_id = serializers.CharField()
    isclever = serializers.BooleanField()
    id_modem = serializers.CharField()
    id_registrator = serializers.CharField()



class ServiceRecordSerializer(serializers.Serializer):
    service = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=300, allow_blank=True)


class ServiceRecordListSerializer(ServiceRecordSerializer):
    user_id = serializers.CharField(max_length=50)
    pk = serializers.IntegerField()
    DateTime = serializers.DateTimeField()


class IssueTokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
