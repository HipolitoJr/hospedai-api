from datetime import datetime
from pytz import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Hotel(models.Model):

    razao_social = models.CharField('Razao social', max_length=255, blank=False, null=False)
    telefone = models.IntegerField('Telefone', blank=False, null=False)
    valor_diaria = models.FloatField('Valor diaria', blank=False, null=False)
    endereco = models.CharField('Endereco', max_length=255, blank=True, null=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hoteis', blank=True, null=True)

    def __str__(self):
        return self.razao_social


class Hospede(models.Model):

    nome = models.CharField('Nome', max_length=255, blank=False, null=False)
    telefone = models.IntegerField('Telefone', blank=False, null=False)
    email = models.CharField('Email', max_length=255, blank=False, null=False)
    cpf = models.IntegerField('CPF', blank=False, null=False)
    endereco = models.CharField('Endereco', max_length=255, blank=True, null=True)

    hotel = models.ForeignKey('Hotel', related_name='clientes_hotel', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nome


class Hospedagem(models.Model):

    TIPO_STATUS = (
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
    )

    data_checkin = models.DateTimeField('Data checkin', auto_now_add=True, blank=False, null=False)
    data_checkout = models.DateTimeField('Data checkout', blank=True, null=True)
    status = models.CharField('Status', max_length=255, choices=TIPO_STATUS, default='aberta', blank=False, null=False)
    valor_debito = models.FloatField('Valor debito', blank=True, null=True)

    hospede = models.OneToOneField('Hospede', on_delete=models.SET_NULL, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', related_name='hospedagens', on_delete=models.CASCADE, blank=True, null=True)

    def dar_baixa(self):
        self.data_checkout = datetime.now(timezone('America/Fortaleza'))
        self.status = 'fechada'
        return self.valor_debito_atual()

    def valor_debito_atual(self):
        if self.status == "aberta":
            tempo_estadia = datetime.now(timezone('America/Fortaleza')) - self.data_checkin
        else:
            tempo_estadia = self.data_checkout - self.data_checkin

        self.valor_debito = self.hotel.valor_diaria * (tempo_estadia.days + 1)
        self.save()

        return self.valor_debito

    def __str__(self):
        return "%s - %s (%s)" %(self.hospede, self.status, self.hotel)
