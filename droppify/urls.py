from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include('orders.urls')),
    path('', include('home.urls')),
    path('staff/', include('staff.urls')),
    path('custom/', include('custom_services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('prebuilt/', include('prebuilt.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),   # home + dashboard pages
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns  += staticfiles_urlpatterns()