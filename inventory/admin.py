from django.contrib import admin
from stockpile.inventory.models import Category, Field, Item, Value, FieldType


admin.site.register(Category)
admin.site.register(Field)
admin.site.register(FieldType)
admin.site.register(Item)
admin.site.register(Value)
#admin.site.register(Catalogue)
