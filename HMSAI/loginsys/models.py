from django.db import models

class ContactMessages(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contactdata"
    
class Userlogin(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = "loginuserdata"


class PointaData11(models.Model):
    name = models.CharField(max_length=250)
    doctor_choices = [
        ('Cardiologist', 'Cardiologist'),
        ('Nephrologist', 'Nephrologist'),
        ('Oncologist', 'Oncologist'),
        ('Disease Specialist', 'Infectious Disease Specialist'),
        ('General Surgeon', 'General Surgeon'),
        ('Medicine Specialist', 'Internal Medicine Specialist'),
    ]
    doctor = models.CharField(max_length=20, choices=doctor_choices)
    time_slot_choices = [
        ('9AM', '9 AM'),
        ('10AM', '10 AM'),
        ('11AM', '11 AM'),
        ('12PM', '12 PM'),
        ('1PM', '1 PM'),
        ('2PM', '2 PM'),
        ('3PM', '3 PM'),
        ('4PM', '4 PM'),
        ('5PM', '5 PM'),
        ('6PM', '6 PM'),
    ]
    time_slot = models.CharField(max_length=4, choices=time_slot_choices)
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=15)
    
    class Meta:
        db_table = "appointdata1"


