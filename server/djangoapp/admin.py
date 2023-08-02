from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'dealer_id')
    list_filter = ('type', 'year')
    search_fields = ('name', 'type', 'dealer_id')

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)