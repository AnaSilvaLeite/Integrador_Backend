
import random

from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from api.models import Sensor, Reading


class Command(BaseCommand):

    help = 'Gera leituras simuladas para sensores ativos.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--quantity',
            type=int,
            default=10,
            help='Quantidade de leituras que serão geradas.'
        )

        parser.add_argument(
            '--sensor',
            type=int,
            help='ID de um sensor específico para gerar leituras.'
        )

    def handle(self, *args, **options):

        quantity = options['quantity']
        sensor_id = options['sensor']

        if quantity <= 0:
            raise CommandError(
                'A quantidade deve ser maior que zero.'
            )

        # Busca sensores ativos com microcontroladores ativos
        sensors = Sensor.objects.filter(
            status='ACTIVE',
            microcontroller__status='ACTIVE'
        ).select_related('microcontroller')

        # Caso seja informado um sensor específico
        if sensor_id is not None:
            sensors = sensors.filter(id=sensor_id)

        sensors = list(sensors)

        if not sensors:
            raise CommandError(
                'Nenhum sensor ativo disponível para gerar leituras.'
            )

        generated = 0

        for i in range(quantity):

            sensor = random.choice(sensors)

            # Gera um valor conforme a função do sensor
            if sensor.function == 'temperature':
                value = random.uniform(15, 40)

            elif sensor.function == 'humidity':
                value = random.uniform(30, 90)

            elif sensor.function == 'luminosity':
                value = random.uniform(100, 1000)

            elif sensor.function == 'counter':
                value = random.randint(0, 100)

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Função desconhecida no sensor {sensor.id}.'
                    )
                )
                continue

            measured_value = Decimal(str(value)).quantize(
                Decimal('0.01')
            )

            registration_date = timezone.now()

            # Evita criar uma leitura duplicada
            reading, created = Reading.objects.get_or_create(
                sensor=sensor,
                registration_date=registration_date,
                measured_value=measured_value
            )

            if created:
                generated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{generated} leituras simuladas geradas com sucesso!'
            )
        )
