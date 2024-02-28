from django.db.utils import IntegrityError
from .models import Game

def saveJSONToDatabase(body):
    try:
        game_instance = Game.objects.create(
            playerGameID=body['PlayerGameID'],
            playerName=body['PlayerName'],
            gameID=body["GameID"],
            queue=body["Queue"],
            placement=body["Placement"],
            level=body["Level"],
            length=body["Length"],
            round=body["Round"],
            augments=body["Augments"],
            headliner=body["Headliner"],
            traits=body["Traits"],
            units=body["Units"]
        )
        game_instance.save()
    except IntegrityError as e:
        print("Data Exists, Error: {}".format(e))