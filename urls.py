from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^lieswetellourselves/', include('lieswetellourselves.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^lies/', include('lieswetellourselves.lies.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/firstclown/Projects/lieswetellourselves/media'}),

)