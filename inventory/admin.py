from django.contrib import admin
import stockpile.inventory.models as models


admin.site.register(models.Category)
admin.site.register(models.Field)
admin.site.register(models.Item)
admin.site.register(models.Value)
#admin.site.register(models.Catalogue)
