from django.http import HttpResponse
from django.shortcuts import render
from django.utils import dateformat
from savetimeapp.models import Item
import datetime
import json

# Year-month-day-hour-minute-second-serverTimezone
TIME_FORMAT = 'Y-m-d-H-i-s-T'
SUCCESS = {"msg": "success"}

# Create your views here.
def home(request):
    # return HttpResponse("Hello, this is the homepage")
    return render(request, "index.html")

def loadSavetimeItems(request, num_items, num_items_so_far):
    ''' Returns back list of save time items in local time decreasing order. '''
    items = Item.objects.order_by("created_at").reverse()[num_items_so_far:(num_items_so_far + num_items)]
    responses = []
    for item in items:
        response = {}
        response["title"] = item.title
        response["desc"] = item.desc
        response["url"] = item.url
        response["created_at"] = dateformat.format(item.created_at, TIME_FORMAT)
        response["num_likes"] = item.num_likes
        response["id"] = item.id
        responses.append(response)
    return HttpResponse(json.dumps(responses), content_type="application/json")

def likeSavetimeItem(request, item_id):
    item = Item.objects.get(id=item_id)
    item.num_likes += 1
    item.save()
    return HttpResponse(json.dumps(SUCCESS), content_type="application/json")