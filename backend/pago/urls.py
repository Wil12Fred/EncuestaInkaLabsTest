from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/dpago/$', views.PagoDListCreate.as_view() ),
    url(r'^api/dpago=(?P<pk>\d+)/detail$', views.PagoDDetailView.as_view(), name = "nuevo_pago_detail"),
    url('api/nuevopago/$', views.Pago2ListCreate.as_view() ),
    url(r'^api/nuevopago=(?P<pk>\d+)/detail$', views.PagoDetailView.as_view(), name = "nuevo_pago_detail"),
    url('api/pago/$', views.PagoListCreate.as_view() ),
    url(r'^api/pago=(?P<pk>\d+)/detail$', views.PagoDetailView.as_view(), name = "pago_detail"),
    url('api/entidad/$', views.EntidadListCreate.as_view() ),
    url(r'^api/entidad=(?P<pk>\d+)/detail$', views.EntidadDetailView.as_view(), name = "entidad_detail"),
    url('api/suministro/$', views.SuministroListCreate.as_view() ),
    url(r'^api/suministro=(?P<pk>\d+)/detail$', views.SuministroDetailView.as_view(), name = "suministro_detail"),
    url('api/servicio/$', views.ServicioListCreate.as_view() ),
    url(r'^api/servicio=(?P<pk>\d+)/detail$', views.ServicioDetailView.as_view(), name = "servicio_detail"),
    url('api/tarjeta/$', views.TarjetaListCreate.as_view() ),
    url(r'^api/tarjeta=(?P<pk>\d+)/detail$', views.TarjetaDetailView.as_view(), name = "tarjeta_detail"),
    url(r'^api/servicioporentidad$', views.ServicioPorEntidadView.as_view(), name = "servicios_de_entidad"),
    url(r'^api/sumporcod$', views.SuministroPorCodigo.as_view(), name = "suministro_por_codigo")
]
