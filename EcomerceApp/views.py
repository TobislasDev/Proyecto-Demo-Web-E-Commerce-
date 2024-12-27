from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Productos, Categoria, Marca, Proveedores, Carrito, ListaDeseos, UsuarioCliente 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CrearProductos,CrearUsuario,ConfirmarUsuario, ConfirmarUsuarioCliente, UsuarioClienteForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q #Para poder mostrar busquedas avanzadas, leer documentacion para mas detalles

# Create your views here.

def index (request):
    return render(request, 'Index.html')

def perfil_usuario(request):
    return render(request, 'Perfil_Usuario.html')

def productos(request):
    query = request.GET.get('q', '')
    if query:
        productos = Productos.objects.filter(
            Q(name__icontains=query) | #Filtra por nombre
            Q(descripcion__icontains=query) | #Filtra por descripcion
            Q(categoria__descripcion__icontains=query) | #Filtra por categoria
            Q(marca__name__icontains=query) #Filtra por marca
        )
    else:
        productos = Productos.objects.all() #Codigo ORM para mostrar todos los productos

    return render (request, 'Productos.html', {
        'productos': productos,
        'query': query #Pasamos el termino de busqueda a la plantilla para ser mostrado
    })

def detalle_producto(request, id):

    producto = get_object_or_404(Productos, id=id)
    
    productos_relacionados = Productos.objects.filter(
        categoria = producto.categoria
    ).exclude(id=producto.id)[:8]
    return render (request, 'Detalle_Producto.html',
                   {'producto': producto,
                   'productos_relacionados': productos_relacionados})


#Procedemos con la creacion de la vista para poder crear usuarios

def Crear_Usuario(request):
    if request.method == 'POST':

        form_usuario = CrearUsuario(request.POST)
        print(request.POST)#Para confirmar que datos nos da importante imprimir en pantalla y confirmarlo
        if form_usuario.is_valid():

            nombre= form_usuario.cleaned_data['nombre']
            apellido = form_usuario.cleaned_data['apellido']
            email = form_usuario.cleaned_data['email']
            password = form_usuario.cleaned_data['password']    
            confirm_password = form_usuario.cleaned_data['confirm_password']

            if password != confirm_password:
                return render (request, 'Crear_Usuario.html', 
                               {'form_usuario': form_usuario, 'error':'Las contraseñas con coinciden, VERIFICAR!'})
            if not UsuarioCliente.objects.filter(nombre=nombre).exists():
                usuario = UsuarioCliente.objects.create(
                    nombre = nombre,
                    apellido = apellido,
                    email = email,
                    password = make_password(password)
                )
                usuario.save()
                messages.success(request, 'Usuario creado correctamente!')
                return redirect('login.html')
            
            else:
                return render(request,'Crear_Usuario.html',{
                    'form_usuario': form_usuario,
                    'error': 'El nombre de usuario ya existe!'
                })
    else:
        form_usuario = CrearUsuario()
        return render(request, 'Crear_Usuario.html',{
            'form_usuario': form_usuario
        })
    
#ESTA FUNCION CORRESPONDE A LA CREACION DE USUARIOCLIENTE DIFERENTE DE LA FUNCION ANTERIOR

def crear_usuario_cliente (request):

    if request.method == 'POST':
        form = UsuarioClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente!')
            return redirect('Index.html') #debe de redireccionar a la pagina del perfil de usuario
    else:
        form = UsuarioClienteForm() 

    return render(request, 'Crear_Usuario_Form.html',{'form': form})

#Esta funcion para login_ingreso, es para validar los datos, pero ya con el model user predeterminado de Django.

def login_ingreso(request):
    if request.method == 'POST':
        formulario_login = ConfirmarUsuario(request.POST)
        if formulario_login.is_valid():
            usuario = formulario_login.cleaned_data['usuario']
            contraseña = formulario_login.cleaned_data['contraseña']
            usuario = authenticate(usuario,contraseña=contraseña)
            if usuario is not None:
                login(request, usuario)
                return redirect('Index')
    else:
        formulario_login = ConfirmarUsuario()
        return render(request, 'login.html', {
            'formulario_login': formulario_login
        })
#////////////////////////////////////////////////////
#Ahora procedemos a generar una vista, para poder validar el Usuario Cliente, ya con el model que generamos propio para el cliente.


"""def login_cliente(request):
    if request.method == 'POST':
        formulario_login_cliente = ConfirmarUsuarioCliente(request.POST)
        if formulario_login_cliente.is_valid():
            email = formulario_login_cliente.cleaned_data['email']
            contraseña = formulario_login_cliente.cleaned_data['contraseña']
            email = authenticate(email, contraseña=contraseña)
            if email is not None:
                login(request, email)
                return redirect('Index')
        else:
            formulario_login_cliente = ConfirmarUsuarioCliente()
            return render(request, 'Login.html',{
                'formulario_login_cliente': formulario_login_cliente
            })"""


#/////////////////////////////////////////////////


#PROCEDEMOS A CREAR LAS VISTAS PARA LISTA DE DESEOS Y CARRITO

#VISTA PARA MOSTRAR EL CARRITO/LISTA DE DESEOS, SOLO SI TENEMOS EL USUARIO VALIDADO
@login_required
def carrito(request):
    #CON OBJECTS.FILLTER LO QUE HAREMOS SERA OBTENER TODOS LOS ARTICULOS DE NUESTRO CARRITO
    carrito_item = Carrito.objects.filter(usuario=request.user)
    #VAMOS A CALCULAR EL VALOR TOTAL, PARA ELLO LO ASIGNAMOS A UNA VARIABLE item.total_producto EL CUAL LO LLEVAMOS A NUESTRA PLANTILLA
    for item in carrito_item:
        item.total_producto = float(item.producto.precio) * item.cantidad
    total = sum(float(item.total_producto) for item in carrito_item)
    #RENDERIZAMOS NUESTRA PLANTILLA DE CARRITO, CON LOS DATOS CORRESPONDIENTES
    return render (request, 'Agregar_Carrito.html', {
        'carrito_item': carrito_item,
        'total': total
    })

#FUNCIONES DE VISTAS, LAS CUALES ACCEDEMOS DESDE NUESTRO NAV CON LOS ICONOS DEL CARRITO/DESEO

def ver_la_lista_deseos(request):
    lista_item = ListaDeseos.objects.filter(id_usuario_id=request.user)

    for item in lista_item:
        item.name=(item.producto.name)
        item.descripcion=(item.producto.descripcion)
    
    return render(request, 'Lista_de_deseos.html', {
        'lista_item':lista_item
    })


#FUNCION PARA AGREGAR LOS PRODUCTOS AL CARRITO. 

@login_required
def carrito(request):
    #CON OBJECTS.FILLTER LO QUE HAREMOS SERA OBTENER TODOS LOS ARTICULOS DE NUESTRO CARRITO
    carrito_item = Carrito.objects.filter(id_usuario_id=request.user)
    #VAMOS A CALCULAR EL VALOR TOTAL, PARA ELLO LO ASIGNAMOS A UNA VARIABLE item.total_producto EL CUAL LO LLEVAMOS A NUESTRA PLANTILLA
    for item in carrito_item:
        item.total_producto = float(item.producto.precio) * item.cantidad
    total = sum(float(item.total_producto) for item in carrito_item)
    #RENDERIZAMOS NUESTRA PLANTILLA DE CARRITO, CON LOS DATOS CORRESPONDIENTES
    return render (request, 'Agregar_Carrito.html', {
        'carrito_item': carrito_item,
        'total': total
    })

@login_required
def agregar_al_carrito(request, id):

    producto = get_object_or_404(Productos, id=id)

    #Ahora verificamos si el producto ya esta en el carrito del usuario de la siguiente manera:

    carrito_item, created = Carrito.objects.get_or_create(id_usuario_id=request.user.id, producto=producto)

    #NUESTRA SENTENCIA IF PARA CONFIRMAR SI EL PRODUCTO YA EXISTE, DEBERA DE INCREMENTAR + 1

    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()
    
    #PASAMOS AL ELSE SI NO ESTA EN EL CARITO, GENERAMOS CON LA CANTIDAD 1
    
    else:
        carrito_item.cantidad = 1
        carrito_item.save()

    #LUEGO DE ESTO PROCEDEMOS   1A REDIRECCIONAR A NUESTRA LISTA DE PRODUCTOS

    return redirect ('ver_carrito') 
    #TAMBIEN PODEMOS REDIRECCIONAR DIRECTO A NUESTRO CARRITO, PARA VER LOS PRODUCTOS, PERO EN ESTE CASO DEJAMOS QUE EL USUARIO DECIDA CUANDO IR AL CARRITO.

    #AHORA PROCEDEMOS DE LA MISMA MANERA QUE AGREGAMOS AL CARRITO, LO HAREMOS PARA AGREGAR A NUESTRA LISTA DE DESEOS, VAMOS A MOSTRAR UNA PANTALLA CON LOS PRODUCTOS SELECCIONADOS, NO HAREMOS ALGUN CALCULO, SOLO MOSTRAREMOS DICHOS PRODUCTOS



@login_required
def agregar_lista_de_deseos(request, id):
 
    producto = get_object_or_404(Productos, id=id)

    lista_item, created = ListaDeseos.objects.get_or_create(id_usuario_id=request.user.id, producto=producto)

    if not created:
        lista_item.cantidad += 1
        lista_item.save()
    
    else: 
        lista_item.cantidad = 1
        lista_item.save()
    
    return redirect('ver_lista_deseos')


#FUNCION para eliminar productos de la lista deseos
@login_required
def eliminar_del_carrito(request, id):
    
    producto = get_object_or_404(Productos, id=id)

    lista_item = ListaDeseos.objects.filter(id_usuario_id=request.user, producto = producto).first()

    if lista_item:
        lista_item.delete()

    return redirect('ver_lista_deseos')


#FUNCION PARA ELIMINAR PRODUCTOS DEL CARRITO

@login_required
def eliminar_del_carrito(request, id):

    carrito_item = get_object_or_404(Carrito, id=id, id_usuario_id=request.user)

    #Condicion para disminuir el producto y no eliminarlo

    if carrito_item.cantidad > 1:

        carrito_item.cantidad -=1
        carrito_item.save()
    
    else:
        carrito_item.delete()

    return redirect('ver_carrito')

@login_required
def eliminar_carrito(request, id):

    carrito_item=get_object_or_404(Carrito, id=id, id_usuario_id=request.user)

    if carrito_item:
        carrito_item.delete()
    
    return redirect('ver_carrito')