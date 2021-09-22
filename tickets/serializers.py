from rest_framework import serializers
from .models import Guest, Movie, Reservation

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model= Guest
        fields= ['reservation', 'guest_name', 'mobile']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields= '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Reservation
        fields= '__all__'