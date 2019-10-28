from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.

#Model 2 lvl-1
class Alternativa(models.Model):
	texto = models.CharField(max_length=50)
	def __str__(self):
		return "/api/alternativa="+str(self.id)+"/detail"
		#return self.texto;

#Model 1 lvl-1
class Pregunta(models.Model):
	titulo = models.CharField(max_length=30)
	enunciado = models.CharField(max_length=50)
	tipo = models.IntegerField(
		default = 0,
		validators=[
			MaxValueValidator(2),
			MinValueValidator(0)
		]
	)
	alternativas = models.ManyToManyField(Alternativa, blank=True, through='Pregunta_detalle')
	def __str__(self):
		return "/api/pregunta="+str(self.id)+"/detail"

#Model 0 lvl-1
class Encuesta(models.Model):
	nombre = models.CharField(max_length=30)
	fecha = models.DateField(default=datetime.date.today)
	descripción = models.CharField(max_length=50)
	preguntas = models.ManyToManyField(Pregunta, blank=True, through='EncuestaPregunta')
	def __str__(self):
		return "/api/encuesta="+str(self.id)+"/detail"

#Model 3 lvl-2
class Pregunta_detalle(models.Model):
	pregunta = models.ForeignKey(Pregunta)
	alternativa = models.ForeignKey(Alternativa)
	def __str__(self):
		return "/api/pregunta_detalle="+str(self.id)+"/detail"
	class Meta:
		unique_together = ('pregunta', 'alternativa',)

#Model 4 lvl-2
class EncuestaPregunta(models.Model):
	encuesta = models.ForeignKey(Encuesta)
	pregunta = models.ForeignKey(Pregunta)
	def __str__(self):
		return "/api/encuesta_pregunta="+str(self.id)+"/detail"
	class Meta:
		unique_together = ('encuesta', 'pregunta',)

#Model 6
class Solucion_texto_detalle(models.Model):
	pregunta = models.ForeignKey(EncuestaPregunta)
	texto = models.CharField(max_length=50)

#Model 6
class Solucion_texto(models.Model):
	pregunta = models.ForeignKey(EncuestaPregunta)
	texto = models.CharField(max_length=30)
	count = models.IntegerField(default=1)
	#objects = Solucion_textoManager()

#Model 7
class Solucion_alternativa_detalle(models.Model):
	pregunta = models.ForeignKey(EncuestaPregunta)
	alternativa = models.ForeignKey(Alternativa)
	def __str__(self):
		return "/api/solucion_alternativa_detalle="+str(self.id)+"/detail"

#Model 3 lvl-2
class Alternativa_orden(models.Model):
	pregunta = models.ForeignKey(EncuestaPregunta)
	alternativa = models.ForeignKey(Alternativa)
	orden = models.IntegerField()
	total = models.IntegerField()
	def __str__(self):
		return "/api/alternativa_orden="+str(self.id)+"/detail"
	"""class Meta:
		unique_together = ('pregunta', 'alternativa','orden')"""

#Model 8
class Solucion_alternativa_orden_detalle(models.Model):
	alternativas = models.ManyToManyField(Alternativa_orden, blank=False, through='Encuesta_alternativa_orden')
	def __str__(self):
		return "/api/solucion_alternativa_orden_detalle="+str(self.id)+"/detail"

#Model 3 lvl-2
class Encuesta_alternativa_orden(models.Model):
	Solucion_alternativa_orden_detalle = models.ForeignKey(Solucion_alternativa_orden_detalle)
	alternativa = models.ForeignKey(Alternativa_orden)
	def __str__(self):
		return "/api/encuesta_alternativa_orden="+str(self.id)+"/detail"
