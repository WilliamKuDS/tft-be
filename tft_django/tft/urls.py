from django.urls import path

from . import views
from tft.api import augment_api, gameInfo_api, game_api, item_api, patch_api, player_api, set_api, trait_api, unit_api, \
    gameTrait_api, gameUnit_api

urlpatterns = [
    path("", views.index, name="index"),
    # ------------------------------------------
    # Augments API Paths
    path("augment", augment_api.readAugmentByName, name="readAugmentByName"),
    path("augmentid", augment_api.readAugmentByID, name="readAugmentByID"),
    path("augment/create", augment_api.createAugment, name="createAugment"),
    path("augment/update", augment_api.updateAugment, name="updateAugment"),
    path("augment/delete", augment_api.deleteAugmentByName, name="deleteAugmentByName"),
    path("augmentid/delete", augment_api.deleteAugmentByID, name="deleteAugmentByID"),
    # ------------------------------------------
    # Game API Paths
    path("game", game_api.readGameByPlayerGame, name="readGameByName"),
    path("gameid", game_api.readGameByID, name="readGameByID"),
    path("game/create", game_api.createGame, name="createGame"),
    path("game/update", game_api.updateGame, name="updateGame"),
    path("game/delete", game_api.deleteGameByPlayerGame, name="deleteGameByName"),
    path("gameid/delete", game_api.deleteGameByID, name="deleteGameByID"),
    # ------------------------------------------
    # GameInfo API Paths
    path("game/info", gameInfo_api.readGameInfoByGameID, name="readGameInfoByGameID"),
    path("game/info/playerid", gameInfo_api.readGameInfoByPlayerID, name="readGameInfoByGameID"),
    path("game/info/gameid", gameInfo_api.readGameInfoByGameID, name="readGameInfoByGameID"),
    path("game/info/playername", gameInfo_api.readGameInfoByPlayerName, name="readGameInfoByPlayerName"),
    path("game/info/create", gameInfo_api.createGameInfo, name="createGameInfo"),
    path("game/info/update", gameInfo_api.updateGameInfo, name="updateGameInfo"),
    path("game/info/delete", gameInfo_api.deleteGameInfoByGameID, name="deleteGameInfoByGameID"),
    # ------------------------------------------
    # GameTrait API Paths
    path("game/trait", gameTrait_api.readGameTrait, name="readGameTrait"),
    path("game/trait/create", gameTrait_api.createGameTrait, name="createTrait"),
    path("game/trait/update", gameTrait_api.updateGameTrait, name="updateTrait"),
    path("game/trait/delete", gameTrait_api.deleteGameTrait, name="deleteTrait"),
    # ------------------------------------------
    # GameUnit API Paths
    path("game/unit", gameUnit_api.readGameUnit, name="readGameUnit"),
    path("game/unit/create", gameUnit_api.createGameUnit, name="createGameUnit"),
    path("game/unit/update", gameUnit_api.updateGameUnit, name="updateGameUnit"),
    path("game/unit/delete", gameUnit_api.deleteGameUnit, name="deleteGameUnit"),
    # ------------------------------------------
    # Item API Paths
    path("item", item_api.readItemByName, name="readItemByName"),
    path("item/all", item_api.readItemAll, name="readItemAll"),
    path("itemid", item_api.readItemByID, name="readItemByID"),
    path("item/create", item_api.createItem, name="createItem"),
    path("item/update", item_api.updateItem, name="updateItem"),
    path("item/delete", item_api.deleteItemByName, name="deleteItemByName"),
    path("itemid/delete", item_api.deleteItemByID, name="deleteItemByID"),
    # ------------------------------------------
    # Patch API Paths
    path("patch", patch_api.readPatchByID, name="readPatchByID"),
    path("patchset", patch_api.readPatchBySetID, name="readPatchBySetID"),
    path("patch/create", patch_api.createPatch, name="createPatch"),
    path("patch/update", patch_api.updatePatch, name="updatePatch"),
    path("patch/delete", patch_api.deletePatchByID, name="deletePatchById"),
    # ------------------------------------------
    # Player API Paths
    path("playerid", player_api.readPlayerByPUUID, name="readPlayerByPUUID"),
    path("player", player_api.readPlayerByValues, name="readPlayerByValue"),
    path("player/create", player_api.createPlayer, name="createPlayer"),
    path("player/update", player_api.updatePlayer, name="updatePlayer"),
    path("player/delete", player_api.deletePlayerByValues, name="deletePlayerByValue"),
    path("playerid/delete", player_api.deletePlayerByID, name="deletePlayerByID"),
    # ------------------------------------------
    # Set API Paths
    path("set", set_api.readSetByName, name="readSetByName"),
    path("setid", set_api.readSetByID, name="readSetByID"),
    path("set/create", set_api.createSet, name="createSet"),
    path("set/update", set_api.updateSet, name="updateSet"),
    path("set/delete", set_api.deleteSetByID, name="deleteSetByID"),
    # ------------------------------------------
    # Trait API Paths
    path("trait", trait_api.readTraitByName, name="readTraitByName"),
    path("traitid", trait_api.readTraitByID, name="readTraitByID"),
    path("trait/create", trait_api.createTrait, name="createTrait"),
    path("trait/update", trait_api.updateTrait, name="updateTrait"),
    path("trait/delete", trait_api.deleteTraitByName, name="deleteTraitByName"),
    path("traitid/delete", trait_api.deleteTraitByID, name="deleteTraitByID"),
    # ------------------------------------------
    # Unit API Paths
    path("unit", unit_api.readUnitByName, name="readUnitByName"),
    path("unitid", unit_api.readUnitByID, name="readUnitByID"),
    path("unit/all", unit_api.readUnitAll, name="readUnitAll"),
    path("unit/create", unit_api.createUnit, name="createUnit"),
    path("unit/update", unit_api.updateUnit, name="updateUnit"),
    path("unit/delete", unit_api.deleteUnitByName, name="deleteUnitByName"),
    path("unitid/delete", unit_api.deleteUnitByID, name="deleteUnitByID"),
]
