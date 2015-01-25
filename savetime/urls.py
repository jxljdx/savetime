from django.conf.urls import patterns, include, url
from django.contrib import admin

# from savetimeapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'savetime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'savetimeapp.views.home', name='home'),
    url(r'^about$', 'savetimeapp.views.about', name='about'),
    # /items/<number>/<number> -> loadSavetimeItems
    url(r'^items/(?P<num_items>\d+)/(?P<num_items_so_far>\d+)$',
        'savetimeapp.views.loadSavetimeItems',
        name='loadSavetimeItems'),

    # /items/(before|after)/<number>/<time> -> loadSavetimeItemsGivenTime
    # Load num of save time items before or after given time.
    # <time> format is as follows,
    # Year-month-day-hour-minute-second-serverTimezone
    url(r'^items/(?P<before_or_after>(before|after))/(?P<num_items>\d+)/(?P<time_str>\d+-\d+-\d+-\d+-\d+-\d+-.+)',
        'savetimeapp.views.loadSavetimeItemsGivenTime',
        name='loadSavetimeItemsGivenTime'),

    # /item/<number>/like -> likeSavetimeItem
    url(r'^item/(?P<item_id>\d+)/like', 'savetimeapp.views.likeSavetimeItem',
        name='likeSavetimeItem'),
)
