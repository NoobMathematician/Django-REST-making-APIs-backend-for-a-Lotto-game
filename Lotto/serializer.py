from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models  import Lottos, Prizes, Tickets,PrizeSingle
class PrizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prizes
        fields = ('id','name','amount')

class PrizesSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizeSingle
        fields = ('id','name','amount')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        depth = 1
        fields = ('ticket_number','prize')

class LottosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottos
        depth = 1
        fields = ('id', 'name', 'total_tickets','prizes')

class LottosSerializerSingle(serializers.ModelSerializer):
    class Meta:
        model = Lottos
        depth = 1
        fields = ('id', 'name', 'total_tickets','available_tickets','winners_drawn','lotto_prizes')

