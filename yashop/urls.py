from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve as static


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
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
]
