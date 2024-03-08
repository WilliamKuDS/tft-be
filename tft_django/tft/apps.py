from django.apps import AppConfig
from django.core.serializers.json import Serializer as DjangoSerializer
from django.utils.encoding import smart_str
from django.core.serializers import BUILTIN_SERIALIZERS

BUILTIN_SERIALIZERS['json'] = 'tft.apps'


class TftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tft'

class Serializer(DjangoSerializer):  # name must be Serializer
    def get_dump_object(self, obj):
        self._current['game_id'] = smart_str(obj._get_pk_val(), strings_only=True)
        return self._current
