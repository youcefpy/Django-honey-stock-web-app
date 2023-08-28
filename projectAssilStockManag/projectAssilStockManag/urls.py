from django.contrib import admin
from django.urls import path
from appAssilStockManag.views import add_honey_product, add_product_batch,list_products
from appAssilStockManag.views import delete_product, delete_batch,add_jar,add_jar_batch,add_filled_jar,list_jars,list_jars_filled,delete_jar,delete_jar_batch,add_ticket
from appAssilStockManag.views import list_tickets,add_batch_ticket,delete_ticket_batch,delete_ticket, add_box,add_box_batch,list_box,delete_box,delete_box_batch,add_fill_box,list_filled_boxes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product/', add_honey_product, name='add_honey_product'),
    path('add_product_batch/', add_product_batch, name='add_product_batch'),
    path('list_products/',list_products, name='list_products'),
    path('delete_product/<int:product_id>',delete_product,name='delete_product'),
    path('delete_batch/<int:batch_id>/', delete_batch, name='delete_batch'),
    path('add_jar/', add_jar, name='add_jar'),
    path('add_jar_bacth/',add_jar_batch,name='jars_batch'),
    path('add_filled_jar/',add_filled_jar,name='add_filled_jar'),
    path('list_jar/',list_jars,name="list_jars"),
    path("list_filled_jars/", list_jars_filled, name="list_filled_jars"),
    path('delete_jar/<int:jar_id>',delete_jar,name="delete_jar"),
    path('delete_jar_batch/<int:batch_id>',delete_jar_batch,name="delete_jar_batch"),
    path('add_ticket/',add_ticket,name='add_ticket'),
    path('add_batch_ticket/',add_batch_ticket,name='add_batch_ticket'),
    path('list_tickets/',list_tickets,name='list_tickets'),
    path('delete_ticket/<int:ticket_id>',delete_ticket,name="delete_ticket"),
    path('delete_ticket_batch/<int:batch_id>',delete_ticket_batch,name="delete_ticket_batch"),
    path('add_box/',add_box,name='add_box'),
    path('add_box_batch/',add_box_batch,name='add_box_batch'),
    path('list_box/',list_box,name='list_box'),
    path('delete_box/<int:box_id>',delete_box,name='delete_box'),
    path('delete_box_batch/<int:batch_id>',delete_box_batch,name='delete_box_batch'),
    path('add_fill_box/',add_fill_box,name='add_fill_box'),
    path('list_filled_boxes/', list_filled_boxes, name='list_filled_boxes'),     
]
