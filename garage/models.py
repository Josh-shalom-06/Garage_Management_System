from django.db import models
from datetime import date

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    experience=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name    

# Car Model
class Car(models.Model):
    customer = models.ForeignKey(Customer, related_name='cars', on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

# Service Record Model
class ServiceRecord(models.Model):
    car = models.ForeignKey(Car, related_name='service_records', on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic,related_name='service_records', on_delete=models.CASCADE,null=True)
    service_date = models.DateField()
    service_type = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car} - {self.service_type} ({self.service_date})"
    
# Invoice Model (new)
class Invoice(models.Model):
    service_record = models.OneToOneField(ServiceRecord, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice for {self.service_record.car} - {self.invoice_date}"

    # Calculate total amount of the service record
    def calculate_total(self):
        # You can add any logic here, like including taxes or additional fees
        self.total_amount = self.service_record.amount
        self.save()    

class stock(models.Model):
    partname = models.CharField(max_length=50, null=True)
    qty = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.CharField(max_length=100, null=True, blank=True)
    restock_date = models.DateField(null=True, blank=True)
    low_stock_threshold = models.IntegerField(default=5)  # Minimum stock level before alerting

    def __str__(self):
        return self.partname

    # Check if stock is low
    def is_low_stock(self):
        return self.qty <= self.low_stock_threshold

    # Calculate total value of the stock
    def total_stock_value(self):
        return self.qty * self.price if self.price else 0    

  