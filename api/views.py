from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import ValidationError

from .models import Environment, EquipmentModel, Microcontroller, Sensor, Reading, User
from .serializers import EnvironmentSerializer, EquipmentModelSerializer, MicrocontrollerSerializer, SensorSerializer, ReadingSerializer, UserSerializer
from .permissions import IsAdministratorOrReadOnly, IsSuperUserOrReadOnly

from rest_framework.filters import OrderingFilter #Import - funcionalidade extra 1

from rest_framework.decorators import action #Imports - funcionalidade extra 2
from django.utils import timezone
from datetime import timedelta
from django.db.models import OuterRef, Subquery

from django.db.models import Count, Avg, Min, Max #Imports - funcionalidade extra 3
from django.utils.dateparse import parse_date

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

    filter_backends = [OrderingFilter]

    ordering_fields = [
        'registration_date',
        'measured_value',
    ]

    ordering = ['-registration_date']

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
            readings = readings.filter(
                registration_date__date__gte=start_date
            )

        if end_date:
            readings = readings.filter(
                registration_date__date__lte=end_date
            )

        if location:
            readings = readings.filter(
                sensor__microcontroller__environment_id=location
            )

        if sensor_status:
            readings = readings.filter(
                sensor__status=sensor_status.upper()
            )

        if function:
            readings = readings.filter(
                sensor__function=function.lower()
            )

        return readings

    # 1. Consulta as leituras das últimas 24 horas
    @action(detail=False, methods=['get'], url_path='last-24-hours')
    def ultimas_24_horas(self, request):

        limite = timezone.now() - timedelta(hours=24)

        readings = self.get_queryset().filter(
            registration_date__gte=limite
        )

        readings = self.filter_queryset(readings)

        serializer = self.get_serializer(readings, many=True)

        return Response(serializer.data)

    # 2. Consulta somente a última leitura de cada sensor
    @action(detail=False, methods=['get'], url_path='latest-by-sensor')
    def ultima_por_sensor(self, request):

        ultima_leitura = Reading.objects.filter(
            sensor_id=OuterRef('sensor_id')
        ).order_by(
            '-registration_date',
            '-id'
        ).values('id')[:1]

        readings = self.get_queryset().filter(
            id=Subquery(ultima_leitura)
        )

        readings = self.filter_queryset(readings)

        serializer = self.get_serializer(readings, many=True)

        return Response(serializer.data)
    
    
    
    # 3. Resumo estatístico das leituras de um sensor
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):

        sensor_id = request.query_params.get('sensor')

        # Verifica se o sensor foi informado
        if not sensor_id:
            raise ValidationError({
                'sensor': 'Informe o ID do sensor.'
            })

        # Valida o ID do sensor
        try:
            sensor_id = int(sensor_id)
        except (ValueError, TypeError):
            raise ValidationError({
                'sensor': 'Informe um ID de sensor válido.'
            })

        # Verifica se o sensor existe
        if not Sensor.objects.filter(id=sensor_id).exists():
            raise ValidationError({
                'sensor': 'Sensor não encontrado.'
            })

        # Obtém as leituras do sensor
        readings = self.get_queryset().filter(
            sensor_id=sensor_id
        )

        # Datas opcionais
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            start_date = parse_date(start_date)

            if not start_date:
                raise ValidationError({
                    'start_date': 'Informe uma data válida no formato YYYY-MM-DD.'
                })

            readings = readings.filter(
                registration_date__date__gte=start_date
            )

        if end_date:
            end_date = parse_date(end_date)

            if not end_date:
                raise ValidationError({
                    'end_date': 'Informe uma data válida no formato YYYY-MM-DD.'
                })

            readings = readings.filter(
                registration_date__date__lte=end_date
            )

        # Verifica se a data inicial é anterior à final
        if start_date and end_date and start_date > end_date:
            raise ValidationError({
                'date': 'A data inicial não pode ser posterior à data final.'
            })

        # Calcula as estatísticas
        statistics = readings.aggregate(
            total_readings=Count('id'),
            minimum_value=Min('measured_value'),
            maximum_value=Max('measured_value'),
            average_value=Avg('measured_value')
        )

        return Response({
            'sensor': sensor_id,
            'start_date': start_date,
            'end_date': end_date,
            **statistics
        })




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrReadOnly] # Apenas SUPERUSER pode fazer CRUD de usuários
