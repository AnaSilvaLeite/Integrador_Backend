
from rest_framework import serializers
from .models import Environment, EquipmentModel, Microcontroller, Sensor, Reading, User
from django.contrib.auth.password_validation import validate_password

class EnvironmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Environment
        fields = '__all__'
        
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
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
