from django.conf.urls import patterns, include, url
from django.contrib import admin

# from savetimeapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'savetime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # ++++ IMPORTANT ++++
    # Restful APIs return format
    # {"msg": "success | <Failure detail>",
    #  "data": "<Any data we want to return back>"}
    # No need to include data part if it's a failure

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

    # /search/items/<keyword>/(before|after)/(1|0)/<number>/<time> -> searchSavetimeItemsGivenTime
    # Search and return num of save time items, which contain keyword in title or
    # description, keywords or category field, before or after given time.
    # If categories_only is set to 1, given keyword is the category name, we only need to return
    # save time items in that category.
    # <time> format is as follows,
    # Year-month-day-hour-minute-second-serverTimezone
    url(r'^search/items/(?P<keyword>.+?)/(?P<before_or_after>(before|after))/(?P<categories_only>(1|0))/(?P<num_items>\d+)/(?P<time_str>\d+-\d+-\d+-\d+-\d+-\d+-.+)',
        'savetimeapp.views.searchSavetimeItemsGivenTime',
        name='searchSavetimeItemsGivenTime'),

    # /item/<number>/like -> likeSavetimeItem
    url(r'^item/(?P<item_id>\d+)/like', 'savetimeapp.views.likeSavetimeItem',
        name='likeSavetimeItem'),

    url(r'^categories$', 'savetimeapp.views.categories', name='categories'),
    url(r'^get/categories/(?P<which_main_category>(critical|major|minor|all))$', 'savetimeapp.views.getCategories', name='getCategories'),
)
