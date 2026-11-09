from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    class ChoicesType(models.TextChoices):
        SUPERUSER = "SUPERUSER", "Superuser"
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        USER = "USER", "User"

    name = models.CharField(max_length=100)

    email = models.EmailField(
        max_length=100,
        unique=True
    )

    type = models.CharField(
        max_length=45,
        choices=ChoicesType.choices,
        default=ChoicesType.USER
    )

    photo = models.ImageField(
        upload_to='users/',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

    
class Environment(models.Model):
    point = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'environment'
    
    def __str__(self):
        return self.name
    
class EquipmentModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'equipment_model'

    def __str__(self):
        return self.name
    
    
class Microcontroller(models.Model):
    class ChoicesStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
    
    mac_address = models.CharField(max_length=20, unique=True)
    
    latitude = models.DecimalField(max_digits=10,decimal_places=7,validators=[MinValueValidator(-90),MaxValueValidator(90)])

    longitude = models.DecimalField(max_digits=10,decimal_places=7,validators=[MinValueValidator(-180),MaxValueValidator(180)])
    
    observation = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=ChoicesStatus.choices,default=ChoicesStatus.ACTIVE)
    registration_date = models.DateTimeField(auto_now_add=True)
    equipment_model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT)
    
    environment = models.ForeignKey(Environment,on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'microcontroller'
    
    def __str__(self):
        return self.mac_address
    
    
class Sensor(models.Model):
    class ChoicesStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        
    class ChoicesFunction(models.TextChoices):
        TEMPERATURE = "temperature", "Temperature"
        HUMIDITY = "humidity", "Humidity"
        LUMINOSITY = "luminosity", "Luminosity"
        COUNTER = "counter", "Counter"

    class UnitMeasureament(models.TextChoices):
        CELSIUS = "°C", "Degrees Celsius"
        PERCENTAGE = "%", "Percentage"
        LUX = "lux", "Lux"
        UNIT = "un", "Units"

    function = models.CharField(
        max_length=20,
        choices=ChoicesFunction.choices
    )    
    
    model = models.CharField(max_length=50)
    unit_measureament = models.CharField(max_length=5,choices=UnitMeasureament.choices)
    status = models.CharField(max_length=50,choices=ChoicesStatus.choices,default=ChoicesStatus.ACTIVE)

    microcontroller = models.ForeignKey(Microcontroller,on_delete=models.PROTECT)

    class Meta:
        db_table = 'sensor'

    def __str__(self):
        return self.model

class Reading (models.Model):
    registration_date = models.DateTimeField()
    sensor = models.ForeignKey( Sensor, on_delete=models.PROTECT)
    measured_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'reading'
    
    def __str__(self):
        return str(self.measured_value)
    
    