from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Brand)
admin.site.register(Product)

#Seach with suggession demo db
admin.site.register(Names)
