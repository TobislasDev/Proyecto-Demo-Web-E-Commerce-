from django import forms
from .models import Categoria, Marca, Proveedores, Productos, Carrito, ListaDeseos, UsuarioCliente


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
    
    #AGREGAMOS UNA FUNCION PARA PODER LIMPIAR LOS DATOS y CONFIRMAR SI LAS CONTRASEÑAS COINCIDEN CORRECTAMENTE

    def clean(self):
        clened_data = super().clean()
        password = clened_data.get('password')
        confirm_password = clened_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden, VERIFICAR!")
        return clened_data

class ConfirmarUsuario(forms.Form):
    Usuario = forms.CharField(label="Ingrese el usuario", max_length=50),
    contraseña = forms.CharField(label="Ingrese su contraseña", max_length=50, widget=forms.PasswordInput)

#Vamos a generar un FOMULARIO para confirmar el usuario correspondiente a nuestro modelo Usuarios, para clientes.

class ConfirmarUsuarioCliente(forms.Form):
    email = forms.EmailField(label="Ingrese su email", max_length=100)
    contraseña = forms.CharField(label="Ingrese su contraseña", max_length=50, widget=forms.PasswordInput)

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