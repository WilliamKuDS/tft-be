from django.db import models

import tft


# Player Account
class account(models.Model):
    puuid = models.CharField(primary_key=True, max_length=100)
    game_name = models.CharField(max_length=16)
    tag_line = models.CharField(max_length=5)

    class Meta:
        indexes = [
            models.Index(fields=['game_name', 'tag_line']),  # Composite index
        ]

    def __str__(self):
        return f'{self.game_name}#{self.tag_line}'

    def safe_get_by_puuid(puuid):
        try:
            return account.objects.get(puuid=puuid)
        except account.DoesNotExist:
            return None

    def safe_get_by_name_tag(game_name, tag_line):
        try:
            return account.objects.get(game_name=game_name, tag_line=tag_line)
        except account.DoesNotExist:
            return None


class region(models.Model):
    region_id = models.CharField(primary_key=True, max_length=3)
    label = models.CharField(max_length=4)
    server = models.CharField(max_length=4)
    description = models.CharField(max_length=50)

    def safe_get_by_region_id(region_id):
        try:
            return region.objects.get(region_id=region_id)
        except region.DoesNotExist:
            return None


# Player Account(Summoner) based on region
class summoner(models.Model):
    id = models.AutoField(primary_key=True)
    summoner_id = models.CharField(max_length=100)
    region = models.ForeignKey(region, on_delete=models.CASCADE, related_name='summoners')
    puuid = models.ForeignKey(account, on_delete=models.CASCADE, related_name='summoners')
    account_id = models.CharField(max_length=100)
    icon = models.CharField(max_length=5)
    level = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('summoner_id', 'region'),)
        indexes = [
            models.Index(fields=['summoner_id', 'region']),
        ]

    def __str__(self):
        return f'{self.summoner_id} - {self.region}'

    def safe_get_by_summoner_id_region(summoner_id, region):
        try:
            return summoner.objects.get(summoner_id=summoner_id, region=region)
        except summoner.DoesNotExist:
            return None

    def safe_get_by_puuid_region(puuid, region):
        try:
            return summoner.objects.get(puuid=puuid, region=region)
        except summoner.DoesNotExist:
            return None


# Ranked league based on region
class league(models.Model):
    id = models.AutoField(primary_key=True)
    league_id = models.CharField(max_length=100)
    region = models.ForeignKey(region, on_delete=models.CASCADE, related_name='leagues')
    tier = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    queue = models.CharField(max_length=10)

    class Meta:
        unique_together = (('league_id', 'region'),)
        indexes = [
            models.Index(fields=['league_id', 'region']),
        ]

    def __str__(self):
        return f'{self.queue} - {self.name} - {self.region}'

    def safe_get_by_league_id(league_id):
        try:
            return league.objects.get(league_id=league_id)
        except league.DoesNotExist:
            return None


# Ranked profile for summoner
class summoner_league(models.Model):
    id = models.AutoField(primary_key=True)
    summoner = models.ForeignKey(summoner, on_delete=models.CASCADE, related_name='summoner_leagues')
    region = models.ForeignKey(region, on_delete=models.CASCADE, related_name='summoner_leagues')
    queue = models.CharField(max_length=50)
    puuid = models.ForeignKey(account, on_delete=models.CASCADE, related_name='summoner_leagues')
    league = models.ForeignKey(league, on_delete=models.CASCADE, related_name='summoner_leagues')
    tier = models.CharField(max_length=10)
    rank = models.CharField(max_length=3)
    league_points = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    veteran = models.BooleanField()
    inactive = models.BooleanField()
    fresh_blood = models.BooleanField()
    hot_streak = models.BooleanField()

    class Meta:
        unique_together = (('summoner', 'region', 'queue', 'league'),)
        indexes = [
            models.Index(fields=['summoner', 'region', 'queue', 'league']),
        ]

    def __str__(self):
        return f'{self.queue} - {self.summoner}'

    def safe_get_by_summoner_id_and_region(summoner_id, region):
        try:
            return summoner_league.objects.get(summoner_id=summoner_id, region=region)
        except summoner_league.DoesNotExist:
            return None


class set(models.Model):
    set_id = models.FloatField(primary_key=True)
    set_name = models.CharField(max_length=50)

    def safe_get(set_id):
        try:
            return set.objects.get(set_id=set_id)
        except set.DoesNotExist:
            return None

    def safe_get_name(set_name):
        try:
            return set.objects.get(set_name=set_name)
        except set.DoesNotExist:
            return None


class patch(models.Model):
    patch_id = models.CharField(primary_key=True, max_length=10)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    highlights = models.CharField(max_length=200)
    patch_url = models.CharField(max_length=200)

    def safe_get_patch_id(patch_id):
        try:
            return patch.objects.get(patch_id=patch_id)
        except patch.DoesNotExist:
            return None

    def safe_get_set_id(set_id):
        try:
            return patch.objects.get(set_id=set_id)
        except patch.DoesNotExist:
            return None

    def safe_get_set_revival_id(revival_set_id):
        try:
            return patch.objects.get(set_name=revival_set_id)
        except patch.DoesNotExist:
            return None


class trait(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=30)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=500)
    description = models.TextField()

    class Meta:
        unique_together = (('api_name', 'patch_id'),)
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'

    def safe_get_id(id):
        try:
            return trait.objects.get(id=id)
        except trait.DoesNotExist:
            return None

    def safe_get_api_name_patch(api_name, patch_id):
        try:
            return trait.objects.get(api_name=api_name, patch_id=patch_id)
        except trait.DoesNotExist:
            return None

    def safe_get_name_patch(display_name, patch_id):
        try:
            return trait.objects.get(display_name=display_name, patch_id=patch_id)
        except trait.DoesNotExist:
            return None


class trait_effect(models.Model):
    id = models.AutoField(primary_key=True)
    trait_id = models.ForeignKey(trait, on_delete=models.CASCADE)
    style = models.IntegerField(null=True, blank=True)
    min_units = models.IntegerField()
    max_units = models.IntegerField()
    variables = models.JSONField()

    class Meta:
        unique_together = (('trait_id', 'min_units', 'max_units'),)
        indexes = [
            models.Index(fields=['trait_id', 'min_units', 'max_units']),
            models.Index(fields=['trait_id']),
        ]

    def safe_get_trait_id_min_max(trait_id, min_units, max_units):
        try:
            return trait_effect.objects.get(trait_id=trait_id, min_units=min_units, max_units=max_units)
        except trait_effect.DoesNotExist:
            return None


class champion(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=100)
    cost = models.IntegerField()
    icon = models.CharField(max_length=500, null=True)
    square_icon = models.CharField(max_length=500, null=True)
    tile_icon = models.CharField(max_length=500, null=True)
    trait = models.ManyToManyField(trait)

    class Meta:
        unique_together = (('api_name', 'patch_id'),)
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def safe_get_id(id):
        try:
            return champion.objects.get(id=id)
        except champion.DoesNotExist:
            return None

    def safe_get_api_name_patch(api_name, patch_id):
        try:
            return champion.objects.get(api_name=api_name, patch_id=patch_id)
        except champion.DoesNotExist:
            return None

    def safe_get_name_patch(display_name, patch_id):
        try:
            return champion.objects.get(display_name=display_name, patch_id=patch_id)
        except champion.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'


class champion_ability(models.Model):
    id = models.AutoField(primary_key=True)
    champion_id = models.ForeignKey(champion, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    icon = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True)
    variables = models.JSONField()


class champion_stats(models.Model):
    id = models.AutoField(primary_key=True)
    champion_id = models.ForeignKey(champion, on_delete=models.CASCADE)
    armor = models.IntegerField(null=True)
    attack_speed = models.FloatField(null=True)
    crit_chance = models.FloatField(null=True)
    crit_multiplier = models.FloatField(null=True)
    damage = models.IntegerField(null=True)
    hp = models.IntegerField(null=True)
    initial_mana = models.IntegerField(null=True)
    mana = models.IntegerField(null=True)
    magic_resist = models.IntegerField(null=True)
    range = models.IntegerField(null=True)


class item(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    icon = models.TextField()
    unique = models.BooleanField(null=True)
    effects = models.JSONField(null=True)
    associated_traits = models.JSONField(null=True)
    incompatible_traits = models.JSONField(null=True)
    composition = models.JSONField(null=True)

    class Meta:
        unique_together = (('api_name', 'patch_id'),)
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'


class augment(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    icon = models.TextField()
    unique = models.BooleanField(null=True)
    effects = models.JSONField(null=True)
    associated_traits = models.JSONField(null=True)
    incompatible_traits = models.JSONField(null=True)
    composition = models.JSONField(null=True)

    class Meta:
        unique_together = (('api_name', 'patch_id'),)
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'


class miscellaneous(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    icon = models.TextField()
    unique = models.BooleanField(null=True)
    effects = models.JSONField(null=True)
    associated_traits = models.JSONField(null=True)
    incompatible_traits = models.JSONField(null=True)
    composition = models.JSONField(null=True)

    class Meta:
        unique_together = (('api_name', 'patch_id'),)
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'

class match(models.Model):
    match_id = models.CharField(primary_key=True, max_length=15)
    game_id = models.BigIntegerField()
    region = models.CharField(max_length=4)
    game_result = models.CharField(max_length=25)
    data_version = models.CharField(max_length=5)
    game_creation = models.BigIntegerField()
    game_datetime = models.BigIntegerField()
    game_length = models.FloatField()
    game_version = models.CharField(max_length=100)
    map_id = models.IntegerField()
    queue_id = models.IntegerField()
    game_type = models.CharField(max_length=50)
    set_core_name = models.CharField(max_length=50)
    set = models.IntegerField()

    def safe_get_by_match_id(match_id):
        try:
            return match.objects.get(match_id=match_id)
        except match.DoesNotExist:
            return None


class match_summoner(models.Model):
    id = models.AutoField(primary_key=True)
    match_id = models.ForeignKey(match, on_delete=models.CASCADE)
    puuid = models.ForeignKey(account, on_delete=models.CASCADE)
    placement = models.IntegerField()
    gold_left = models.IntegerField()
    last_round = models.IntegerField()
    level = models.IntegerField()
    players_eliminated = models.IntegerField()
    time_eliminated = models.FloatField()
    total_damage_to_players = models.IntegerField()
    companion = models.JSONField()
    missions = models.JSONField()
    augments = models.JSONField()
    traits = models.JSONField()
    units = models.JSONField()

    class Meta:
        unique_together = (('match_id', 'puuid'),)
        indexes = [
            models.Index(fields=['match_id', 'puuid']),
            models.Index(fields=['puuid']),
        ]