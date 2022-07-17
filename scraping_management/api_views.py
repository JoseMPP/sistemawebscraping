from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Oferta,Ejecucion
from .serializers import OfertaSerializer

@api_view()
def all_ofertas(request):
    ofertas = Oferta.objects.all()
    ofertas_serializer = OfertaSerializer(ofertas,many=True)
    return Response(ofertas_serializer.data)

@api_view()
def first_oferta_api(request):
    num_ofertas = Oferta.objects.count()
    return  Response({"num_ofertas":num_ofertas})

class AllOfertas(ListAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
