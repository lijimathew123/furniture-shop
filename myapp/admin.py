from django.contrib import admin
from .models import FurnitureCategory,FurnitureProduct,ShoppingCart,CartItem,Order,Promotion,Review,BlogPost
# Register your models here.

admin.site.register(FurnitureCategory)
admin.site.register(FurnitureProduct)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)

admin.site.register(Review)
admin.site.register(Promotion)
admin.site.register(BlogPost)
