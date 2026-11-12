from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import ValidationError

from .models import Environment, EquipmentModel, Microcontroller, Sensor, Reading, User
from .serializers import EnvironmentSerializer, EquipmentModelSerializer, MicrocontrollerSerializer, SensorSerializer, ReadingSerializer, UserSerializer
from .permissions import IsAdministratorOrReadOnly, IsSuperUserOrReadOnly


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'erro': 'Não é possível excluir este registro porque existem registros relacionados.'},
                status=status.HTTP_409_BAD_REQUEST
            )


class EquipmentModelViewSet(viewsets.ModelViewSet):
    queryset = EquipmentModel.objects.all()
    serializer_class = EquipmentModelSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'erro': 'Não é possível excluir este registro porque existem registros relacionados.'},
                status=status.HTTP_409_BAD_REQUEST
            )



class MicrocontrollerViewSet(viewsets.ModelViewSet):
    queryset = Microcontroller.objects.all()
    serializer_class = MicrocontrollerSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def get_queryset(self):
        microcontrollers = Microcontroller.objects.all()

        status_filter = self.request.query_params.get('status')

        if status_filter:
            status_filter = status_filter.upper()

            valid_status = [
                choice.value
                for choice in Microcontroller.ChoicesStatus
            ]

            if status_filter not in valid_status:
                raise ValidationError({
                    'status': 'Status inválido. Utilize ACTIVE ou INACTIVE.'
                })

            microcontrollers = microcontrollers.filter(
                status=status_filter
            )

        return microcontrollers

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'erro': 'Não é possível excluir este registro porque existem registros relacionados.'
                },
                status=status.HTTP_409_CONFLICT
            )


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def get_queryset(self):
        sensors = Sensor.objects.all()

        status_filter = self.request.query_params.get('status')

        if status_filter:
            status_filter = status_filter.upper()

            valid_status = [
                choice.value
                for choice in Sensor.ChoicesStatus
            ]

            if status_filter not in valid_status:
                raise ValidationError({
                    'status': 'Status inválido. Utilize ACTIVE ou INACTIVE.'
                })

            sensors = sensors.filter(
                status=status_filter
            )

        return sensors

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'erro': 'Não é possível excluir este registro porque existem registros relacionados.'
                },
                status=status.HTTP_409_CONFLICT
            )


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [IsAdministratorOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'options']


    def get_queryset(self):
        readings = Reading.objects.all()

        sensor_id = self.request.query_params.get('sensor')
        date = self.request.query_params.get('data')
        start_date = self.request.query_params.get('data_inicio')
        end_date = self.request.query_params.get('data_fim')
        location = self.request.query_params.get('local')
        sensor_status = self.request.query_params.get('status')
        function = self.request.query_params.get('function')

        if sensor_id:
            readings = readings.filter(sensor_id=sensor_id)

        if date:
            readings = readings.filter(registration_date__date=date)

        if start_date:
            readings = readings.filter(registration_date__date__gte=start_date)

        if end_date:
            readings = readings.filter(registration_date__date__lte=end_date)

        if location:
            readings = readings.filter(
                sensor__microcontroller__environment_id=location
            )

        if sensor_status:
            readings = readings.filter(sensor__status=sensor_status.upper())

        if function:
            readings = readings.filter(sensor__function=function.lower())

        return readings



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrReadOnly]
