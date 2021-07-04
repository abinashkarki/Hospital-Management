from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

# Create your models here.


departments = [('Cardiology', 'Cardiology'), ('Dermatology','Dermatology'), ('Immunology','Immunology'), ('Anesthesiology','Anesthesiology'), ('Emergency', 'Emergency')]
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True)
    department = models.CharField(max_length=50,choices=departments, default='Generalist')
    status = models.BooleanField(default= False)

    def __str__(self):
        return '{} ({})'.format(self.name, self.department)

class Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    patient_name = models.CharField(max_length=100)
    # doctor = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.TimeField()
    
    # def __str__(self):
    #     return '{}has an appointment with {} at {}'.format(self.patient_name, self.doctor, self.time)

class History(models.Model):
    name = models.CharField(max_length=100)
    img = models.FileField(upload_to='images/')
    