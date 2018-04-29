from django.contrib import admin

from animals.models import Animal, AnimalWeight


class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ('id', )
    ordering = ('id',)


admin.site.register(Animal, AnimalAdmin)


class AnimalWeightAdmin(admin.ModelAdmin):
    list_display = ('animal', 'weight', 'weight_date')
    search_fields = ('animal__name', )
    ordering = ('animal', 'weight_date')


admin.site.register(AnimalWeight, AnimalWeightAdmin)
