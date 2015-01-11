from django.conf.urls import patterns, include, url
from django.contrib import admin

# from savetimeapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'savetime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'savetimeapp.views.home', name='home'),
    # /items/<number>/<number> -> loadSavetimeItems
    url(r'^items/(?P<num_items>\d+)/(?P<num_items_so_far>\d+)',
        'savetimeapp.views.loadSavetimeItems',
        name='loadSavetimeItems'),
    # /item/<number>/like -> likeSavetimeItem
    url(r'^item/(?P<item_id>\d+)/like', 'savetimeapp.views.likeSavetimeItem',
        name='likeSavetimeItem'),
)
