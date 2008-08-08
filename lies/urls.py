from django.conf.urls.defaults import *
from lieswetellourselves.lies.models import Lie
from lieswetellourselves.lies.forms import LieForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

info_dict = {
    'queryset': Lie.objects.all(),
}

urlpatterns = patterns('',
#    (r'^$', 'index'),
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^add/$', 'django.views.generic.create_update.create_object', {'form_class': LieForm}),
    (r'^add_vote/$', 'lieswetellourselves.lies.views.add_vote'),
#    (r'^add/$', 'lieswetellourselves.lies.views.add'),
#    (r'^(?P<lie_id>\d+)/$', 'detail'),
    url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict, name='lie_detail'),
)
