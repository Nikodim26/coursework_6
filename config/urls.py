from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer_management.urls', namespace='customer_management')),
    path('', include('message_management.urls', namespace='message_management')),
    path('', include('mailing_management.urls', namespace='mailing_management')),
    path('', include('users.urls', namespace='users')),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )