from django.db import models
from accounts.models import Account, Address
from products.models import Product
from django.db.models import Sum


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADO', 'Aceptado'),
        ('DESPACHADO', 'Despachado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
        ('RECHAZADO', 'Rechazado'),
        ('DEVUELTO', 'Devuelto')
    )

    client = models.CharField(max_length=100, blank=True, db_index=True, default='CLIENTES VARIOS', verbose_name='Cliente')
    order_number = models.CharField(max_length=10, verbose_name='pedido')
    # user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Usuario')
    # order_note = models.CharField(max_length=100, blank=True, verbose_name='Nota de pedido')
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name='Total')  # Se cambió a DecimalField
    status = models.CharField(max_length=10, choices=STATUS, default='PENDIENTE', verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    def __str__(self):
        return self.client if self.client else "Pedido sin cliente"

    def update_total(self):
        """Calcula y actualiza el total del pedido sumando los totales de los productos asociados."""
        total_items = self.orderproduct_set.aggregate(total=Sum('total'))['total'] or 0.00
        self.total = total_items
        self.save(update_fields=['total'])

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ('-created_at',)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderproduct_set', verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')  # Se cambió a PositiveIntegerField para evitar negativos
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio')  # Se cambió a DecimalField
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name='Total')
    ordered = models.BooleanField(default=False, verbose_name='DPCD')

    def __str__(self):
        return self.product.name_extend if self.product else "Producto sin nombre"

    def save(self, *args, **kwargs):
        """Calcula el total del ítem antes de guardarlo y actualiza el total del pedido."""
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
        self.order.update_total()  # Actualiza el total del pedido cada vez que se guarda un OrderProduct

    class Meta:
        verbose_name = "Producto del Pedido"
        verbose_name_plural = "Productos del Pedido"
        
