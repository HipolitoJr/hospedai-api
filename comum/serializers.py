
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from rest_framework import authentication, permissions, serializers, exceptions
from rest_framework.response import Response

from comum.models import Hotel, Hospede, Hospedagem


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('password', 'id', User.USERNAME_FIELD, 'full_name', 'is_active')
        read_only_fields = ('id', 'is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        usuario = User.objects.create_user(**validated_data)
        usuario.save()

        return usuario


class HotelUnicoSerializer(serializers.ModelSerializer):

    #usuario = serializers.StringRelatedField(many=False)

    class Meta:
        model = Hotel
        fields = ('id',
                  'usuario',
                  'razao_social',
                  'telefone',
                  'valor_diaria',
                  'endereco',)

        read_only_fields = ('id', 'clientes_hotel', 'hospedagens', 'usuario',)


class HospedeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospede
        fields = ('id',
                  'nome',
                  'cpf',
                  'telefone',
                  'email',
                  'endereco',)

        read_only_fields = ('id','hotel',)

    def create(self, validated_data):

        hotel_pk = self.context.get('hotel_pk')

        try:
            hotel_obj = Hotel.objects.get(pk=hotel_pk)
            hospede = Hospede.objects.create(**validated_data, hotel=hotel_obj)
            return hospede
        except Hotel.DoesNotExist:
            raise exceptions.NotFound(detail='Hotel não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível adicionar o Hospede.')


class HospedagemSerializer(serializers.ModelSerializer):

    #hospede = HospedeSerializer(many=False)

    class Meta:
        model = Hospedagem
        fields = ('id',
                  'status',
                  'hospede',
                  'valor_debito_atual',
                  'data_checkin',
                  'data_checkout',)

        read_only_fields = ('id', 'status',)

    def create(self, validated_data):

        hotel_pk = self.context.get('hotel_pk')
        hospede = validated_data['hospede']

        try:
            hotel = Hotel.objects.get(pk=hotel_pk)
            hospedagem = Hospedagem.objects.create(hotel=hotel, hospede=hospede)
            return hospedagem
        except Hotel.DoesNotExist or Hospede.DoesNotExist:
            raise exceptions.NotFound(detail='Hotel ou Hospede não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível adicionar a Hospedagem.')


class HotelSerializer(serializers.ModelSerializer):

    clientes_hotel = HospedeSerializer(many=True)
    hospedagens = HospedagemSerializer(many=True)
    usuario = UserSerializer(many=False)

    class Meta:
        read_only_fields = ('id', 'clientes_hotel', )
        model = Hotel
        fields = ('id',
                  'usuario',
                  'razao_social',
                  'telefone',
                  'valor_diaria',
                  'endereco',
                  'clientes_hotel',
                  'hospedagens',)