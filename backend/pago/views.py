from django.shortcuts import render

# Create your views here.

from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework.response import Response 
from pago.models import Pago, Entidad, Servicio, Suministro, Tarjeta, ReturnSuministro, Pago2, PagoD
from .serializers import PagoSerializer, EntidadSerializer, ServicioSerializer, SuministroSerializer, TarjetaSerializer, ReturnSuministroSerializer, Pago2Serializer, PagoDSerializer
import random

class EntidadListCreate(generics.ListCreateAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer

class EntidadDetailView(generics.RetrieveAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer

class ServicioListCreate(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ServicioDetailView(generics.RetrieveAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class SuministroListCreate(generics.ListCreateAPIView):
    queryset = Suministro.objects.all()
    serializer_class = SuministroSerializer

class SuministroDetailView(generics.RetrieveAPIView):
    queryset = Suministro.objects.all()
    serializer_class = SuministroSerializer

class PagoListCreate(generics.ListCreateAPIView):
    queryset = Pago2.objects.all()
    serializer_class = Pago2Serializer

class PagoDetailView(generics.RetrieveAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class Pago2ListCreate(generics.ListCreateAPIView):
    queryset = Pago2.objects.all()
    serializer_class = Pago2Serializer

class Pago2DetailView(generics.RetrieveAPIView):
    queryset = Pago2.objects.all()
    serializer_class = Pago2Serializer

class PagoDListCreate(generics.ListCreateAPIView):
    queryset = PagoD.objects.all()
    serializer_class = PagoDSerializer

class PagoDDetailView(generics.RetrieveAPIView):
    queryset = PagoD.objects.all()
    serializer_class = PagoDSerializer

class TarjetaListCreate(generics.ListCreateAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class TarjetaDetailView(generics.RetrieveAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class ServicioPorEntidadView(generics.ListCreateAPIView):
    model = Servicio
    serializer_class = ServicioSerializer
    def get_queryset(self):
        entidadId = int(self.request.query_params.get('entidad'))
        queryset = Servicio.objects.filter(entidad=entidadId)
        return queryset

class SuministroPorCodigo(generics.ListCreateAPIView):
    model = ReturnSuministro
    serializer_class = ReturnSuministroSerializer
    def get_queryset(self):
        suministroCodigo = self.request.query_params.get('numero')
        servicioId = int(self.request.query_params.get('servicio'))
        querySum = Suministro.objects.filter(servicio=servicioId).filter(codigo=suministroCodigo)
        newReturn = []
        if(len(querySum)>0):
            print (".........")
            a = ReturnSuministro
            a.monto="S/ "+str(random.randrange(1000))
            a.descripcion = querySum[0].servicio.nombre
            a.id = 1
            a.titular = querySum[0].titular
            a.codigo = querySum[0].codigo
            newReturn.append(a)
        return newReturn
