from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='accounts_root'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('follower/', views.profile_edit, name='profile_edit'),
    path('password_change/', views.password_change,
         name='password_change')
]

urlpatterns += [
    path(r'api-token-auth/', obtain_auth_token),
]
