from django.contrib.auth import get_user_model
from rest_framework import viewsets, authentication, permissions, status

# Create your views here.
from rest_framework.response import Response

from comum.models import Hotel, Hospede, Hospedagem
from comum.serializers import HotelUnicoSerializer, HospedeSerializer, HospedagemSerializer, HotelSerializer, \
    UserSerializer

User = get_user_model()

class DefaultMixin(object):

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )


class HotelViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Hotel.objects.order_by('id')
    serializer_class = HotelUnicoSerializer

    def retrieve(self, request, *args, **kwargs):
        hotel = self.get_object()
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        usuario_logado = request.user
        razao_social = request.data['razao_social']
        telefone = request.data['telefone']
        valor_diaria = request.data['valor_diaria']
        endereco = request.data['endereco']
        hotel = Hotel.objects.create(usuario=usuario_logado,
                                     razao_social=razao_social,
                                     telefone=telefone,
                                     valor_diaria=valor_diaria,
                                     endereco=endereco)

        serializer = HotelUnicoSerializer(hotel,
                                          data=request.data)
        serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        usuario_logado = request.user
        queryset = self.filter_queryset(Hotel.objects.filter(usuario=usuario_logado))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HospedeViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Hospede.objects.order_by('id')
    serializer_class = HospedeSerializer

    def create(self, request, pk, *args, **kwargs):
        serializer = HospedeSerializer(data=request.data,
                                         context={'hotel_pk': pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(Hospede.objects.filter(hotel__pk=pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HospedagemViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Hospedagem.objects.order_by('id')
    serializer_class = HospedagemSerializer

    def create(self, request, pk, *args, **kwargs):
        serializer = HospedagemSerializer(data=request.data,
                                         context={'hotel_pk': pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(Hospedagem.objects.filter(hotel__pk=pk, status='aberta'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def dar_baixa(self, hotel_pk, hospedagem_pk):
        hospedagem = Hospedagem.objects.get(pk = hospedagem_pk)
        hospedagem.dar_baixa()
        serializer = self.get_serializer_class(hospedagem)

        return Response(serializer.data)


class HistoricoHospedagensViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Hospedagem.objects.filter(status='fechada')
    serializer_class = HospedagemSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer