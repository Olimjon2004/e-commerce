from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# from drf_yasg.generators import OpenAPIAchemaGenerator
# from rest_framework import permissions
# from rest_framework_simplejwt import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )
# from billing.vews import CreateChargeView


schem_view = get_schema_view(
    openapi.Info(
        title='API E-Commerce',
        default_version='v1',
        description='E-commerce API',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='xikmatullayevolimjon@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('products.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schem_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schem_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schem_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),

]
