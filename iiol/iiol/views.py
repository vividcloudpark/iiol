from django.shortcuts import redirect
from rest_framework.response import Response  
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

def site_prefix_redirect(request, path):
    """
    URL 경로에서 중복된 '/'나 잘못된 prefix가 들어왔을 때,
    올바른 경로로 리다이렉트해주는 함수입니다.
    예: '/some/path' -> 'some/path'
    """
    new_path = path.lstrip('/')
    return redirect(new_path)


@api_view(('GET',))
@permission_classes([AllowAny])
def health_check(request):
    """
    서버의 정상 동작 여부를 확인하는 Health Check API입니다.
    컨테이너 오케스트레이션 도구(예: 로드밸런서, Docker/Kubernetes)가
    해당 서버 인스턴스가 요청을 처리할 수 있는지 확인할 때 사용됩니다.
    """
    return Response(status=status.HTTP_200_OK)