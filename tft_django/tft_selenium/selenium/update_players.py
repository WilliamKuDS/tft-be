from datetime import timedelta, datetime, time
from django.db.models import Q
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()
from tft.models import player
from tft_query import tftQuery

def update_players(batch, days=7):
    playerUpdateList = player.objects.filter(Q(last_updated__gte=datetime.now() - timedelta(days=days)) | Q(last_updated__isnull=True))
    errorCounter = 0
    for players in playerUpdateList[:batch]:
        playerName = players.player_name
        playerRegion = players.region
        print("Updating {}".format(playerName))
        url = "https://www.metatft.com/player/" + playerRegion + "/" + playerName
        tft = tftQuery()
        tft.queryPlayer(url)
        print("Finished querying {}, saving date now".format(playerName))
        players.last_updated = datetime.now()
        players.save()
        errorCounter += tft.errorCounter
    print('Finished updating {} players'.format(batch))
    return errorCounter

for i in range(1000):
    try:
        number_of_players_to_update = 100
        errorCounter = update_players(number_of_players_to_update)
        print("Error rate: {}".format(errorCounter/number_of_players_to_update))
        time.sleep(10)
    except Exception as e:
        continue