# Import Riot API Wrapper
import os
from cassiopeia import dto
from cassiopeia import riotapi

# Set API key
riotapi.set_api_key(os.environ['LEAGUE_TOKEN'])


# Set a new region if it's not currently selected
def set_region(new_region):
    riotapi.set_region(new_region)


# Convert a Player Name into a Player ID
def get_id_by_name(player_name, region):
    print(f'Getting ID for Name {player_name} on {region}')
    set_region(region)
    return riotapi.get_summoner_by_name(player_name).id


# Get a Summoner by ID
def get_summoner_by_name(player_name, region):
    set_region(region)
    return riotapi.get_summoner_by_name(player_name)


def get_summoner_by_id(player_id, region):
    print(f'Getting Summoner for ID {player_id} on {region}')
    set_region(region)
    return riotapi.get_summoner_by_id(player_id)


# Get someone's Champ Mastery Points on Bard
def get_mastery_points(name, region):
    return dto.championmasteryapi.get_champion_mastery(get_id_by_name(name, region), 432).championPoints


def get_current_game(name, region):
    return riotapi.get_current_game(get_summoner_by_name(name, region))


def get_ranked_info(player_id, region):
    print(f'Getting Rank for {player_id} on {region}')
    return riotapi.get_ranked_stats(get_summoner_by_id(player_id, region))[None]
