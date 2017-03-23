# Import Riot API Wrapper
import os
from cassiopeia import dto
from cassiopeia import riotapi

# Set API key
riotapi.set_api_key(os.environ['LEAGUE_TOKEN'])


def set_region(new_region: str):
    """
    Set a new Region for the API to make Calls on.
    
    :param new_region: The New Region to set 
    """
    riotapi.set_region(new_region)


def get_id_by_name(player_name, region):
    """
    Get a Player ID by the name and region.
    
    :param player_name: The Player's Summoner Name
    :param region: The Region the Player is on
    :return: The ID of the Summoner
    """
    return get_summoner_by_name(player_name, region).id


def get_summoner_by_name(player_name, region):
    """
    Get a Summoner Object by his Name and Region
    
    :param player_name: The Summoner Name
    :param region: The Region on which to get the Summoner
    :return: The Summoner
    """
    set_region(region)
    return riotapi.get_summoner_by_name(player_name)


def get_summoner_by_id(player_id, region):
    """
    Get a Summoner Object based on their Summoner ID and Region.
    
    :param player_id: The Player ID to be looked up
    :param region: The Region on which to look up the given Player ID
    :return: A Summoner Object
    """
    set_region(region)
    return riotapi.get_summoner_by_id(player_id)


def get_mastery_points(name, region, champ_id: int=432):
    """
    Get someone's Champ Mastery Points on Bard
    
    :param name: The Name of the Player to lookup 
    :param region: The Region of the Player
    :param champ_id: The Champion ID for which to get the Points. Defaults to Bard.
    :return: The Points of the given Person on Bard
    """
    return dto.championmasteryapi.get_champion_mastery(get_id_by_name(name, region), champ_id).championPoints


def get_mastery_points_by_id(player_id, region, champ_id: int=432):
    """
    Get someone's Champ Mastery Points on Bard by their ID and Server
    
    :param player_id: The ID of the Summoner for which to lookup the Points 
    :param region: The Region of the Summoner
    :param champ_id: The Champion ID for which to get the Points. Defaults to Bard.
    :return: The Mastery Points of the Player on Bard
    """
    set_region(region)
    return dto.championmasteryapi.get_champion_mastery(player_id, champ_id).championPoints
