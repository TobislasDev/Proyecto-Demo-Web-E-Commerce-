from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.

#Procedemos a crear nuestros modelos, los cuales se convertiran en tablas en nuestra base de datos


class Categoria(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name="name")    

    def __str__(self):
        return self.descripcion 
    
class Marca(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")

    def __str__(self):
        return self.name
    
class Proveedores(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    descripcion = models.CharField(max_length=200, verbose_name="descripcion")
    telefono = models.CharField(max_length=200, verbose_name="Telefono", null=True, blank=True)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    direccion = models.TextField(verbose_name="Direccion", null=True, blank=True)

    def __str__(self):
        return self.name + ' - ' + self.descripcion

    
#Procedemos a generar una de las tablas importantes la de PRODUCTOS / STOCK
class Productos(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    descripcion = models.CharField(max_length=150, verbose_name="descripcion")
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True, verbose_name="Imagen_Principal")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="Productos", verbose_name="Marca")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="Productos", verbose_name="Categoria")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name="Productos", verbose_name="Proveedor")
    stock_min = models.DecimalField(max_digits=10,decimal_places=2,null=False, verbose_name="Stock_Minimo")
    stock_max = models.DecimalField(max_digits=10,decimal_places=2, null=False, verbose_name="Stock_Maximo")

    def __str__(self):
        return self.name + ' - ' + self.descripcion + ' - ' + self.categoria.descripcion +  ' - ' + self.marca.name + ' - ' + self.proveedor.name
    
#Procedemos a crear un modelo de imagenes adicionales, para poder tener varias imagenes del producto.
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="Imagenes_Adicionales", verbose_name="Producto")
    imagen = models.ImageField(upload_to="productos/otras_imagenes/", verbose_name="Imagenes Adicionales")

    def __str__(self):
        return f"Imagen de {self.producto.name}"

class Carrito(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Carrito", verbose_name="Id_Usuario")
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="Carrito", verbose_name="Producto")
    cantidad = models.PositiveBigIntegerField(default=1, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.id_usuario.username} - {self.producto.name}"

class ListaDeseos(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Id_Usuario", related_name="ListaDeseos")
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="ListaDeseos", verbose_name="Producto")
    cantidad = models.PositiveBigIntegerField(default=1, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.id_usuario.username} - {self.producto.name}"

#procedemos a generar las tablas de ventas, y detalle ventas

class Ventas(models.Model):
    #Generamos una lista con los distintos estados de una venta
    ESTADOS_VENTA = [ 
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Cancelado', 'Cancelado'),]
    
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Ventas", verbose_name='Id_Usuario')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha_Hora')
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='Total_Venta')
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS_VENTA,
        default='Pendiente',
        verbose_name='Estado'
    )
    def __str__(self):
        return f"Venta #: {self.id} - Usuario: {self.id_usuario.username} - Estado:{self.estado} - Total: {self.formato_total_venta()}"
    #CALCULAR EL TOTAL

    def calcular_total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())
    #Funcion, para formateo de miles en los totales.

    def formato_total_venta(self):
        return "{:,.0f}".format(self.total_venta)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name='DetalleVenta', verbose_name='Venta')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="DetalleVenta", verbose_name='Producto')
    cantidad = models.PositiveBigIntegerField(default=1, verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio_Unitario')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Subtotal')

    def __str__(self):
        return f"Venta #: {self.id} - Producto: {self.producto.name} - Subtotal: {self.formato_sub_total()}"
    
    #Formato de separador de miles

    def formato_precio_unitario(self):
        return "{:,.0f}".format(self.precio_unitario)
    
    def formato_sub_total(self):
        return "{:,.0f}".format(self.subtotal)
    

#Añadimos los modelos para Usuario Clientes

class UsuarioCliente(AbstractUser):

    user= models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name="usuario_cliente",
        verbose_name="Usuario"
    )
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", null=True, blank=True)
    direccion = models.TextField(verbose_name="Dirección", null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    #Generamos un diccionario para las opciones de Genero
    genero=models.CharField(
        max_length=1,
        choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otros")],
        null=True,
        blank=True,
        verbose_name="Género"
    )
    verificado = models.BooleanField(default=False, verbose_name="Correo Verificado")
    foto_perfil= models.ImageField(upload_to="Usuarios/", null=True, blank=True)

    # Procedemos con modificar las relaciones de permisos y grupos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="usuario_cliente_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_cliente_permissions',
        blank=True
    )

    #Funciones
    #Actualizar direccion
    def actualizar_direccion_principal(self, nueva_direccion):
        self.direcciones.update(es_principal=False)
        nueva_direccion.es_principal=True
        nueva_direccion.save()
        

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.username})"
        
    class Meta:
        verbose_name = "Usuario Cliente"
        verbose_name_plural = "Usuarios Clientes"

class DireccionesEnvio(models.Model):
    TIPO_DIRECCION_CHOICES = [
        ('envio', 'Envío'),
        ('facturacion', 'Facturación'),
        ('trabajo', 'Trabajo')
    ]
    usuario_cliente= models.ForeignKey(
        UsuarioCliente,
        on_delete=models.CASCADE,
        related_name="direcciones",
        verbose_name="UsuarioCliente",
        null=True
    )
    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_DIRECCION_CHOICES,
        verbose_name="Tipo de Dirección"
    )
    es_principal = models.BooleanField(default=False, verbose_name="Es Principal")  
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Creación")

    #Funciones
    #Validamos una única dirección principal por usuario y tipo
    def clean(self):
        if self.es_principal:
            DireccionesEnvio.objects.filter(
                usuario_cliente=self.usuario_cliente,
                tipo=self.tipo,
                es_principal=True
            ).exclude(id=self.id).update(es_principal=False)
        super().clean()

    def marcar_como_principal(self):
        self.usuario_cliente.direcciones.filter(tipo=self.tipo).update(es_principal=False)
        self.es_principal = True
        self.save()

    @classmethod
    def obtener_principal(cls, usuario_cliente, tipo):
        return cls.objects.filter(usuario_cliente=usuario_cliente, tipo=tipo, es_principal=True).first()
    
    def __str__(self):
        usuario_cliente = self.usuario_cliente.username if self.usuario_cliente else "Sin Usuario"
        return f"{usuario_cliente} - {self.direccion}, {self.ciudad}, {self.departamento}"
    
    class Meta:
        verbose_name="Dirección de Envío"
        verbose_name_plural= "Direcciones de Envío"
        indexes = [
            models.Index(fields=['usuario_cliente', 'es_principal']),
            models.Index(fields=['tipo']),
        ]

#Añadimos los modelos adicionales, para metodos de pago, pedidos, ordenees.

