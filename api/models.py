from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    choices_type = {       
        "SUPERUSER": "Superuser",
        "ADMINISTRATOR": "Administrator",
        "USER": "User"
    }
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    type = models.CharField(max_length=45, choices=choices_type)
    
    class Meta:
        db_table = 'user'
    
    def __str__(self):
        return self.name
    
class Environment(models.Model):
    point = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'environment'
    
    def __str__(self):
        return self.name
    
    
class Microcontroller(models.Model):
    choices_status = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive",
    }
    
    mac_address = models.CharField(max_length=20, unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    model = models.CharField(max_length=50)
    observation = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=choices_status)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    environment = models.ForeignKey(Environment,on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'microcontroller'
    
    def __str__(self):
        return self.mac_address
    
    
class Sensor(models.Model):
    choices_status = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive",
    }

    class UnitMeasureament(models.TextChoices):
        CELSIUS = "°C", "Degrees Celsius"
        PERCENTAGE = "%", "Percentage"
        LUX = "lux", "Lux"
        UNIT = "un", "Units"

    function = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    unit_measureament = models.CharField(max_length=5,choices=UnitMeasureament.choices
    )
    status = models.CharField(max_length=50, choices=choices_status)

    microcontroller = models.ForeignKey(Microcontroller,on_delete=models.PROTECT)

    class Meta:
        db_table = 'sensor'

    def __str__(self):
        return self.model

class Reading (models.Model):
    registration_date = models.DateTimeField(auto_now_add=True)
    sensor = models.ForeignKey( Sensor, on_delete=models.PROTECT)
    measured_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'reading'
    
    def __str__(self):
        return str(self.measured_value)
    
    