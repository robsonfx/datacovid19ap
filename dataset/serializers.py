from rest_framework import serializers
from .models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    cidade = serializers.CharField(source='get_cidade_display')
    class Meta:
        model = Registro
        fields = ('pk', 'cidade', 'data', 'suspeitos', 'confirmados', 'descartados', 'recuperados', 'obitos')