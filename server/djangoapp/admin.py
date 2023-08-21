from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    search_fields = ['name']


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'year')
    search_fields = ['name', 'car_type']


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
