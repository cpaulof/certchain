from rest_framework.routers import SimpleRouter
from core.viewsets import UserViewSet, BlockViewSet, DocumentViewSet
from auth.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserViewSet, basename='user')

#BLOCK
routes.register(r'block', BlockViewSet, basename='block')
routes.register(r'doc', DocumentViewSet, basename='document')

urlpatterns = [
    *routes.urls
]
