from django.contrib import admin
from .models import Work, Production, ProductionMedia, People, Role

# Register your models here.
admin.site.register(Work)
admin.site.register(Production)
admin.site.register(ProductionMedia)
admin.site.register(People)
admin.site.register(Role)