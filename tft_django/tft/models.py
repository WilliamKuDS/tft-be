from django.db import models
from django.db.models import Count

# Create your models here.
class player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=200)
    region = models.CharField(max_length=2)
    player_rank = models.CharField(max_length=200)
    player_lp = models.IntegerField()
    icon = models.CharField(max_length=200)
    last_updated = models.DateField(null=True)

    def safe_get(player_name, region):
        try:
            return player.objects.get(player_name=player_name, region=region)
        except player.DoesNotExist:
            return None

    def safe_get_id(player_id):
        try:
            return player.objects.get(player_id=player_id)
        except player.DoesNotExist:
            return None

class set(models.Model):
    set_id = models.FloatField(primary_key=True)
    set_name = models.CharField(max_length=200)

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
    patch_id = models.IntegerField(primary_key=True)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)
    revival_set_id = models.ForeignKey(set, on_delete=models.CASCADE, related_name='revival_set_id', blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200)

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

class game_info(models.Model):
    game_id = models.CharField(max_length=200, primary_key=True)
    queue = models.CharField(max_length=50)
    lobby_rank = models.CharField(max_length=50)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    date = models.DateField()
    player_id = models.ManyToManyField(player)

    class Meta:
        indexes = [
            models.Index(fields=['queue'])
        ]

    def safe_get_game_id(game_id):
        try:
            return game_info.objects.get(game_id=game_id)
        except game_info.DoesNotExist:
            return None
        except game_info.IntegrityError:
            return None

    def safe_get_player_id(player_id):
        try:
            return game_info.objects.filter(player_id=player_id)
        except game_info.DoesNotExist:
            return None

    def safe_get_player_in_game_id(game_id, player_id):
        try:
            return game_info.objects.filter(game_id=game_id, player_id=player_id)
        except game_info.DoesNotExist:
            return None

    def safe_add_player_id(player_id):
        try:
            return game_info.player_id.add(player_id=player_id)
        except game_info.IntegrityError:
            return None


class augment(models.Model):
    augment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    tier = models.IntegerField()
    description = models.CharField(max_length=2000)
    icon = models.CharField(max_length=500, null=True, blank=True)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)

    def safe_get_id(augment_id):
        try:
            return augment.objects.get(augment_id=augment_id)
        except augment.DoesNotExist:
            return None

    def safe_get_name(name, set_id):
        try:
            return augment.objects.get(name=name, set_id=set_id)
        except augment.DoesNotExist:
            return None

class synergy(models.Model):
    synergy_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    description = models.CharField(max_length=1000)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)

    def safe_get_id(synergy_id):
        try:
            return synergy.objects.get(synergy_id=synergy_id)
        except synergy.DoesNotExist:
            return None

    def safe_get_by_trait(name, count, set_id):
        try:
            return synergy.objects.get(name=name, count=count, set_id=set_id)
        except synergy.DoesNotExist:
            return None

class trait(models.Model):
    trait_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    synergy = models.ManyToManyField(synergy)
    icon = models.CharField(max_length=500, null=True, blank=True)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)

    def safe_get_id(trait_id):
        try:
            return trait.objects.get(trait_id=trait_id)
        except trait.DoesNotExist:
            return None

    def safe_get_name(name, set_id):
        try:
            return trait.objects.get(name=name, set_id=set_id)
        except trait.DoesNotExist:
            return None



class item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    recipe = models.ManyToManyField('self', blank=True)
    description = models.CharField(max_length=1000)
    icon = models.CharField(max_length=500, null=True, blank=True)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)

    def safe_get_id(item_id):
        try:
            return item.objects.get(item_id=item_id)
        except item.DoesNotExist:
            return None

    def safe_get_name(name, set_id):
        try:
            return item.objects.get(name=name, set_id=set_id)
        except item.DoesNotExist:
            return None

class unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    tier = models.IntegerField()
    trait = models.ManyToManyField(trait)
    ability_name = models.CharField(max_length=200)
    ability_description = models.CharField(max_length=1000)
    ability_info = models.CharField(max_length=1000)
    ability_icon = models.CharField(max_length=500)
    stats = models.CharField(max_length=1000)
    icon = models.CharField(max_length=200, null=True, blank=True)
    set_id = models.ForeignKey(set, on_delete=models.CASCADE)

    def safe_get_id(unit_id):
        try:
            return unit.objects.get(unit_id=unit_id)
        except unit.DoesNotExist:
            return None

    def safe_get_name(name, set_id):
        try:
            return unit.objects.get(name=name, set_id=set_id)
        except unit.DoesNotExist:
            return None

class game_unit(models.Model):
    game_unit_id = models.AutoField(primary_key=True)
    unit_id = models.ForeignKey(unit, on_delete=models.CASCADE)
    patch_id = models.ForeignKey(patch, on_delete=models.CASCADE)
    star = models.IntegerField()
    item = models.ManyToManyField(item)

    def safe_get(game_unit_id):
        try:
            return game_unit.objects.get(game_unit_id=game_unit_id)
        except game_unit.DoesNotExist:
            return None

    def safe_get_unit(unit_id, patch_id, star, items):
        try:
            existCheck = game_unit.objects.filter(unit_id=unit_id, patch_id=patch_id, star=star).annotate(
                count=Count('item')).filter(count=len(items))
            for pk in items:
                existCheck = existCheck.filter(item__pk=pk)
            return existCheck
        except:
            return None


class game_trait(models.Model):
    game_trait_id = models.AutoField(primary_key=True)
    trait_id = models.ForeignKey(trait, on_delete=models.CASCADE)
    count = models.IntegerField()

    def safe_get(game_trait_id):
        try:
            return game_trait.objects.get(game_trait_id=game_trait_id)
        except game_trait.DoesNotExist:
            return None

    def safe_get_trait(trait_id, count):
        try:
            return game_trait.objects.get(trait_id=trait_id, count=count)
        except game_trait.DoesNotExist:
            return None


class game(models.Model):
    player_game_id = models.AutoField(primary_key=True)
    player_id = models.ForeignKey(player, on_delete=models.CASCADE)
    game_id = models.ForeignKey(game_info, on_delete=models.CASCADE)
    icon = models.CharField(max_length=200)
    placement = models.IntegerField()
    level = models.IntegerField()
    length = models.CharField(max_length=10)
    round = models.CharField(max_length=10)
    augment_id = models.ManyToManyField(augment)
    headliner_id = models.ForeignKey(trait, on_delete=models.CASCADE, null=True, related_name='headliner')
    game_trait_id = models.ManyToManyField(game_trait)
    game_unit_id = models.ManyToManyField(game_unit)

    def safe_get(player_game_id):
        try:
            return game.objects.get(player_game_id=player_game_id)
        except game.DoesNotExist:
            return None

    def safe_get_player_game_id(player_id, game_id):
        try:
            return game.objects.get(player_id=player_id, game_id=game_id)
        except game.DoesNotExist:
            return None


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




