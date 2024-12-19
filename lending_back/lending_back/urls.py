from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    # path('api/submit-application/', SubmitApplicationView.as_view(), name='submit_application'),
    path('api/auth/', include("custom_auth.urls", namespace='auth',)),
    path('api/user/', include("custom_auth.user_urls", namespace='user', )),
    path('api/email/', include("email_sender.urls", namespace='email')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
