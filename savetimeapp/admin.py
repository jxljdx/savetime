from django.contrib import admin
from django import forms
from savetimeapp.models import Category
from savetimeapp.models import Item

# Register your models here.

class ItemDescForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea)
    # title = forms.CharField(widget=forms.Textarea)

class ItemAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'url', 'desc', 'num_likes', 'created_at')
    #     }),
    # )
    form = ItemDescForm
    list_display = ('title', 'num_likes', 'created_at', 'url', 'keywords', 'category_names')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('main_category', "sub_category", 'num_clicks')

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)