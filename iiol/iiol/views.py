from django.shortcuts import redirect
from rest_framework.response import Response  
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

def site_prefix_redirect(request, path):
    new_path = path.lstrip('/')
    return redirect(new_path)


@api_view(('GET',))
@permission_classes([AllowAny])
def health_check(request):
    return Response(status=status.HTTP_200_OK)