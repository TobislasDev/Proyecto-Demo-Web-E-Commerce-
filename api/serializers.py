from rest_framework import serializers
from django.contrib.auth.models import User



#LO QUE REALIZAMOS FUE LO SIGUIENTE, DESCARGAR EL DJANGO REST-FRAMEWORK-REST, con esto podremos expandir este proyeto, de tal manera a poder aprovechar las funcionalidades de django rest framework
#Creamos una app nueva llamada api, la adherimos en sethings install app y creamos un archivo llamado serializers.py el cual es algo similar a un model, pero con distintas opciones

#creamos nuestro primer serializers para lo que corresponde a crear un usuario cliente

class UsuarioClienteSerializeer(serializers.Serializer):

    #ahora definimos los datos 
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    #funcion para crear el usuario 

    """def create_usuario(self, validate_date):
        instance = User()
        instance.first_name = validate_date.get('nombre')
        instance.last_name = validate_date.get('apellido')
        instance.username = validate_date.get('usuario')
        instance.email = validate_date.get('email')
        instance.set_password(validate_date.get('password'))
        instance.save()
        return instance
    
    def valida_usuario(self, data):
        users = User.objects.filter(username = data)
        if len(users) != 0:
            raise serializers.ValidationError("El nombre de usuario ya existe, favor verifique nuevamente!")
        else:
            return data"""
    
    def validar_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe, favor verifique nuevamente!")
        return value
    
    def create(self, validated_data):
        user = User(
             first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    

    
