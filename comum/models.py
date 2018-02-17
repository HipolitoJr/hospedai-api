from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Endereco(models.Model):

    logradouro = models.CharField('Logradouro', max_length=255, blank=False, null=False)
    numero = models.IntegerField('Numero', blank=False, null=False)
    cep = models.IntegerField('CEP', blank=True, null=False)
    bairro = models.CharField('Bairro', max_length=255, blank=True, null=False)
    cidade = models.CharField('Cidade', max_length=255, blank=True, null=False)
    estado = models.CharField('Estado', max_length=255, blank=True, null=False)

    def __str__(self):
        return "%s, Nº - %s, %s" %(self.logradouro, self.numero, self.cidade, self.estado)


class Hotel(models.Model):

    razao_social = models.CharField('Razao social', max_length=255, blank=False, null=False)
    telefone = models.IntegerField('Telefone', blank=False, null=False)
    valor_diaria = models.FloatField('Valor diaria', blank=False, null=False)

    endereco = models.OneToOneField('Endereco', on_delete=models.SET_NULL, blank=True, null=True)
    usuario = models.OneToOneField(User, related_name='hotel')

    def __str__(self):
        return self.razao_social


class Hospede(models.Model):

    nome = models.CharField('Nome', max_length=255, blank=False, null=False)
    telefone = models.IntegerField('Telefone', blank=False, null=False)
    email = models.CharField('Email', max_length=255, blank=False, null=False)
    cpf = models.IntegerField('CPF', blank=False, null=False)

    endereco = models.OneToOneField('Endereco', on_delete=models.SET_NULL, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', related_name='clientes_hotel', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.nome


class Hospedagem(models.Model):

    TIPO_STATUS = (
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
    )

    data_checkin = models.DateTimeField('Data checkin', auto_now_add=True, blank=False, null=False)
    data_checkout = models.DateTimeField('Data checkout', auto_now=True, blank=True, null=True)
    status = models.CharField('Status', max_length=255, choices=TIPO_STATUS, blank=False, null=False)

    hospede = models.OneToOneField('Hospede', on_delete=models.SET_NULL, blank=True, null=True)
    hotel = models.OneToOneField('Hotel', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "%s - %s (%s)" %(self.hospede, self.status, self.hotel)
