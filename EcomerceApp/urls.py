
from django.urls import path, include
from EcomerceApp import views
from api.api import UserClienteAPI
from django.views.generic import TemplateView

urlpatterns =[
    path('',views.index, name="Index"),
    path('productos/', views.productos, name="Productos"),
    path('Detalle-Producto/<int:id>', views.detalle_producto, name="Productos_Detalle"),
    path("login/", views.login_ingreso, name="Login"),
    path('agregar-al-carrito/<int:id>/', views.agregar_al_carrito, name="Carrito_de_compras"),
    path('agregar-lista-de-deseos/<int:id>/', views.agregar_lista_de_deseos, name="Lista_de_deseo"),
    path('lista-deseos/', views.ver_la_lista_deseos, name='ver_lista_deseos'),
    path('Remover-de-lista/<int:id>/', views.eliminar_del_carrito, name="remover_de_lista_deseos"),
    path('carrito/', views.carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:id>/', views.agregar_al_carrito, name='Carrito_de_compras'),
    path('Remover-del-carito/<int:id>/', views.eliminar_del_carrito, name='Eliminar_del_carrito'),
    path('Eliminar_Carrito/<int:id>/', views.eliminar_carrito, name='Eliminar_carrito'),
    path('Crear-Usuario/', views.Crear_Usuario, name='Crear_Usuario'),
    path('api/crear-usuario/', UserClienteAPI.as_view(), name='crear_usuario_api'),
    path('crear-usuario-cliente/', views.crear_usuario_cliente, name='crear_usuario_cliente'),
    path('Perfil-usuario/', views.perfil_usuario, name='Perfil_Usuario'),



]


