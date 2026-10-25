from django.contrib import admin

from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'type', 'year']
    list_filter = ['make', 'type', 'year']
    search_fields = ['name', 'make__name']


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'city', 'state']
    list_filter = ['state']
    search_fields = ['full_name', 'city', 'state', 'address']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dealership', 'car_make', 'car_model', 'car_year', 'sentiment']
    list_filter = ['dealership', 'sentiment']
    search_fields = ['name', 'review', 'car_make', 'car_model']
