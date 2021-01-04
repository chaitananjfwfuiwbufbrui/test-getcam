from django.contrib import admin

# Register your models here.
from home.models import *
admin.site.register(contact)

# admin.site.register(products)

admin.site.register(Orderitems)
admin.site.register(Order)
admin.site.register(ShippingOrder)
admin.site.register(Customer)
admin.site.register(essential_details)


class postimageadmin(admin.StackedInline):
        model = images_fiels


@admin.register(products)
class postadmin(admin.ModelAdmin):
    inlines = [postimageadmin]
    class Meta:
        model = products

@admin.register(images_fiels)
class postimageadmin(admin.ModelAdmin):
    pass
