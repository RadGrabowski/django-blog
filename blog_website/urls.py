from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.generic.base import RedirectView

sitemaps = {'posts': PostSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
                  path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                  path('', RedirectView.as_view(pattern_name='blog:post_list', permanent=False))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
