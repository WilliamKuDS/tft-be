from django.urls import path

from . import views
from tft.api import augment_api, match_api, item_api, patch_api, account_api, summoner_api, set_api, trait_api, champion_api, profile_api

urlpatterns = [
    path("", views.index, name="index"),
    # ------------------------------------------
    # Account API Paths
    path("account", account_api.createUpdateAccount, name="createUpdateAccount"),
    path("account/create", account_api.createAccount, name="createPlayer"),
    path("account/read", account_api.readAccount, name="readPlayer"),
    path("account/update", account_api.updateAccount, name="updatePlayer"),
    path("account/delete", account_api.deleteAccount, name="deleteAccount"),
    # ------------------------------------------
    # Summoner API Paths
    path("summoner", summoner_api.createUpdateSummoner, name="createUpdateAccount"),
    path("summoner/create", summoner_api.createSummoner, name="createSummoner"),
    path("summoner/read", summoner_api.readSummoner, name="readSummoner"),
    path("summoner/update", summoner_api.updateSummoner, name="updateSummoner"),
    path("summoner/delete", summoner_api.deleteSummoner, name="deleteSummoner"),
    # ------------------------------------------
    # Profile API Paths
    path("profile", profile_api.createUpdateProfile, name="createUpdateProfile"),
    # ------------------------------------------
    # Match API Paths
    path("match", match_api.readMatch, name="readGameByName"),
    path("match/create", match_api.createMatch, name="createGame"),
    path("match/update", match_api.updateMatch, name="updateGame"),
    path("match/delete", match_api.deleteMatch, name="deleteGameByID"),
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
    # Augments API Paths
    path("augment", augment_api.readAugmentByName, name="readAugmentByName"),
    path("augmentid", augment_api.readAugmentByID, name="readAugmentByID"),
    path("augment/create", augment_api.createAugment, name="createAugment"),
    path("augment/update", augment_api.updateAugment, name="updateAugment"),
    path("augment/delete", augment_api.deleteAugmentByName, name="deleteAugmentByName"),
    path("augmentid/delete", augment_api.deleteAugmentByID, name="deleteAugmentByID"),
    # ------------------------------------------
    # Patch API Paths
    path("patch", patch_api.readPatchByID, name="readPatchByID"),
    path("patchset", patch_api.readPatchBySetID, name="readPatchBySetID"),
    path("patch/create", patch_api.createPatch, name="createPatch"),
    path("patch/update", patch_api.updatePatch, name="updatePatch"),
    path("patch/delete", patch_api.deletePatchByID, name="deletePatchById"),
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
    path("unit", champion_api.readUnitByName, name="readUnitByName"),
    path("unitid", champion_api.readUnitByID, name="readUnitByID"),
    path("unit/all", champion_api.readUnitAll, name="readUnitAll"),
    path("unit/create", champion_api.createUnit, name="createUnit"),
    path("unit/update", champion_api.updateUnit, name="updateUnit"),
    path("unit/delete", champion_api.deleteUnitByName, name="deleteUnitByName"),
    path("unitid/delete", champion_api.deleteUnitByID, name="deleteUnitByID"),
]
