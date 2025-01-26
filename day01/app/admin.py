from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(category)
admin.site.register(unit)
admin.site.register(Item)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(Product)
