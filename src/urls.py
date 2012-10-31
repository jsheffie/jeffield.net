from django.conf.urls.defaults import patterns, include, url
from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {'tags': TagSitemap,
            'blog': EntrySitemap,
            'authors': AuthorSitemap,
            'categories': CategorySitemap,}



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jeffield.views.home', name='home'),
    #url(r'^testapp/', include('testapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    
    url(r'^', include('zinnia.urls.capabilities')),
    url(r'^search/', include('zinnia.urls.search')),
    url(r'^sitemap/', include('zinnia.urls.sitemap')),
    url(r'^trackback/', include('zinnia.urls.trackback')),  
    url(r'^weblog/tags/', include('zinnia.urls.tags')),
    url(r'^weblog/feeds/', include('zinnia.urls.feeds')),
    url(r'^weblog/authors/', include('zinnia.urls.authors')),
    url(r'^weblog/categories/', include('zinnia.urls.categories')),
    url(r'^weblog/discussions/', include('zinnia.urls.discussions')),
    url(r'^weblog/', include('zinnia.urls.entries')),
    url(r'^weblog/', include('zinnia.urls.archives')),
    url(r'^weblog/', include('zinnia.urls.shortlink')),
    url(r'^weblog/', include('zinnia.urls.quick_entry')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)
urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'index',
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap',
        {'sitemaps': sitemaps}),)

#from django.conf import settings
from django.conf import settings
import os
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^tparty/(.*)$',     'django.views.static.serve', {'document_root': os.path.join(settings.ROOT_PATH, "tparty/static/")}),
                            )
