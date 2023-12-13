from django.db import models
# from django.conf import settings
# from users import Collaborator

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    last_contact_date = models.DateField(auto_now=True)
    # sales_contact = models.ForeignKey(Collaborator, on_delete=models.CASCADE, related_name='customer_sales')

class Contract(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # sales_contact = models.ForeignKey(Collaborator, on_delete=models.CASCADE, related_name='contract_sales')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)

class Event(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_date_start = models.DateTimeField()
    event_date_end = models.DateTimeField()
    # support_contact = models.ForeignKey(Collaborator, on_delete=models.CASCADE, related_name='event_support')
    location = models.CharField(max_length=255)
    attendees = models.IntegerField()
    notes = models.TextField()
