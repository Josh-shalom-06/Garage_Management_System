from django.contrib import admin
from .models import Customer, Car, ServiceRecord,Mechanic,stock

admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(ServiceRecord)
admin.site.register(Mechanic)
admin.site.register(stock)
