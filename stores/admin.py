from django.db import models
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from .models import Order, OrderProduct

class QuantityInput(forms.TextInput):
    """Cambia el tamaño del input en el admin."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'style': 'width: 30px; text-align: center;'})  # Ajusta el tamaño

class PriceInput(forms.TextInput):
    """Cambia el tamaño del input en el admin."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'style': 'width: 70px; text-align: center;'})  # Ajusta el tamaño







class OrderProductInline(admin.TabularInline):
    """Permite visualizar los productos dentro de una orden en el admin con imagen y campos pequeños."""
    model = OrderProduct
    extra = 0
    readonly_fields = ('total', 'product_image')  # Agregamos el campo de vista previa


    formfield_overrides = {
        # Aplica un widget más pequeño a estos campos
        models.IntegerField: {'widget': QuantityInput()},  
        models.DecimalField: {'widget': PriceInput()},
    }




    def product_image(self, obj):
        """Muestra la imagen con enlace para abrir en nueva pestaña, verificando `images` y `image_alterna`"""
        image_url = None

        if obj.product:
            if hasattr(obj.product, 'images') and obj.product.images:
                image_url = obj.product.images.url
            elif hasattr(obj.product, 'image_alterna') and obj.product.image_alterna:
                image_url = obj.product.image_alterna.url if hasattr(obj.product.image_alterna, 'url') else obj.product.image_alterna

        if image_url:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>'
                '</a>', image_url, image_url
            )

        return "Sin imagen"

    product_image.short_description = "Imagen"
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'order_number', 'status', 'created_at')
    list_display_links = ('id','order_number', 'total', 'status', 'created_at')
    search_fields = ('id', 'status')
    list_filter = ('status', 'created_at')
    list_per_page = 10
    inlines = [OrderProductInline]  # Muestra los productos dentro de la orden
    readonly_fields = ('total', 'created_at')

admin.site.register(Order, OrderAdmin)
