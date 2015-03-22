from django.contrib import admin
from actors.models import Actor, Movies

admin.site.register(Movies)

class MovieInline(admin.TabularInline):
    model = Movies
    extra = 10

class ActorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['actor']})
    ]
    inlines = [MovieInline]

admin.site.register(Actor, ActorAdmin)

# Register your models here.
