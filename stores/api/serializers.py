from rest_framework.serializers import ModelSerializer
from stores.models import Order, OrderProduct


# from warehome.api.serializers import StockSerializer



class OrderDetailSerializer(ModelSerializer):
    # stock_data = StockSerializer(source='stock', read_only=True)
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'total', 'quantity', 'price', 'ordered']
        read_only_fields = ['id', 'total']
    


class OrderSerializer(ModelSerializer):
    order_details = OrderDetailSerializer(many=True, write_only=True)  # Solo en escritura
    products = OrderDetailSerializer(many=True, read_only=True, source='orderproduct_set')  # Para lectura

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total', 'status', 'created_at', 'updated_at', 'order_details', 'products']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Crear orden con productos relacionados."""
        order_details_data = validated_data.pop('order_details', [])  # Extraer detalles
        order = Order.objects.create(**validated_data)  # Crear la orden

        # Crear los detalles de la orden
        for detail in order_details_data:
            OrderProduct.objects.create(order=order, **detail)

        return order

    def update(self, instance, validated_data):
        """Actualizar orden y sus productos."""
        order_details_data = validated_data.pop('order_details', [])
        instance = super().update(instance, validated_data)  # Actualizar la orden

        # Limpiar detalles existentes y agregar los nuevos
        instance.orderproduct_set.all().delete()
        for detail in order_details_data:
            OrderProduct.objects.create(order=instance, **detail)

        return instance