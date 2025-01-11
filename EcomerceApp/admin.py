from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Marca, Categoria, Productos, Proveedores, Carrito, ListaDeseos, Ventas, DetalleVenta, UsuarioCliente, DireccionesEnvio, ImagenProducto
from django.utils.translation import gettext_lazy as _

# Register your models here.

admin.site.site_header= _("Panel de Administración E-Comerce")
#admin.site.site_title= _("")
admin.site.index_title= _("Gestión E-comerce")

#CONFIGURAMOS EL PANEL DE BUSQUEDA, DE TAL MODO A PODER FACILITAR LA MENERA EN QUE BUSCAMOS DATOS DESDE EL ADMIN

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display= ('id', 'datos') #Con list_display podemos editar lo que queremos mostrar en nuestra pantalla de ADMIN
    search_fields = ('id', 'name') #Con search_fields, habilitamos un label de busqueda, y editamos como podemos buscar los datos
    #list_editable = ('datos',)#Con list_editable seleccionamos en pantalla lo que podemos editar sin necesidad de ingresar dentro del dato, desde la pantalla principal
    list_per_page = 3 #Con list_per_page seleccionamos cuantos datos queremos mostrar por pagina, lo que hara que nos genere paginas que solo muestren la cantidad de datos seleccionados
   
    #Ahora agregaremos una funcion, que nos mostrara en pantalla las marcas pero en mayusculas.
    def datos(self, obj):
        return obj.name.upper()
    datos.short_description = "MARCAS" #Damos un titulo al campo donde indican los nombres 
    datos.empty_value_diplay = "???" #Si tenemos datos vacios, en pantalla apareceran ???
    datos.admin_order_field = "name" #Ordenamos los datos teniendo en cuenta la casilla name


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display= ('id', 'descripcion',)
    search_fields=('id','descripcion',)
    list_editable=('descripcion',)
    list_per_page = 3

class ImagenProductoAdmin(admin.TabularInline):
    model = ImagenProducto
    extra = 1


@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'datos', 'stock_min', 'stock_max', 'precio')
    search_fields=('id', 'name')
    list_per_page = 3
    list_filter = ('marca',)
    inlines = [ImagenProductoAdmin]
     #Vamos a adherir un advance option, con fieldsets lo que haremos sera, no habilitar a primera los distintos datos que corresponden al modelo producto en pantalla, para poder observar los demas datos, tendremos que dar click en advance option y con ello se nos desplegaran los demas datos para poder modificarlos
    fieldsets = (
        (None , {
            'fields': ('name',)
        }),
        ('Advanced options', {
            'classes':('collapse', 'wide', 'extrapretty'),
            'fields': ('descripcion','imagen','precio','marca','categoria','proveedor','stock_min', 'stock_max')
        })
    )
    def datos(self, obj):
        return obj.name.upper()
    datos.short_description = "PRODUCTOS" 
    datos.empty_value_diplay = "???" 
    datos.admin_order_field = "name" 

@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display=('id', 'datos', 'descripcion')
    search_fields=('id', 'name')
    list_per_page = 3
    list_filter = ('descripcion',)

    fieldsets= (
        (None, {
            'fields': ('name',)
        }),
        ('Advanced options', {
            'classes': ('collapse', 'wide', 'extrapretty'),
            'fields':['descripcion']
        })

    )
    def datos(self, obj):
        return obj.name.upper()
    datos.short_description = "PROVEEDORES" 
    datos.empty_value_diplay = "???" 
    datos.admin_order_field = "name" 

#Llamamos a los modelos de Venta, Venta detalle

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display=('id', 'id_usuario','fecha', 'total_venta', 'estado')
    search_fields=('id','fecha', 'id_usuario')
    list_per_page= 10
    list_filter=('fecha',)
    list_editable=('estado',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display=('id', 'venta','producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('id', 'producto', 'venta')
    list_per_page = 10
    list_filter=('id', 'venta', )

#VERIFICACION DE USUARIOS Y DIRECCIONES EN EL PANEL DE ADMINISTRADOR
class UsuarioClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'direccion')
    list_filter = ('username', 'email', 'groups')
    search_fields = ('user__username', 'user__email', 'first_name', 'telefono')
    ordering = ('user__username', )

    fieldsets=(
        (None, {'fields':('user',)}),
        ('Informacion Adicional',{
            'fields': ('telefono', 'direccion'),
        }),
    )

class DireccionesEnvioAdmin(admin.ModelAdmin):
    list_display = ('usuario_cliente', 'direccion', 'ciudad', 'departamento', 'tipo', 'es_principal', 'fecha_creacion')
    list_filter = ('tipo', 'es_principal', 'fecha_creacion')
    search_fields = ('usuario_cliente__user__username', 'direccion', 'ciudad', 'departamento')


admin.site.register(UsuarioCliente, UsuarioClienteAdmin)
admin.site.register(DireccionesEnvio, DireccionesEnvioAdmin)
admin.site.register(ImagenProducto)

