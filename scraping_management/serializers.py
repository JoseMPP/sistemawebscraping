from rest_framework import serializers
from .models import Oferta,Ejecucion,SitioWeb,Categoria
"""Forma manual de serializar:"""
# class SitioWebSerializer(serializers.Serializer):
#     nombre = serializers.CharField()
#     dominio = serializers.CharField()
# class CategoriaSerializer(serializers.Serializer):
#     nombre = serializers.CharField()
# class EjecucionSerializer(serializers.Serializer):
#     categoria = CategoriaSerializer()
#     sitio_web = SitioWebSerializer()
# class OfertaSerializer(serializers.Serializer):
#     titulo = serializers.CharField()
#     precio = serializers.FloatField()
#     divisa = serializers.CharField()
#     fecha_extraccion = serializers.DateTimeField()
#     url_image = serializers.CharField()
#     ejecucion = EjecucionSerializer()
"""Forma mas eficiente usando modelos:"""
class SitioWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitioWeb
        fields = ['nombre','dominio']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

class EjecucionSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    sitio_web = SitioWebSerializer()
    class Meta:
        model = Ejecucion
        fields = ['categoria','sitio_web']

class OfertaSerializer(serializers.ModelSerializer):
    ejecucion = EjecucionSerializer()
    class Meta:
        model = Oferta
        fields = ['titulo','precio','divisa','fecha_extraccion','url_image','ejecucion']