from rest_framework import serializers
from .models import *
    
class SistemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sistem
        fields = "__all__"

class AktuatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktuator
        fields = "__all__"
        