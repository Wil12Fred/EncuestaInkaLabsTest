from rest_framework import serializers
from django.core.exceptions import ValidationError
from encuesta.models import Encuesta, Pregunta, Alternativa, Pregunta_detalle, EncuestaPregunta, Solucion_texto_detalle, Solucion_alternativa_detalle, Alternativa_orden, Solucion_alternativa_orden_detalle, Encuesta_alternativa_orden, Solucion_texto

class EncuestaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Encuesta
		fields = '__all__'

class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Pregunta
		fields = '__all__'
		#fields = ['url', 'titulo', 'enunciado', 'tipo', 'alternativas']#'__all__'

class AlternativaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Alternativa
		fields = '__all__'

class Pregunta_detalleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Pregunta_detalle
		fields = '__all__'

class EncuestaPreguntaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = EncuestaPregunta
		fields = '__all__'

class Solucion_texto_detalleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Solucion_texto_detalle
		fields = '__all__'
	def validate_pregunta(self, pregunta):
		if(pregunta.pregunta.tipo==0):
			try:
				data = pregunta
			except Exception as e:
				raise ValidationError({
					'field_pregunta': e.detail,
				})
			return data
		else:
			raise ValidationError({
				'field_pregunta': 'is not type text (tipo=0)',
			})
		return data

class Solucion_textoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Solucion_texto
		fields = '__all__'

class Solucion_alternativa_detalleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Solucion_alternativa_detalle
		fields = '__all__'
	def validate_pregunta(self, pregunta):
		if(pregunta.pregunta.tipo==1):
			try:
				data = pregunta
			except Exception as e:
				raise ValidationError({
					'field_pregunta': e.detail,
				})
			return data
		else:
			raise ValidationError({
				'field_pregunta': 'is not type alternativa (tipo=1)',
			})
		return data

class Alternativa_ordenSerializer(serializers.HyperlinkedModelSerializer):
	def get_total(self, obj):
		return getattr(obj, 'total', 1)
	class Meta:
		model = Alternativa_orden
		fields = ('url', 'pregunta', 'alternativa', 'orden')

class Solucion_alternativa_orden_detalleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Solucion_alternativa_orden_detalle
		fields = '__all__'

class Encuesta_alternativa_ordenSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Encuesta_alternativa_orden
		fields = '__all__'
