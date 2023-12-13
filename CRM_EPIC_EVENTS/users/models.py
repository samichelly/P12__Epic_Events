from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE = [
    ('sales', 'SALES'),
    ('support', 'SUPPORT'),
    ('management', 'MANAGEMENT'),
]
    
    role = models.CharField(max_length=10, choices=ROLE)
    name = models.CharField(max_length=50)
    employee_number = models.CharField(max_length=20, unique=True)
    # email = models.EmailField(unique=True)
