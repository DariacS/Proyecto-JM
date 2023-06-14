from django.contrib import admin
from .models import *

# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','descripcion','tipo','fechagregado','fechamodificado']
    search_fields = ['nombre']
    list_per_page = 5


class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombrecompleto','apellidos','correo','numerotelefono']
    search_fields = ['nombrecompleto']

admin.site.register(TipoProducto)
admin.site.register(Producto, ProductosAdmin)
admin.site.register(Suscripcion, SuscripcionAdmin)
admin.site.register(ItemCarrito)
admin.site.register(Historial)