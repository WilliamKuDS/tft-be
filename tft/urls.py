from django.urls import path

from . import views
from tft.api import augment_api, match_api, item_api, patch_api, account_api, summoner_api, set_api, trait_api, champion_api, profile_api, openai_api

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
    path("match/basic", match_api.getBasicMatch, name="getBasicMatch"),
    path("match/detailed", match_api.getDetailedMatch, name="getDetailedMatch"),
    path("match/create", match_api.createMatch, name="createGame"),
    path("match/update", match_api.updateMatch, name="updateGame"),
    path("match/delete", match_api.deleteMatch, name="deleteGame"),
    # ------------------------------------------
    # Patch API Paths
    path("patch", patch_api.readPatch, name="readPatch"),
    path("patch/all", patch_api.readPatchAll, name="readPatchAll"),
    path("patch/create", patch_api.createPatch, name="createPatch"),
    path("patch/update", patch_api.updatePatch, name="updatePatch"),
    path("patch/delete", patch_api.deletePatch, name="deletePatch"),
    # ------------------------------------------
    # Set API Paths
    path("set", set_api.readSet, name="readSet"),
    path("set/all", set_api.readSetAll, name="readSetAll"),
    path("set/create", set_api.createSet, name="createSet"),
    path("set/update", set_api.updateSet, name="updateSet"),
    path("set/delete", set_api.deleteSetByID, name="deleteSet"),
    # ------------------------------------------
    # Augments API Paths
    path("augment", augment_api.readAugment, name="readAugment"),
    path("augment/all/patch", augment_api.readAugmentAllByPatch, name="readAugmentAllByPatch"),
    path("augment/create", augment_api.createAugment, name="createAugment"),
    path("augment/update", augment_api.updateAugment, name="updateAugment"),
    path("augment/delete", augment_api.deleteAugment, name="deleteAugment"),
    # ------------------------------------------
    # Item API Paths
    path("item", item_api.readItem, name="readItem"),
    path("item/all", item_api.readItemAll, name="readItemAll"),
    path("item/all/patch", item_api.readItemAllByPatch, name="readItemAllByPatch"),
    path("item/create", item_api.createItem, name="createItem"),
    path("item/update", item_api.updateItem, name="updateItem"),
    path("item/delete", item_api.deleteItem, name="deleteItem"),
    # ------------------------------------------
    # Trait API Paths
    path("trait", trait_api.readTrait, name="readTrait"),
    path("trait/all/patch", trait_api.readTraitAllByPatch, name="readTraitAllByPatch"),
    path("trait/create", trait_api.createTrait, name="createTrait"),
    path("trait/update", trait_api.updateTrait, name="updateTrait"),
    path("traitid/delete", trait_api.deleteTraitByID, name="deleteTrait"),
    # ------------------------------------------
    # Champion API Paths
    path("champion", champion_api.readChampion, name="readChampion"),
    path("champion/all", champion_api.readChampionAll, name="readChampionAll"),
    path("champion/all/patch", champion_api.readChampionAllByPatch, name="readChampionAllByPatch"),
    path("champion/create", champion_api.createChampion, name="createChampion"),
    path("champion/update", champion_api.updateChampion, name="updateChampion"),
    path("champion/delete", champion_api.deleteChampion, name="deleteChampion"),
    # ------------------------------------------
    # OpenAI API Paths
    path("summoner/analyze", openai_api.analyze_performance, name="analyzePerformance"),
    path("summoner/recommendations", openai_api.match_recommendations, name="matchRecommendations"),
]
