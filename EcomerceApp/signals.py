from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetalleVenta, Productos, Ventas

#Una vez importamos los modulos requeridos, procedemos con la logica de actualizar stock.

#Funcion para actualizar el stock, cada que agreguemos un detalle de venta, esta funcion actualizara el stock de los productos.
@receiver(post_save, sender=DetalleVenta)
def actualizar_stock(sender, instance, created, **kwargs):
    producto = instance.producto
    
    if created:
        try: 
            if producto.stock_max < instance.cantidad:
                raise ValueError(f"No hay suficiente stock para el producto '{producto.name}'. Stock disponible: {producto.stock_max}, solicitado: {instance.cantidad}")
            producto.stock_max -= instance.cantidad
            producto.save() 
        except Exception as e:
            print(f"Error al actualizar el stock: {e}")




#Funcion para restaurar productos, caso contrario al anterior, si eliminamos detalles de ventas, tendremos que restaurar los productos.

@receiver(post_delete, sender=DetalleVenta)
def restaurar_stock(sender, instance, **kwargs):
    producto = instance.producto

    try:
        producto.stock_max += instance.cantidad
        producto.save()
    except Exception as e:
        print(f"Error al restaurar el stock: {e}")
        
    