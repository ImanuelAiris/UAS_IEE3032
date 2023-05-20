from django.shortcuts import render
from rest_framework.response import Response
import paho.mqtt.client as mqtt

from .serializers import *
from .models import *
from .machinelearning import *

machinelearning = mlirigasi()

def webview(request):
    """A view of all bands."""
    view1 = Sistem.objects.get(name="kelembaban").value
    view2 = Sistem.objects.get(name="ph").value
    view3 = Sistem.objects.get(name="suhu").value
    act = Aktuator.objects.get(name='sprinkler').value
    return render(request, 'webview.html', {'views1': view1, 'views2': view2, 'views3': view3, 'views_act':act})

def actuator_prediction():
    kelembaban = Sistem.objects.get(name="kelembaban").value
    ph = Sistem.objects.get(name="ph").value
    suhu = Sistem.objects.get(name="suhu").value
    aktuator = machinelearning.hitungml(int(kelembaban), int(ph), int(suhu))
    if aktuator < 0:
        aktuator = 0
    elif aktuator > 30:
        aktuator = 30
    data_act = {
            'value': aktuator
        }
    act = Aktuator.objects.get(name="sprinkler")
    serializer = AktuatorSerializer(act, data=data_act, partial=True)
    if serializer.is_valid():
        serializer.save()

def on_message_kelembaban(client, userdata, msg):
    kelembaban = Sistem.objects.get(name="kelembaban")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SistemSerializer(kelembaban, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print('recieved a new kelembaban data ', msg.payload.decode('utf-8'))    
    
    return Response({"value": msg.payload.decode('utf-8')}) 
    
def on_message_ph(client, userdata, msg):
    ph = Sistem.objects.get(name="ph")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SistemSerializer(ph, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print('recieved a new ph data ', msg.payload.decode('utf-8'))   
    return Response({"value": msg.payload.decode('utf-8')})
    
def on_message_suhu(client, userdata, msg):
    suhu = Sistem.objects.get(name="suhu")
    data = {
        'value': msg.payload.decode('utf-8')
    }
    serializer = SistemSerializer(suhu, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print('recieved a new suhu data ', msg.payload.decode('utf-8'))    
    actuator_prediction()
    return Response({"value": msg.payload.decode('utf-8')})

client = mqtt.Client("smart_farm_appp")

client.message_callback_add('sf/kelembaban', on_message_kelembaban)
client.message_callback_add('sf/ph', on_message_ph)
client.message_callback_add('sf/suhu', on_message_suhu)

client.connect('localhost', 1883)
client.loop_start()
client.subscribe('sf/#')