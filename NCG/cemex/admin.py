from django.contrib import admin
from .models import Item, Attribute, Option
from .models import Order, Order_Item, Order_Item_Detail, Order_Address


# Register models in the admin tool:


admin.site.register(Item)
admin.site.register(Attribute)
admin.site.register(Option)

admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Order_Item_Detail)
admin.site.register(Order_Address)

