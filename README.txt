
                                Proyecto Demo: Web E-Commerce 🛒

Este es un sistema de E-Comerce desarrollado con Django, diseñado para facilitar la gestion de usuarios, productos y compras en línea. Incluye funcionalidades para usuarios finales y administradores, además de una API básica para la creación de Usuarios Clientes.

##Caracteristicas Principales
Frontend: Funcionalidades para Usuarios Clientes.
Gestion de Usuarios: 
-Registro de usuarios clientes.
-Modificacion del perfil. 
-Carrito de Compras y Lista de Deseos:
-Agregar productos al carrito o la lista de deseos.
-Visualizacion de los productos seleccionados.
Compra Simulada:
-Proceso ficticio para simular una experiencia de compra.
Backend: Panel de Administración.
Panel Predefinido de Django:
Control de Usuarios:
-Alta, baja y modificacion.
-Gestion de permisos para usuarios clientes y administradores.
Gestion de Productos:
-Alta, baja y modificacion de productos.
-Manejo de modelos relacionados y sus detalles.
Panel Personalizado:
Personalización de la interfaz:
-Titulo personalizado.
-Visualizacion del username del usuario actual.
Funcionalidades añadidas:
-Registro de acciones realizadas por cada usuario.
-Buscadores en modelos clave para facilitar la búsqueda.
-Vistas personalizadas para presentar datos específicos.
-Filtros avanzados para categorizar y encontrar datos rápidamente.
-API
Implementacion de una API básica utilizando Django REST Framework:
Creacion de usuarios clientes mediantes solicitudes POST.
-Validaciones para evitar duplicados y asegurar datos consistentes.
##Tecnologias Utilizadas.
Backend
-Python: Lenguaje principal para el desarrollo del backend.
-Django: Framework web utilizado para la lógica del servidor y la gestión de datos.
-Django REST Framework: Extensión de Django para la creación de APIs RESTful.
##Frontend
-HTML: Estructuración de las páginas web.
-CSS: Estilización para un diseño atractivo y responsivo.
-JavaScript (JS): funcionalidades dinámicas en el navegador.
-Django Templates: Sistema de plantillas utilizado para integrar datos del backend con el frontend.
Requisitos de instalación.
Python 3.8 o superior.
Virtualenv para entornos virtuales.
## Instalar dependencias con
Para instalar las dependencias, usa:
pip install -r requirements.txt ---todas las dependencias se encuentran dentro del archivo
## Cómo Ejecutar el Proyecto
*Clona el repositorio:
git clone 
cd mi-proyecto-ecommerce
*Configura las migraciones de la base de datos:
python manage.py makemigrations
python manage.py migrate
*Crea un usuario administrador:
python manage.py createsuperuser
*Ejecuta el servidor de desarrollo:
python manage.py runserver
Accede a la aplicación en http://127.0.0.1:8000.

