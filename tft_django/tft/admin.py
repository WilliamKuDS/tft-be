from django.contrib import admin
from .models import player, patch, augment, trait, item, unit, game_unit, game_info, game, set, game_trait, synergy

# Register your models here.
admin.site.register(player)
admin.site.register(patch)
admin.site.register(augment)
admin.site.register(trait)
admin.site.register(item)
admin.site.register(unit)
admin.site.register(game_unit)
admin.site.register(game_info)
admin.site.register(game)
admin.site.register(set)
admin.site.register(game_trait)
admin.site.register(synergy)
