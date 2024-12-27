#api seria similar a los views en django normal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioClienteSerializeer


#a diferencia de los views aca creamos primero la clase


"""class UserClienteAPI(APIView):
    def post(self, request):
        serializer = UsuarioClienteSerializeer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)"""

class UserClienteAPI(APIView):
    def post(self, request):
        serializer = UsuarioClienteSerializeer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




