from django.contrib import admin
from . models import *

admin.site.register(Slider)
admin.site.register(Banner_Area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)


class Product_Images(admin.TabularInline):
    model = Product_Image
    
class Additional_Informations(admin.TabularInline):
    model = Additional_Information
    
class Product_Admin(admin.ModelAdmin):
    inlines = [Product_Images,Additional_Informations]
    list_display = ('product_name','price','categories','color','section')
    list_editable = ('categories','section','color')


admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)


admin.site.register(Color)

admin.site.register(Brand)
admin.site.register(CouponCode)



