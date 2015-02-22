from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import dateformat
from pytz import timezone
from savetimeapp.models import Item
import json

# Year-month-day-hour-minute-second-serverTimezone
TIME_FORMAT = '%Y-%m-%d-%H-%M-%S-%Z'
MESSAGE_KEY = "msg"
DATA_KEY = "data"
SUCCESS_MSG = "success"
SUCCESS = {"msg": SUCCESS_MSG}

# Create your views here.
def home(request):
    # return HttpResponse("Hello, this is the homepage")
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

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

def searchSavetimeItemsGivenTime(request, keyword, before_or_after, num_items, time_str):
    '''
    Searches and returns back list of save time items, which contain the
    matching text in the title, description or keyword field, before or after
    given time in local time decreasing order.
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
    items = None
    if before_or_after == "before":
        items = Item.objects.filter(created_at__lt=time) \
                            .filter(Q(title__icontains=keyword) | \
                                    Q(desc__icontains=keyword) | \
                                    Q(keywords__icontains=keyword)) \
                            .order_by("num_likes") \
                            .reverse()[0:num_items]
    else:
        items = Item.objects.filter(created_at__gt=time) \
                            .filter(Q(title__icontains=keyword) | \
                                    Q(desc__icontains=keyword) | \
                                    Q(keywords__icontains=keyword)) \
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