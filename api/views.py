
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

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
                status=status.HTTP_400_BAD_REQUEST
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
                status=status.HTTP_400_BAD_REQUEST
            )


class MicrocontrollerViewSet(viewsets.ModelViewSet):
    queryset = Microcontroller.objects.all()
    serializer_class = MicrocontrollerSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'erro': 'Não é possível excluir este registro porque existem registros relacionados.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdministratorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'erro': 'Não é possível excluir este registro porque existem registros relacionados.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [IsAdministratorOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        queryset = Reading.objects.all()

        sensor = self.request.query_params.get('sensor')
        data = self.request.query_params.get('data')
        local = self.request.query_params.get('local')
        status = self.request.query_params.get('status')
        function = self.request.query_params.get('function')

        if sensor:
            queryset = queryset.filter(sensor_id=sensor)

        if data:
            queryset = queryset.filter(registration_date__date=data)

        if local:
            queryset = queryset.filter(
                sensor__microcontroller__environment_id=local
            )

        if status:
            queryset = queryset.filter(sensor__status=status.upper())

        if function:
            queryset = queryset.filter(sensor__function=function.lower())

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrReadOnly]
