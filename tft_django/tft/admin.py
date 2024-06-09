from django.contrib import admin
from .models import account, region, summoner, league, summoner_league
from .models import set, patch
from .models import trait, trait_effect
from .models import champion, champion_stats, champion_ability
from .models import item, augment, miscellaneous
from .models import match, match_summoner


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


class MatchInLine(admin.TabularInline):
    model = match_summoner
    extra = 1


class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchInLine]


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
admin.site.register(champion)
admin.site.register(champion_stats)
admin.site.register(champion_ability)
admin.site.register(item)
admin.site.register(augment)
admin.site.register(miscellaneous)
admin.site.register(match, MatchAdmin)
admin.site.register(match_summoner)
# admin.site.register(game_unit)
# admin.site.register(game_info)
# admin.site.register(game)
# admin.site.register(game_trait)
