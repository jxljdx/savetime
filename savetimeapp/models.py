from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    """A save time item which contains basic info like title, link to the site
       detailing about the item, etc.
    """
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now())
    num_likes = models.IntegerField(default=0)
    url = models.CharField(max_length=300)
    desc = models.CharField(max_length=2048)