from rest_framework import serializers
from .models import Madre, Parto, RecienNacido, InformeREM


class MadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Madre
        fields = '__all__'


class PartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parto
        fields = '__all__'


class RecienNacidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecienNacido
        fields = '__all__'


class InformeREMSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeREM
        fields = '__all__'
