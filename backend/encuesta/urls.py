from django.conf.urls import url
from . import views

urlpatterns = [
	#path('api', views.api_root),
	#url ('api', views.api_root),
	url('api/encuesta/$', views.EncuestaListCreate.as_view(), name = 'encuesta-list'),
	url('api/encuesta=(?P<pk>\d+)/detail$', views.EncuestaDetailView.as_view(), name='encuesta-detail' ),
	url('api/encuesta=(?P<pk>\d+)/update$', views.EncuestaDetailView.as_view() ),
	url('api/reporte=(?P<pk>\d+)/detail$', views.encuesta_detail, name = 'encuesta-reporte-list'),
	url('api/pregunta/$', views.PreguntaListCreate.as_view() , name='pregunta-list'),
	url('api/pregunta=(?P<pk>\d+)/detail$', views.PreguntaDetailView.as_view() , name='pregunta-detail'),
	url('api/alternativa/$', views.AlternativaListCreate.as_view(), name ='alternativa-list' ),
	url('api/alternativa=(?P<pk>\d+)/detail$', views.AlternativaListCreate.as_view(), name ='alternativa-detail' ),
	url('api/pregunta_detalle/$', views.Pregunta_detalleListCreate.as_view() , name='pregunta_detalle-list'),
	url('api/pregunta_detalle=(?P<pk>\d+)/update/$', views.Pregunta_detalleDetailView.as_view() , name='pregunta_detalle-update'),
	url('api/encuesta_pregunta/$', views.EncuestaPreguntaListCreate.as_view() , name = 'encuestapregunta-list'),
	url('api/encuesta_pregunta=(?P<pk>\d+)/detail$', views.EncuestaPreguntaDetailView.as_view(), name = 'encuestapregunta-detail'),
	#url('api/solucion/$', views.SolucionListCreate.as_view(), name = 'solucion-list'),
	#url('api/solucion=(?P<pk>\d+)/detail$', views.SolucionDetailView.as_view(), name='solucion-detail' ),
	url('api/solucion_texto_detalle/$', views.Solucion_texto_detalleListCreate.as_view(), name = 'solucion_texto_detalle-list' ),
	url('api/solucion_texto_detalle=(?P<pk>\d+)/detail/$', views.Solucion_texto_detalleDetailView.as_view(), name = 'solucion_texto_detalle-detail'),
	url('api/solucion_texto/$', views.Solucion_textoListCreate.as_view(), name = 'solucion_texto-list' ),
	url('api/solucion_texto=(?P<pk>\d+)/detail/$', views.Solucion_textoDetailView.as_view(), name = 'solucion_texto-detail'),
	url('api/solucion_alternativa_detalle/$', views.Solucion_alternativa_detalleListCreate.as_view(), name = 'solucion_alternativa_detalle-list' ),
	url('api/solucion_alternativa_detalle=(?P<pk>\d+)/detail$', views.Solucion_alternativa_detalleDetailView.as_view(), name = 'solucion_alternativa_detalle-detail' ),
	url('api/alternativa_orden/$', views.Alternativa_ordenListCreate.as_view(), name = 'alternativa_orden-list' ),
	url('api/alternativa_orden=(?P<pk>\d+)/detail$', views.Alternativa_ordenDetailView.as_view(), name = 'alternativa_orden-detail'),
	url('api/solucion_alternativa_orden_detalle/$', views.Solucion_alternativa_orden_detalleListCreate.as_view(), name = 'solucion_alternativa_orden_detalle-list' ),
	url('api/solucion_alternativa_orden_detalle=(?P<pk>\d+)/detail$', views.Solucion_alternativa_orden_detalleDetailView.as_view(), name = 'solucion_alternativa_orden_detalle-detail' )
]
