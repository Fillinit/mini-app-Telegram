import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    
    # Эндпоинты админ-панели
    path('admin/', admin.site.urls),
    
    path('api/v1.0/schema/', SpectacularAPIView.as_view(), name='schema'), # JSON схема
    path('api/v1.0/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI
    path('api/v1.0/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # Redoc UI
        
    # Эндпоинты приложений
    path('api/v1.0/mainapp/', include('mainapp.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
