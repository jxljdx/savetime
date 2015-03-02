# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import dateformat
from pytz import timezone
from savetimeapp.models import Category
from savetimeapp.models import Item
import json

# Year-month-day-hour-minute-second-serverTimezone
TIME_FORMAT = '%Y-%m-%d-%H-%M-%S-%Z'
MESSAGE_KEY = "msg"
DATA_KEY = "data"
SUCCESS_MSG = "success"
SUCCESS = {"msg": SUCCESS_MSG}
CRITICAL_CATEGORY = "critical"
MAJOR_CATEGORY = "major"
MINOR_CATEGORY = "minor"

# Create your views here.
def home(request):
    # return HttpResponse("Hello, this is the homepage")
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def categories(request):
    critical_category_list = Category.objects.filter(main_category=CRITICAL_CATEGORY).order_by("num_clicks")
    major_category_list = Category.objects.filter(main_category=MAJOR_CATEGORY).order_by("num_clicks")
    minor_category_list = Category.objects.filter(main_category=MINOR_CATEGORY).order_by("num_clicks")
    category_dict = {
        "critical_category_list": critical_category_list,
        "major_category_list": major_category_list,
        "minor_category_list": minor_category_list
    }
    return render(request, "categories.html", category_dict)

def getCategories(request):
    critical_category_list = Category.objects.filter(main_category=CRITICAL_CATEGORY).order_by("num_clicks")
    major_category_list = Category.objects.filter(main_category=MAJOR_CATEGORY).order_by("num_clicks")
    minor_category_list = Category.objects.filter(main_category=MINOR_CATEGORY).order_by("num_clicks")
    response_data = {}

    # Get critical category list
    response_critical = []
    for c in critical_category_list:
        response_item = {}
        response_item["sub_category"] = c.sub_category
        response_item["num_clicks"] = c.num_clicks
        response_item["id"] = c.id
        response_critical.append(response_item)

    # Get major category list
    response_major = []
    for c in major_category_list:
        response_item = {}
        response_item["sub_category"] = c.sub_category
        response_item["num_clicks"] = c.num_clicks
        response_item["id"] = c.id
        response_major.append(response_item)

    # Get minor category list
    response_minor = []
    for c in minor_category_list:
        response_item = {}
        response_item["sub_category"] = c.sub_category
        response_item["num_clicks"] = c.num_clicks
        response_item["id"] = c.id
        response_minor.append(response_item)

    response_data = {CRITICAL_CATEGORY: response_critical,
                     MAJOR_CATEGORY: response_major,
                     MINOR_CATEGORY: response_minor}
    response = {MESSAGE_KEY: SUCCESS_MSG,
                DATA_KEY: response_data}
    return HttpResponse(json.dumps(response), content_type="application/json")

def loadSavetimeItems(request, num_items, num_items_so_far):
    ''' Returns back list of save time items in local time decreasing order. '''
    items = Item.objects.order_by("created_at").reverse()[num_items_so_far:(num_items_so_far + num_items)]
    responses = []
    for item in items:
        response = {}
        response["title"] = item.title
        response["desc"] = item.desc
        response["url"] = item.url
        response["created_at"] = item.created_at.strftime(TIME_FORMAT)
        response["num_likes"] = item.num_likes
        response["id"] = item.id
        responses.append(response)
    return HttpResponse(json.dumps(responses), content_type="application/json")

def loadSavetimeItemsGivenTime(request, before_or_after, num_items, time_str):
    '''
    Returns back list of save time items before or after given time in local
    time decreasing order.
    '''

    # Get time object from string
    time = None
    try:
        # strptime does not set the timezone info, so we have to explictly
        # set this info.
        time = datetime.strptime(time_str, TIME_FORMAT)
        item_timezone = timezone(time_str.split("-")[-1])
        time = time.replace(tzinfo=item_timezone)
    except ValueError:
        resp = {"msg": "Given time is not correct"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    items = None
    if before_or_after == "before":
        items = Item.objects.filter(created_at__lt=time) \
                            .order_by("created_at") \
                            .reverse()[0:num_items]
    else:
        items = Item.objects.filter(created_at__gt=time) \
                            .order_by("created_at") \
                            .reverse()[0:num_items]

    responses = []
    for item in items:
        response = {}
        response["title"] = item.title
        response["desc"] = item.desc
        response["url"] = item.url
        response["created_at"] = item.created_at.strftime(TIME_FORMAT)
        response["num_likes"] = item.num_likes
        response["id"] = item.id
        responses.append(response)
    return HttpResponse(json.dumps(responses), content_type="application/json")

def searchSavetimeItemsGivenTime(request, keyword, before_or_after, categories_only, num_items, time_str):
    '''
    Searches and returns back list of save time items, which contain the
    matching text in the title, description keywords or category field, before
    or after given time in local time decreasing order.
    '''

    # Get time object from string
    time = None
    try:
        # strptime does not set the timezone info, so we have to explictly
        # set this info.
        time = datetime.strptime(time_str, TIME_FORMAT)
        item_timezone = timezone(time_str.split("-")[-1])
        time = time.replace(tzinfo=item_timezone)
    except ValueError:
        resp = {"msg": "Given time is not correct"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    # Search for items
    base_conditions = Q(title__icontains=keyword) | \
                      Q(desc__icontains=keyword) | \
                      Q(keywords__icontains=keyword)
    category_condition = Q(categories__sub_category__icontains=keyword)
    query_conditon = None
    if int(categories_only) == 1:
        query_conditon = category_condition
    else:
        query_conditon = base_conditions | category_condition

    items = None
    if before_or_after == "before":
        items = Item.objects.filter(created_at__lt=time) \
                            .filter(query_conditon) \
                            .order_by("num_likes") \
                            .reverse()[0:num_items]
    else:
        items = Item.objects.filter(created_at__gt=time) \
                            .filter(query_conditon) \
                            .order_by("num_likes") \
                            .reverse()[0:num_items]

    responses = []
    for item in items:
        response = {}
        response["title"] = item.title
        response["desc"] = item.desc
        response["url"] = item.url
        response["created_at"] = item.created_at.strftime(TIME_FORMAT)
        response["num_likes"] = item.num_likes
        response["id"] = item.id
        responses.append(response)
    resp = {MESSAGE_KEY: SUCCESS_MSG, DATA_KEY: responses}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def likeSavetimeItem(request, item_id):
    item = None

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        response = {"msg": "Item can not be found"}
        return HttpResponse(json.dumps(response), content_type="application/json")

    item.num_likes += 1
    item.save()
    return HttpResponse(json.dumps(SUCCESS), content_type="application/json")