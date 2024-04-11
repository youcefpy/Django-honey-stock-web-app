from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from appAssilStockManag.views import add_honey_product, add_product_batch,list_products,export_products_to_excel,export_jars_to_excel,export_tickets_excel,export_filled_jars_excel,export_boxes_to_excel,sku_search,add_sell_fill_box,list_sell_boxes,export_filled_boxes_excel, get_jars
from appAssilStockManag.views import delete_product, delete_batch,add_jar,add_jar_batch,add_filled_jar,list_jars,list_jars_filled,delete_jar,delete_jar_batch,add_ticket,delete_jar_batch,delete_filled_jar,list_sell_jars,add_sku,list_sku,update_product_batch
from appAssilStockManag.views import list_tickets,add_batch_ticket,delete_ticket_batch,delete_ticket, add_box,add_box_batch,list_box,delete_box,delete_box_batch,add_fill_box,list_filled_boxes,main,delete_filled_box,add_sell_fill_jars,signup
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', RedirectView.as_view(pattern_name='login')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup, name='signup'),
    path('admin/', admin.site.urls),
    path('',main,name='main'),
    path('add_product/', add_honey_product, name='add_honey_product'),
    path('add_product_batch/', add_product_batch, name='add_product_batch'),
    path('list_products/',list_products, name='list_products'),
    path('update_product_batch/<int:batch_id>/', update_product_batch, name='update_product_batch'),    
    path('delete_product/<int:product_id>',delete_product,name='delete_product'),
    path('delete_batch/<int:batch_id>/', delete_batch, name='delete_batch'),
    path('export-products-to-excel/', export_products_to_excel, name='export_products_to_excel'),
    path('add_jar/', add_jar, name='add_jar'),
    path('add_jar_bacth/',add_jar_batch,name='jars_batch'),
    path('add_filled_jar/',add_filled_jar,name='add_filled_jar'),
    path('list_jar/',list_jars,name="list_jars"),
    path("list_filled_jars/", list_jars_filled, name="list_filled_jars"),
    path('export-filled-jars-excel',export_filled_jars_excel,name='export_filled_jars_excel'),
    path('delete_jar/<int:jar_id>',delete_jar,name="delete_jar"),
    path('delete_jar_batch/<int:batch_id>/',delete_jar_batch,name='delete_jar_batch'),
    path('export-jars-to-excel/',export_jars_to_excel,name='export_jars_to_excel'),
    path('add_ticket/',add_ticket,name='add_ticket'),
    path('add_batch_ticket/',add_batch_ticket,name='add_batch_ticket'),
    path('list_tickets/',list_tickets,name='list_tickets'),
    path('delete_ticket/<int:ticket_id>',delete_ticket,name="delete_ticket"),
    path('delete_ticket_batch/<int:batch_id>',delete_ticket_batch,name="delete_ticket_batch"),
    path('export-tickets-excel',export_tickets_excel,name='export_tickets_excel'),
    path('add_box/',add_box,name='add_box'),
    path('add_box_batch/',add_box_batch,name='add_box_batch'),
    path('list_box/',list_box,name='list_box'),
    path('delete_box/<int:box_id>',delete_box,name='delete_box'),
    path('delete_box_batch/<int:batch_id>',delete_box_batch,name='delete_box_batch'),
    path('export-boxes-to-excel/', export_boxes_to_excel, name='export_boxes_to_excel'),
    path('add_fill_box/',add_fill_box,name='add_fill_box'),
    path('list_filled_boxes/', list_filled_boxes, name='list_filled_boxes'),  
    path('delete_filled_box/<int:fill_box_id>',delete_filled_box,name='delete_filled_box'),
    path('export-filled-boxes-excel/',export_filled_boxes_excel,name='export_filled_boxes_excel'),
    path('delete_filled_jar/<int:filled_jar_id>/', delete_filled_jar, name='delete_filled_jar'),
    path('add_sku/',add_sku,name='add_sku'),
    path('list_sku/',list_sku,name='list_sku'),
    path('add_sell_filled_jars/',add_sell_fill_jars,name='add_sell_filled_jars'),
    path('list_sell_jars/',list_sell_jars,name='list_sell_jars'),
    path('list-sell-box',list_sell_boxes,name='list_sell_boxes'),
    path('api/skus/', sku_search, name='sku_search'),
    path('add-sell-filled-box',add_sell_fill_box,name='add_sell_fill_box'),
    path('get_jars/', get_jars, name='get_jars'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)