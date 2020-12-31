from django.contrib import admin

# Register your models here.
from home.models import *
admin.site.register(contact)

admin.site.register(products)

admin.site.register(Orderitems)
admin.site.register(Order)
admin.site.register(ShippingOrder)
admin.site.register(Customer)
