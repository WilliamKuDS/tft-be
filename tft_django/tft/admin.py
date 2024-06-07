from django.contrib import admin
from .models import account, region, summoner, league, summoner_league
from .models import set, patch, trait, trait_effect


class AccountInLine(admin.TabularInline):
    model = summoner
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountInLine]


class SummonerInLine(admin.TabularInline):
    model = summoner_league
    extra = 1


class SummonerAdmin(admin.ModelAdmin):
    inlines = [SummonerInLine]


class LeagueInLine(admin.TabularInline):
    model = summoner_league
    extra = 1


class LeagueAdmin(admin.ModelAdmin):
    inlines = [LeagueInLine]


# Register your models here.
admin.site.register(account, AccountAdmin)
admin.site.register(region)
admin.site.register(summoner, SummonerAdmin)
admin.site.register(league, LeagueAdmin)
admin.site.register(summoner_league)
admin.site.register(set)
admin.site.register(patch)
admin.site.register(trait)
admin.site.register(trait_effect)
# admin.site.register(augment)
# admin.site.register(item)
# admin.site.register(unit)
# admin.site.register(game_unit)
# admin.site.register(game_info)
# admin.site.register(game)
# admin.site.register(game_trait)
