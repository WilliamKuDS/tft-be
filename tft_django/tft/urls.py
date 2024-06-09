from django.urls import path

from . import views
from tft.api import augment_api, match_api, item_api, patch_api, account_api, summoner_api, set_api, trait_api, champion_api, profile_api

urlpatterns = [
    path("", views.index, name="index"),
    # ------------------------------------------
    # Account API Paths
    path("account", account_api.createUpdateAccount, name="createUpdateAccount"),
    path("account/create", account_api.createAccount, name="createPlayer"),
    path("account/update", account_api.updateAccount, name="updatePlayer"),
    path("account/delete", account_api.deleteAccount, name="deleteAccount"),
    # ------------------------------------------
    # Summoner API Paths
    path("summoner", summoner_api.readSummoner, name="readSummoner"),
    path("summoner/create", summoner_api.createSummoner, name="createSummoner"),
    path("summoner/update", summoner_api.updateSummoner, name="updateSummoner"),
    path("summoner/delete", summoner_api.deleteSummoner, name="deleteSummoner"),
    # ------------------------------------------
    # Profile API Paths
    path("profile", profile_api.createUpdateProfile, name="createUpdateProfile"),
    # ------------------------------------------
    # Match API Paths
    path("match", match_api.readMatch, name="readGame"),
    path("match/create", match_api.createMatch, name="createGame"),
    path("match/update", match_api.updateMatch, name="updateGame"),
    path("match/delete", match_api.deleteMatch, name="deleteGame"),
    # ------------------------------------------
    # Item API Paths
    path("item", item_api.readItem, name="readItem"),
    path("item/all", item_api.readItemAll, name="readItemAll"),
    path("item/create", item_api.createItem, name="createItem"),
    path("item/update", item_api.updateItem, name="updateItem"),
    path("item/delete", item_api.deleteItem, name="deleteItem"),
    # ------------------------------------------
    # Augments API Paths
    path("augment", augment_api.readAugment, name="readAugment"),
    path("augment/create", augment_api.createAugment, name="createAugment"),
    path("augment/update", augment_api.updateAugment, name="updateAugment"),
    path("augment/delete", augment_api.deleteAugment, name="deleteAugment"),
    # ------------------------------------------
    # Patch API Paths
    path("patch", patch_api.readPatch, name="readPatch"),
    path("patch/create", patch_api.createPatch, name="createPatch"),
    path("patch/update", patch_api.updatePatch, name="updatePatch"),
    path("patch/delete", patch_api.deletePatch, name="deletePatch"),
    # ------------------------------------------
    # Set API Paths
    path("set", set_api.readSet, name="readSet"),
    path("set/create", set_api.createSet, name="createSet"),
    path("set/update", set_api.updateSet, name="updateSet"),
    path("set/delete", set_api.deleteSetByID, name="deleteSet"),
    # ------------------------------------------
    # Trait API Paths
    path("trait", trait_api.readTrait, name="readTrait"),
    path("trait/create", trait_api.createTrait, name="createTrait"),
    path("trait/update", trait_api.updateTrait, name="updateTrait"),
    path("traitid/delete", trait_api.deleteTraitByID, name="deleteTrait"),
    # ------------------------------------------
    # Unit API Paths
    path("unit", champion_api.readChampion, name="readChampion"),
    path("unit/all", champion_api.readChampionAll, name="readChampionAll"),
    path("unit/create", champion_api.createChampion, name="createChampion"),
    path("unit/update", champion_api.updateChampion, name="updateChampion"),
    path("unit/delete", champion_api.deleteChampion, name="deleteChampion"),
]
