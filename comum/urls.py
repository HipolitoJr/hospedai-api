from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hoteis', views.HotelViewSet)
router.register(r'usuarios', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^hoteis/(?P<pk>\d+)/hospedes/$',
        views.HospedeViewSet.as_view({'post': 'create', 'get': 'list'}), name='hospedes'),
    url(r'^hoteis/(?P<pk>\d+)/hospedagens/$',
        views.HospedagemViewSet.as_view({'post': 'create', 'get': 'list'}), name='hospedagens'),
    url(r'^hoteis/(?P<pk>\d+)/historico/$',
        views.HistoricoHospedagensViewSet.as_view({'get': 'list'}), name='historico'),
    url(r'^hoteis/(?P<hotel_pk>\d+)/hospedagens/(?P<hospedagem_pk>\d+)/checkout/$',
        views.HospedagemViewSet.dar_baixa, name='checkout')
]