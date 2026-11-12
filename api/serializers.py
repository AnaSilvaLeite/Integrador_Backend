
from rest_framework import serializers
from .models import Environment, EquipmentModel, Microcontroller, Sensor, Reading, User 
from django.contrib.auth.password_validation import validate_password # Responsável por validar senhas conforme as regras configuradas no Django

class EnvironmentSerializer(serializers.ModelSerializer):

    class Meta: # Fornece configurações para o Serializer
        model = Environment # Informa qual Model
        fields = '__all__' #Informa quais campos
        
class EquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = '__all__'

class MicrocontrollerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Microcontroller
        fields= '__all__'
        
class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'

    # Função para validar função e unidade de medida do sensor
    def validate(self, data):
        function = data.get(
            'function',
            self.instance.function if self.instance else None
        )

        unit = data.get(
            'unit_measureament',
            self.instance.unit_measureament if self.instance else None
        )

        combinations = {
            'temperature': '°C',
            'humidity': '%',
            'luminosity': 'lux',
            'counter': 'un'
        }

        if function and unit and combinations[function] != unit:
            raise serializers.ValidationError({
                'unit_measureament': 'A unidade de medida não corresponde à função do sensor.'
            })

        return data
        
class ReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = '__all__'

    # Método exclusivo para validar o campo sensor, onde caso verifica os statos do sensor e microcontrolador
    # Caso o Sensor ou o Microcontrolador estiver inativo irá mostrar mensagem de erro
    def validate_sensor(self, sensor):

        if sensor.status == 'INACTIVE':
            raise serializers.ValidationError(
                'Não é possível registrar medições em um sensor inativo.'
            )

        if sensor.microcontroller.status == 'INACTIVE':
            raise serializers.ValidationError(
                'Não é possível registrar medições em um microcontrolador inativo.'
            )

        return sensor
        

class UserSerializer(serializers.ModelSerializer):

    # Configuração personalizada para não retornar a senha no Json
    password = serializers.CharField(
        write_only=True,
        required=False
    )

    # Personalizei os dados que seram enviados no Json
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'email',
            'type',
            'photo',
            'password'
        ]

    def validate(self, data):
        # Verifica se aquele usuário ja existe e se a senha esta com campo vazio, impedindo cadastro com senha vazia
        if not self.instance and not data.get('password'):
            raise serializers.ValidationError({
                'password': 'A senha é obrigatória no cadastro.'
            })

        return data

    # Método que valida a senha conforme diretrizes da biblioteca importada como: tamanha suficiente, senhas comuns...
    def validate_password(self, value):
        validate_password(value)
        return value

    # Método é responsável por criar um novo usuário
    def create(self, validated_data):
        password = validated_data.pop('password') # Pop - Retira o campo password do dicionário validated_data e armazena seu valor na variável password
        user_type = validated_data.get('type')

        user = User(**validated_data)
        user.set_password(password)

        # Sincroniza o perfil com as permissões nativas do Django.
        if user_type == User.ChoicesType.SUPERUSER:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        user.save()

        return user

    # Método é responsável por atualizar um usuário já existente
    def update(self, instance, validated_data):
            password = validated_data.pop('password', None)

            for attribute, value in validated_data.items():
                setattr(instance, attribute, value)

            if password:
                instance.set_password(password)

            # Atualiza as permissões caso o tipo seja alterado.
            if instance.type == User.ChoicesType.SUPERUSER:
                instance.is_superuser = True
                instance.is_staff = True
            else:
                instance.is_superuser = False
                instance.is_staff = False

            instance.save()

            return instance
