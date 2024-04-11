from django.contrib import admin
from .models import HoneyProduct,ProductBatch, Box,BoxBatch,FilledJar,Jar,Ticket, TicketBatch,FilledBox,Sku,SoldFilledJar,SoldFilledBox



class HoneyProductAdmin(admin.ModelAdmin):
    list_display = ('name_product', 'quantity_in_the_stock', 'date_entry')
    search_fields = ('name_product',)

class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ('product','date_received','quantity_received','price_per_kg')
    search_fields = ('product',)

class JarAdmin(admin.ModelAdmin):
    list_display = ('size', 'quantity_in_the_stock')

class JarBatchAdmin(admin.ModelAdmin):
    list_display = ('jar', 'date_received', 'quantity_received', 'price_jar')

class FilledJarAdmin(admin.ModelAdmin):
    list_display = ('jar','product','quantity_field','filled_date')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('type_ticket','product', 'quantity_in_the_stock', 'date_entry')
    list_filter = ('type_ticket',)
    search_fields = ('type_ticket',)

class TicketBatchAdmin(admin.ModelAdmin):
    list_display = ('ticket','quantity_received','purchase_price')

class BoxAdmin(admin.ModelAdmin):
    list_display = ('type_box', 'quantity_in_stock')

class BoxBatchAdmin(admin.ModelAdmin):
    list_display = ('box','quantity_received','purchase_price')

class FilledBoxAdmin(admin.ModelAdmin):
    list_display = ['box_type']
    

class SkuAdmin(admin.ModelAdmin):
    list_display=('code','title')

class SoldFilledJarAdmin(admin.ModelAdmin):
    list_display=['filled_jar','quantity_sell_jars','price_sell']

class SoldFilledBoxAdmin(admin.ModelAdmin):
    list_display=['filled_box','quantity_sell_box','price_sell']

admin.site.register(HoneyProduct,HoneyProductAdmin)
admin.site.register(ProductBatch,ProductBatchAdmin)
admin.site.register(Jar,JarAdmin)
admin.site.register(FilledJar,FilledJarAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Box,BoxAdmin)
admin.site.register(BoxBatch,BoxBatchAdmin) 
admin.site.register(FilledBox,FilledBoxAdmin)
admin.site.register(Sku,SkuAdmin)
admin.site.register(SoldFilledJar,SoldFilledJarAdmin)
admin.site.register(SoldFilledBox,SoldFilledBoxAdmin)

