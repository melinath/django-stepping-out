from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import djam


djam.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + patterns('',
    url(r'^admin/', include(djam.admin.urls)),
    url(r'^daguerre/', include('daguerre.urls')),
    url(r'^', include('stepping_out.urls')),
)
