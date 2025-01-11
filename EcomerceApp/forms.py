from django import forms
from django.contrib.auth.models import User
from .models import Categoria, Marca, Proveedores, Productos, Carrito, ListaDeseos, UsuarioCliente, DireccionesEnvio, Ventas, DetalleVenta


#CREAMOS NUESTROS DISTINTOS FORMULARIOS

class CrearProductos(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['name', 'descripcion', 'marca', 'categoria', 'precio', 'imagen', 'stock_min', 'stock_max', 'proveedor']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'categoroa': forms.Select(attrs={'class':'form-control'}),
            'precio': forms.NumberInput(attrs={'class':'form-control','step':'0.01','min': '0'}),
            'imagen': forms.ImageField(label="IMG", required=False, widget=forms.FileInput(attrs={'class': 'form-control'})),
            'stock_min':forms.NumberInput(attrs={'class':'form-control','step':'1','min': '1'}),
            'stock_max':forms.NumberInput(attrs={'class':'form-control','step':'1','min': '1'}),
            'proveedor': forms.Select(attrs={'class':'form-control'})

#IMPORTANTE PARA AGREGAR IMAGENES A NUESTRO FORMULARIO DEBEMOS DE USAR EL WIDGETS ClearableFileInput

        }

        labels = {
            'name':'Agrega el nombre del producto',
            'descripcion':'Ingresa un breve detalle acerca del produco',
            'marca':'Marca',
            'categoroa':'Categoria',
            'precio':'Precio',
            'imagen':'Imagen',
            'stock_min':'Stock Min',
            'stock_max':'Stock Max',
            'proveedor':'Proveedor'

        }

#FUNCION PARA CORROBORAR QUE EL USUARIO NO DEJE SALDO NEGATIVO MENOR A 0 
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            forms.ValidationError('El precio debe ser mayor a 0')
        return precio
    
class CrearUsuario(forms.Form):
    nombre = forms.CharField(
        label="Usuario", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellido = forms.CharField(
        label="Apellido", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email", 
        max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="Usuario",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña", 
        max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirmar contraseña", 
        max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        widget=forms.DateInput(attrs={'class':'form-control', 'type': 'date'})
    )
    #procedemos a validar que no se permita usar el mismo Username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya ésta en uso')
        return username

    #AGREGAMOS UNA FUNCION PARA PODER LIMPIAR LOS DATOS y CONFIRMAR SI LAS CONTRASEÑAS COINCIDEN CORRECTAMENTE
    def clean(self):
        clened_data = super().clean()
        password = clened_data.get('password')
        confirm_password = clened_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden, VERIFICAR!")
        return clened_data

#Formulario para editar el perfil de usuario
class EditarPerflForm(forms.ModelForm):
    #Agregamos los campos adicionales del Usuario Cliente, para poder guardar
    telefono = forms.CharField(
        label="Telefono",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    genero = forms.ChoiceField(
        label="Género",
        choices=[("M", "Masculino"), ("F", "Fenemino"), ("O", "Otros")],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    direccion = forms.CharField(
        label="Direccion",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets ={
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        usuario_cliente = kwargs.pop('usuario_cliente', None)  # Extraer 'usuario_cliente'
        super().__init__(*args, **kwargs)  # Llamar al constructor base
        if usuario_cliente:
            self.fields['telefono'].initial = usuario_cliente.telefono
            self.fields['fecha_nacimiento'].initial = usuario_cliente.fecha_nacimiento
            self.fields['genero'].initial = usuario_cliente.genero
    
#Formulario para las direcciones del UsuarioCliente
class DireccionesEnvioForm(forms.ModelForm):
    model = DireccionesEnvio
    fields = ['direccion', 'ciudad', 'departamento', 'tipo', 'es_principal']
    widgets = {
        'direccion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'ciudad': forms.TextInput(attrs={'class':'form-control'}),
        'departamento':forms.TextInput(attrs={'class':'form-control'}),
        'tipo':forms.Select(attrs={'class':'form-select'}),
        'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
    labels = {
        'direccion':'Dirección',
        'ciudad':'Ciudad',
        'departamento':'Departamento',
        'tipo':'Tipo de Dirección',
        'es_principal':'¿Es principal?',
    }
class ConfirmarUsuario(forms.Form):
    usuario = forms.CharField(
        label='Usuario o Email',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario o email', 'class': 'form-control'})
    )
    contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña', 'class': 'form-control'})
    )


#Vamos a generar un FOMULARIO para confirmar el usuario correspondiente a nuestro modelo UsuarioCliente

class ConfirmarUsuarioCliente(forms.Form):
    usuario = forms.CharField(
       label='Usuario o Email',
       max_length=150,
       widget=forms.TextInput(attrs={'placeholder':'Ingresa tu usuario o email'})
   )
    contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder':'Ingresa tu contraseña'})
    
    )
    
#Formulario para UsuarioCliente el cual se diferencia de USER

class UsuarioClienteForm(forms.ModelForm):
    class Meta:
        model = UsuarioCliente
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'telefono', 'direccion', 'fecha_nacimiento', 'genero', 'foto_perfil']

    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], required=False)

#Procedemos a generar los formularios para el detalle de la venta/Finalizar compra

class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = ('id_usuario', 'total_venta')
    
        #fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
        total_venta = forms.CharField(widget=forms.CharField)


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    
        venta = forms.CharField(widget=forms.CharField)
        producto = forms.CharField(widget=forms.Textarea)
        cantidad = forms.CharField(widget=forms.Textarea)
        precio_unitario=forms.DecimalField(widget=forms.DecimalField)
        subtotal = forms.DecimalField(widget=forms.DecimalField)

    
