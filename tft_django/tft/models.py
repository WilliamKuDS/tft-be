from django.db import models

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

    def safe_get_name_patch(name, patch_id):
        try:
            return trait.objects.get(name=name, patch_id=patch_id)
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

class unit(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['api_name', 'patch_id'], name='unit_unique_name_patch')
        ]
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),  # Composite index
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'


class item(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['api_name', 'patch_id'], name='item_unique_name_patch')
        ]
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),  # Composite index
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'


class augment(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=255)
    patch_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['api_name', 'patch_id'], name='augment_unique_name_patch')
        ]
        indexes = [
            models.Index(fields=['api_name', 'patch_id']),  # Composite index
            models.Index(fields=['api_name']),
            models.Index(fields=['patch_id']),
        ]

    def __str__(self):
        return f'{self.api_name} - {self.patch_id}'

# class augment(models.Model):
#     augment_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     display_name = models.CharField(max_length=100)
#     tier = models.IntegerField()
#     description = models.CharField(max_length=2000)
#     icon = models.CharField(max_length=500, null=True, blank=True)
#     set_id = models.ForeignKey(set, on_delete=models.CASCADE)
#
#     def safe_get_id(augment_id):
#         try:
#             return augment.objects.get(augment_id=augment_id)
#         except augment.DoesNotExist:
#             return None
#
#     def safe_get_name(name, set_id):
#         try:
#             return augment.objects.get(name=name, set_id=set_id)
#         except augment.DoesNotExist:
#             return None

# class item(models.Model):
#     item_id = models.CharField(primary_key=True, max_length=50, unique=True)
#     name = models.CharField(max_length=100)
#     display_name = models.CharField(max_length=100)
#     recipe = models.ManyToManyField('self', blank=True)
#     description = models.CharField(max_length=1000, null=True, blank=True)
#     icon = models.CharField(max_length=500)
#     stats = models.CharField(max_length=500)
#     tags = models.CharField(max_length=100)
#     url = models.CharField(max_length=500)
#     set_id = models.ForeignKey(set, on_delete=models.CASCADE)
#
#     def safe_get_id(item_id):
#         try:
#             return item.objects.get(item_id=item_id)
#         except item.DoesNotExist:
#             return None
#
#     def safe_get_name(name, set_id):
#         try:
#             return item.objects.get(name=name, set_id=set_id)
#         except item.DoesNotExist:
#             return None
#
# class unit(models.Model):
#     unit_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     display_name = models.CharField(max_length=100)
#     tier = models.IntegerField()
#     trait = models.ManyToManyField(trait)
#     ability_name = models.CharField(max_length=200)
#     ability_description = models.CharField(max_length=1000)
#     ability_info = models.CharField(max_length=1000)
#     ability_icon = models.CharField(max_length=500)
#     stats = models.CharField(max_length=1000)
#     icon = models.CharField(max_length=200, null=True, blank=True)
#     set_id = models.ForeignKey(set, on_delete=models.CASCADE)
#
#     def safe_get_id(unit_id):
#         try:
#             return unit.objects.get(unit_id=unit_id)
#         except unit.DoesNotExist:
#             return None
#
#     def safe_get_name(name, set_id):
#         try:
#             return unit.objects.get(name=name, set_id=set_id)
#         except unit.DoesNotExist:
#             return None

# class game_info(models.Model):
#     game_id = models.CharField(max_length=200, primary_key=True)
#     queue = models.CharField(max_length=50)
#     lobby_rank = models.CharField(max_length=50)
#     patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
#     date = models.DateField()
#     player_id = models.ManyToManyField(player)
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['queue'])
#         ]
#
#     def safe_get_game_id(game_id):
#         try:
#             return game_info.objects.get(game_id=game_id)
#         except game_info.DoesNotExist:
#             return None
#         except game_info.IntegrityError:
#             return None
#
#     def safe_get_player_id(player_id):
#         try:
#             return game_info.objects.filter(player_id=player_id)
#         except game_info.DoesNotExist:
#             return None
#
#     def safe_get_player_in_game_id(game_id, player_id):
#         try:
#             return game_info.objects.filter(game_id=game_id, player_id=player_id)
#         except game_info.DoesNotExist:
#             return None
#
#     def safe_add_player_id(player_id):
#         try:
#             return game_info.player_id.add(player_id=player_id)
#         except game_info.IntegrityError:
#             return None
#
#
# class game_unit(models.Model):
#     game_unit_id = models.AutoField(primary_key=True)
#     unit_id = models.ForeignKey(unit, on_delete=models.CASCADE)
#     patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
#     star = models.IntegerField()
#     item = models.ManyToManyField(item)
#
#     def safe_get(game_unit_id):
#         try:
#             return game_unit.objects.get(game_unit_id=game_unit_id)
#         except game_unit.DoesNotExist:
#             return None
#
#     def safe_get_unit(unit_id, patch_id, star, items):
#         try:
#             existCheck = game_unit.objects.filter(unit_id=unit_id, patch_id=patch_id, star=star).annotate(
#                 count=Count('item')).filter(count=len(items))
#             for pk in items:
#                 existCheck = existCheck.filter(item__pk=pk)
#             return existCheck
#         except:
#             return None
#
#
# class game_trait(models.Model):
#     game_trait_id = models.AutoField(primary_key=True)
#     trait_id = models.ForeignKey(trait, on_delete=models.CASCADE)
#     count = models.IntegerField()
#
#     def safe_get(game_trait_id):
#         try:
#             return game_trait.objects.get(game_trait_id=game_trait_id)
#         except game_trait.DoesNotExist:
#             return None
#
#     def safe_get_trait(trait_id, count):
#         try:
#             return game_trait.objects.get(trait_id=trait_id, count=count)
#         except game_trait.DoesNotExist:
#             return None
#
#
# class game(models.Model):
#     player_game_id = models.AutoField(primary_key=True)
#     player_id = models.ForeignKey(player, on_delete=models.CASCADE)
#     game_id = models.ForeignKey(game_info, on_delete=models.CASCADE)
#     icon = models.CharField(max_length=200)
#     placement = models.IntegerField()
#     level = models.IntegerField()
#     length = models.CharField(max_length=10)
#     round = models.CharField(max_length=10)
#     augment_id = models.ManyToManyField(augment)
#     headliner_id = models.ForeignKey(trait, on_delete=models.CASCADE, null=True, related_name='headliner')
#     game_trait_id = models.ManyToManyField(game_trait)
#     game_unit_id = models.ManyToManyField(game_unit)
#
#     def safe_get(player_game_id):
#         try:
#             return game.objects.get(player_game_id=player_game_id)
#         except game.DoesNotExist:
#             return None
#
#     def safe_get_player_game_id(player_id, game_id):
#         try:
#             return game.objects.get(player_id=player_id, game_id=game_id)
#         except game.DoesNotExist:
#             return None


    # def serialize(self):
    #     return {
    #         "Name": self.playerName,
    #         "GameID": self.gameID,
    #         "Queue": self.queue,
    #         "Placement": self.placement,
    #         "Level": self.level,
    #         "Length": self.length,
    #         "Round": self.round,
    #         "Augments": self.augments,
    #         "Headliner": self.headliner,
    #         "Traits": self.traits,
    #         "Units": self.units
    #     }




