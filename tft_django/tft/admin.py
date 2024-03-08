from django.contrib import admin
from .models import player
from .models import patch
from .models import augment
from .models import trait
from .models import item
from .models import unit
from .models import game_unit
from .models import game_info
from .models import game
from .models import set
from .models import game_trait

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
