from django.contrib import admin
from .models import customer, Order

admin.site.register(customer)
admin.site.register(Order)

# Register your models here.
