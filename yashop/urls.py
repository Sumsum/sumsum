from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve as static
from rest_framework import routers
from products.api import ProductViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', ProductViewSet)


urlpatterns = []


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static, {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^select2/', include('django_select2.urls')),
]
