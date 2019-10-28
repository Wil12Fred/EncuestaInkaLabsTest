from django.shortcuts import render
from django.db.models import Q 
from django.db.models import Count
from django.core.urlresolvers import resolve

# Create your views here.

from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response 
from encuesta.models import Alternativa, Pregunta, Encuesta, Pregunta_detalle, EncuestaPregunta, Solucion_texto_detalle, Solucion_texto, Solucion_alternativa_detalle, Alternativa_orden, Solucion_alternativa_orden_detalle, Encuesta_alternativa_orden
from encuesta.serializers import EncuestaSerializer, PreguntaSerializer, AlternativaSerializer, Pregunta_detalleSerializer, EncuestaPreguntaSerializer, Solucion_texto_detalleSerializer, Solucion_textoSerializer, Solucion_alternativa_detalleSerializer, Alternativa_ordenSerializer, Solucion_alternativa_orden_detalleSerializer, Encuesta_alternativa_ordenSerializer

def reporte_texto(encuesta_pregunta):
	solucion_textos = Solucion_texto.objects.filter(pregunta__id=encuesta_pregunta.id).order_by('-count')[:50]
	reporte = {}
	for solucion_texto in solucion_textos:
		reporte[solucion_texto.texto]=solucion_texto.count
	return reporte

def reporte_alternativa(encuesta_pregunta):
	solucion_alternativa_detalles = Solucion_alternativa_detalle.objects.filter(pregunta__id=encuesta_pregunta.id).values('alternativa').annotate(dcount=Count('alternativa'))
	reporte = {}
	total=0
	for solucion_alternativa in solucion_alternativa_detalles:
		reporte[solucion_alternativa['alternativa']]=solucion_alternativa['dcount']
		total += reporte[solucion_alternativa['alternativa']]
	if(total>0):
		for solucion_alternativa in solucion_alternativa_detalles:
			reporte[solucion_alternativa['alternativa']]=(solucion_alternativa['dcount'])/total
	return reporte

def reporte_alternativa_orden(encuesta_pregunta):
	alternativas_orden = Alternativa_orden.objects.filter(pregunta__id=encuesta_pregunta.id)
	reporte = {}
	for alternativa_orden in alternativas_orden:
		print(alternativa_orden.pregunta.pregunta)
		print(alternativa_orden.pregunta.pregunta.id)
		if (alternativa_orden.pregunta.pregunta.id in reporte)==False:
			reporte[alternativa_orden.pregunta.pregunta.id]={}
			reporte[alternativa_orden.pregunta.pregunta.id]['total']=0
		reporte[alternativa_orden.pregunta.pregunta.id][alternativa_orden.orden]=alternativa_orden.total
		reporte[alternativa_orden.pregunta.pregunta.id]['total'] += alternativa_orden.total
	for alternativa_orden in alternativas_orden:
		reporte[alternativa_orden.pregunta.pregunta.id][alternativa_orden.orden]=alternativa_orden.total/reporte[alternativa_orden.pregunta.pregunta.id]['total']
	return reporte

@api_view(["GET"])
def encuesta_detail(request, pk):
	encuestas = Encuesta.objects.filter(pk=pk)
	if(len(encuestas)!=0):
		encuesta=encuestas[0]
		encuesta_preguntas = EncuestaPregunta.objects.filter(encuesta__id=pk)
		#preguntas = encuesta.preguntas.all() 
		reporte = {}
		for encuesta_pregunta in encuesta_preguntas:
			pregunta = encuesta_pregunta.pregunta
			preguntaserializer = PreguntaSerializer(encuesta_pregunta, context={'request': request})
			reporte[pregunta.id]={}
			if pregunta.tipo==0:
				reporte[pregunta.id]['textos'] = reporte_texto(encuesta_pregunta)
			elif pregunta.tipo==1:
				reporte[pregunta.id]['alternativas'] = reporte_alternativa(encuesta_pregunta)
			elif pregunta.tipo==2:
				reporte[pregunta.id]['alternativas_orden'] = reporte_alternativa_orden(encuesta_pregunta)
		print(reporte)
		#alternativa_total = len(Solucion_alternativa_detalle.objects.filter(Q(pregunta__id=encuesta_pregunta.pregunta.id) & Q(alternativa__id=alternativa.id)))
		serializer = EncuestaSerializer(encuesta, context={'request': request})
		return Response(reporte)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

class AlternativaListCreate(generics.ListCreateAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer

class AlternativaDetailView(generics.RetrieveAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer

class PreguntaListCreate(generics.ListCreateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

class PreguntaDetailView(generics.RetrieveAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

class EncuestaListCreate(generics.ListCreateAPIView):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class EncuestaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class Pregunta_detalleListCreate(generics.ListCreateAPIView):
    queryset = Pregunta_detalle.objects.all()
    serializer_class = Pregunta_detalleSerializer

class Pregunta_detalleDetailView(generics.RetrieveUpdateAPIView):
    queryset = Pregunta_detalle.objects.all()
    serializer_class = Pregunta_detalleSerializer

class EncuestaPreguntaListCreate(generics.ListCreateAPIView):
    queryset = EncuestaPregunta.objects.all()
    serializer_class = EncuestaPreguntaSerializer

class EncuestaPreguntaDetailView(generics.RetrieveAPIView):
    queryset = EncuestaPregunta.objects.all()
    serializer_class = EncuestaPreguntaSerializer

class Solucion_texto_detalleListCreate(generics.ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	queryset = Solucion_texto_detalle.objects.all()
	serializer_class = Solucion_texto_detalleSerializer
	def post(self, request, *args, **kwargs):
		serializer = Solucion_texto_detalleSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			encuestapregunta = serializer.validated_data['pregunta']
			textos = serializer.validated_data['texto'].split()
			for texto in textos:
				solucion_texto = Solucion_texto.objects.filter(Q(pregunta__id=encuestapregunta.id) & Q(texto=texto))
				if(len(solucion_texto)==0):
					solucion_texto=Solucion_texto(pregunta=encuestapregunta, texto=texto)
				else:
					solucion_texto=solucion_texto[0]
					solucion_texto.count = solucion_texto.count + 1
				solucion_texto.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Solucion_texto_detalleDetailView(generics.RetrieveAPIView):
    queryset = Solucion_texto_detalle.objects.all()
    serializer_class = Solucion_texto_detalleSerializer

class Solucion_textoListCreate(generics.ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	queryset = Solucion_texto.objects.all()
	serializer_class = Solucion_textoSerializer

class Solucion_textoDetailView(generics.RetrieveAPIView):
	queryset = Solucion_texto.objects.all()
	serializer_class = Solucion_textoSerializer

class Solucion_alternativa_detalleListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Solucion_alternativa_detalle.objects.all()
    serializer_class = Solucion_alternativa_detalleSerializer

class Solucion_alternativa_detalleDetailView(generics.RetrieveAPIView):
    queryset = Solucion_alternativa_detalle.objects.all()
    serializer_class = Solucion_alternativa_detalleSerializer

class Alternativa_ordenListCreate(generics.ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	queryset = Alternativa_orden.objects.all()
	serializer_class = Alternativa_ordenSerializer
	def post(self, request, *args, **kwargs):
		serializer = Alternativa_ordenSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			alternativa_orden = serializer.validated_data
			alternativa_ordens = Alternativa_orden.objects.filter(Q(pregunta__id=alternativa_orden['pregunta'].id) & Q(alternativa__id=alternativa_orden['alternativa'].id) & Q(orden=alternativa_orden['orden']))
			if(len(alternativa_ordens)!=0):
				alternativa_orden = alternativa_ordens[0]
				print(alternativa_orden)
				alternativa_orden.total = alternativa_orden.total + 1
				alternativa_orden.save()
				serializer = Alternativa_ordenSerializer(alternativa_orden, context={'request': request})
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				alternativa_orden = Alternativa_orden(pregunta=alternativa_orden['pregunta'], alternativa=alternativa_orden['alternativa'], orden = alternativa_orden['orden'], total = 1)
				alternativas = alternativa_orden.pregunta.pregunta.alternativas.filter(pk=alternativa_orden.alternativa.id)
				total_alternativas=len(alternativa_orden.pregunta.pregunta.alternativas.all())
				if(len(alternativas)!=0 and alternativa_orden.orden>0 and alternativa_orden.orden<=total_alternativas):
					alternativa_orden.save()
					serializer = Alternativa_ordenSerializer(alternativa_orden, context={'request': request})
					return Response(serializer.data, status=status.HTTP_201_CREATED)
				else:
					return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			alternativa_orden = serializer.validated_data
			print (alternativa_orden)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Alternativa_ordenDetailView(generics.RetrieveAPIView):
    queryset = Alternativa_orden.objects.all()
    serializer_class = Alternativa_ordenSerializer

class Solucion_alternativa_orden_detalleListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Solucion_alternativa_orden_detalle.objects.all()
    serializer_class = Solucion_alternativa_orden_detalleSerializer

class Solucion_alternativa_orden_detalleDetailView(generics.RetrieveAPIView):
    queryset = Solucion_alternativa_orden_detalle.objects.all()
    serializer_class = Solucion_alternativa_orden_detalleSerializer

class Encuesta_alternativa_ordenListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Solucion_alternativa_orden_detalle.objects.all()
    serializer_class = Solucion_alternativa_orden_detalleSerializer

class Encuesta_alternativa_ordenDetailView(generics.RetrieveAPIView):
    queryset = Encuesta_alternativa_orden.objects.all()
    serializer_class = Encuesta_alternativa_ordenSerializer

