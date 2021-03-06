import datetime
import discord
import json
import os
import random

print('Loading Data Holder...')
config_dir = os.path.join(os.getcwd(), 'config')


class DataCruncher:
    def __init__(self):
        # Load all Configs
        self._configs = dict()
        for file_name in os.listdir(config_dir):
            print(f'Loading Config {file_name}... ', end='')
            # Remove .json Extension for simpler access
            self._configs[file_name[:-5]] = self.load_config(file_name)
            print('done.')

        # Do not save the following files
        self._do_not_save = 'trivia'

        # Trivia User List for Timeout
        self._trivia_users = []
        self._TRIVIA_TIMEOUT_PER_USER = 10

        print('Done loading Data Holder.')

    @staticmethod
    def load_config(file_path):
        path = os.path.join(config_dir, file_path)
        with open(path) as f:
            return json.load(f)

    @staticmethod
    def save_config(json_data, file_path):
        path = os.path.join(config_dir, file_path)
        print(f'Saving Config in {path}... ', end='')
        with open(file_path, 'w') as f:
            json.dump(json_data, f)

    def save_all(self):
        print('Saving all Configs...')
        for file_name in self._configs:
            if file_name in self._do_not_save:
                continue
            file_name += '.json'
            path = os.path.join(config_dir, file_name)
            print(f'Saving Config {file_name}... ', end='')
            with open(path, 'w') as f:
                json.dump(self._configs[file_name[:-5]], f, indent=4)
            print(f'done.')
        print('Done saving Configs.')

    def get_prefix(self, key: str):
        try:
            return self._configs['messages']['prefixes'][key]
        except KeyError:
            print(f'Error trying to access Prefixes at key {key}')
            return None

    def add_custom_reaction(self, guild_id: str, name: str, contents: str, added_by: str):
        guild_id = str(guild_id)
        name = name.lower()
        if guild_id not in self._configs['custom_reactions']:
            self._configs['custom_reactions'][guild_id] = dict()
        if name not in self._configs['custom_reactions'][guild_id]:
            self._configs['custom_reactions'][guild_id][name] = []
        self._configs['custom_reactions'][guild_id][name].append([contents, added_by,
                                                                  str(datetime.datetime.now())[:-7]])
        print(f'Added new Custom Reaction for {guild_id} named {name}')

    def remove_custom_reaction(self, guild_id, name):
        # return true or false based on success
        pass

    def get_custom_reaction(self, guild_id: int, name: str):
        """
        Get a Custom Reaction on the Guild specified, with the name specified.
        
        :param guild_id: The Guild for which to access the Custom Reaction 
        :param name: The Name for which to get a Custom Reaction
        :return: None if the Guild or the Custom Reaction were not found.
        """
        guild_id = str(guild_id)
        name = name.lower()
        try:
            guild = self._configs['custom_reactions'][guild_id]
        except KeyError:
            return None
        else:
            try:
                reaction = guild[name]
            except KeyError:
                return None
            else:
                return reaction[random.randrange(0, len(reaction))]

    def get_all_custom_reactions_on_guild(self, guild_id: int):
        """
        Returns a List of all Custom Reactions on a Guild, in the following format:
        [ [contents, author, creation date, name], ... ]
        
        :param guild_id: The Guild for which to get all Custom Reactions. 
        :return: A List of all Custom Reactions, or None if none were found for the specified Guild.
        """
        guild_id = str(guild_id)
        all_custom_reactions = list()
        try:
            for namespace in self._configs['custom_reactions'][guild_id]:
                for custom_reaction in self._configs['custom_reactions'][guild_id][namespace]:
                    all_custom_reactions.append([custom_reaction[0], custom_reaction[1],
                                                 custom_reaction[2], namespace])
        except KeyError:
            return None
        else:
            return all_custom_reactions

    def get_twitch_subscriptions(self):
        try:
            return self._configs['twitch']['subscriptions']
        except KeyError:
            return None

    def get_stream_announcement_channel(self):
        return int(self._configs['twitch']['announcement_channel'])

    def get_moderators_and_above(self, guild_id: int):
        guild_id = str(guild_id)
        try:
            return self._configs['users'][guild_id]['moderators'] \
                   + self._configs['users'][guild_id]['administrators'] \
                   + self._configs['users']['owner']
        except KeyError:
            return self._configs['users']['owner']

    def get_admins_and_above(self, guild_id: int):
        guild_id = str(guild_id)
        try:
            return self._configs['users'][guild_id]['administrators'] \
                   + self._configs['users']['owner']
        except KeyError:
            return self._configs['users']['owner']

    def get_owner(self):
        return self._configs['users']['owner']

    def add_self_assignable_role(self, guild_id: int, role_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            self._configs['roles'][guild_id] = {'enabled': True, 'roles': [role_id], 'log': 0}
        else:
            self._configs['roles'][guild_id]['roles'].append(role_id)

    def remove_self_assignable_role(self, guild_id: int, role_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            return None
        try:
            self._configs['roles'][guild_id]['roles'].remove(role_id)
        except ValueError:
            return False
        return True

    def get_self_assignable_roles(self, guild_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            return None
        return self._configs['roles'][guild_id]['roles']

    def get_role_self_assigning_state(self, guild_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            return None
        return self._configs['roles'][guild_id]['enabled']

    def switch_role_self_assigning_state(self, guild_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            return None
        self._configs['roles'][guild_id]['enabled'] = not self._configs['roles'][guild_id]['enabled']
        return self.get_role_self_assigning_state(int(guild_id))

    def set_log_channel(self, guild_id: int, channel_id: int):
        if str(guild_id) not in self._configs['roles']:
            return False
        self._configs['roles'][str(guild_id)]['log'] = channel_id
        return True

    def get_log_channel(self, guild_id: int):
        return self._configs['roles'].get(str(guild_id))['log']

    def add_moderator(self, guild_id: int, moderator_user_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['users']:
            self._configs['users'][guild_id] = {'administrators': [], 'moderators': [moderator_user_id]}
        elif moderator_user_id not in self._configs['users'][guild_id]['moderators']:
            self._configs['users'][guild_id]['moderators'].append(moderator_user_id)

    def remove_moderator(self, guild_id: int, moderator_user_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['users']:
            return None
        try:
            self._configs['users'][guild_id]['moderators'].remove(moderator_user_id)
        except ValueError:
            return False
        return True

    def add_administrator(self, guild_id: int, administrator_user_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['users']:
            self._configs['users'][guild_id] = {'administrators': [administrator_user_id], 'moderators': []}
        elif administrator_user_id not in self._configs['users'][guild_id]['administrators']:
            self._configs['users'][guild_id]['administrators'].append(administrator_user_id)

    def remove_administrator(self, guild_id: int, administrator_user_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['users']:
            return None
        try:
            self._configs['users'][guild_id]['administrators'].remove(administrator_user_id)
        except ValueError:
            return False
        return True

    def get_role_servers(self):
        return self._configs['roles']

    def _get_currency_guild(self, guild_id: str):
        """
        A Helper function to ease getting Data from the Currency Configuration file.
        
        :param guild_id: The Guild ID for which to lookup Data
        :return: The Guild-specific Currency Configuration
        """
        if guild_id not in self._configs['currency']:
            self._configs['currency'][guild_id] = {'chance': 4, 'channels': [], 'total': 0, 'users': {}}
        return self._configs['currency'][guild_id]

    def _get_currency_user(self, user_id: str, guild_id: str):
        """
        A Helper function to ease getting Currency Data from a User.
        
        :param user_id: The User ID for which to get Data  
        :return: Data about the User
        """
        guild = self._get_currency_guild(guild_id)
        if user_id not in guild['users']:
            guild['users'][user_id] = {
                'name': '',
                'amount': 0
            }
        return guild['users'][user_id]

    def get_currency_channels(self, guild_id: int):
        """
        Get a List of Channel IDs for a given Guild in which Currency Generation is enabled.
         
        :param guild_id: The Guild for which to get the Channel IDs 
        :return: A List of Channel IDs in which Currency Generation is enabled for the given Guild
        """
        return self._get_currency_guild(str(guild_id))['channels']

    def get_currency_chance(self, guild_id: int):
        """
        Get the Spawn Chance (in percent) for Currency for the given Guild ID.
        
        :param guild_id: The Guild ID for which to get the Currency Spawn Chance
        :return: The Spawn Chance if the Guild has an entry for it
        """
        return self._get_currency_guild(str(guild_id))['chance']

    def set_currency_chance(self, guild_id: int, chance: int):
        """
        Set the Currency Spawn Chance (in percent) for the given Guild ID.

        :param guild_id: The Guild ID for which to set the Chance 
        :param chance: The Chance to set
        """
        self._get_currency_guild(str(guild_id))['chance'] = chance

    def add_currency_channel(self, guild_id: int, channel_id: int):
        """
        Adds a Channel in which Currency Generation is enabled to the given Guild.
        
        :param guild_id: The Guild ID for which to add a Currency-Enabled Channel
        :param channel_id: The Channel ID which should be added
        """
        self._get_currency_guild(str(guild_id))['channels'].append(channel_id)

    def remove_currency_channel(self, guild_id: int, channel_id: int):
        """
        Remove a Channel in which Currency Generation is enabled from the given Guild.
        
        :param guild_id: The Guild ID for which to remove the Currency-Enabled Channel 
        :param channel_id: The Channel ID which should be removed
        """
        self._get_currency_guild(str(guild_id))['channels'].remove(channel_id)

    def currency_increment_count(self, guild_id: int):
        """
        Increment the Counter for Currency on the given Guild. Used for Statistics.
        
        :param guild_id: The Guild ID for which to increment the Counter. 
        """
        self._get_currency_guild(str(guild_id))['total'] += 1

    def get_currency_total(self, guild_id: int):
        """
        Get the total amount of spawned Currency on the given Guild. Used for Statistics.
        
        :param guild_id: The Guild ID for which to get the Amount. 
        """
        return self._get_currency_guild(str(guild_id))['total']

    def get_currency_of_user(self, guild_id: int, member: discord.Member):
        """
        Get the Amount of Currency a User has.
        
        :param guild_id: The Guild in which to check for his Currency 
        :param member: The Member for which to get the Currency
        :return: The amount of Currency the Member has
        """
        user = self._get_currency_user(str(member.id), str(guild_id))
        user['name'] = member.display_name
        return user['amount']

    def modify_currency_of_user(self, guild_id: int, member: discord.Member, amount: int):
        """
        Modify the Currency of the specified User.
        
        :param guild_id: The Guild on which to modify his Currency. 
        :param member: The User whose Currency should be modified.
        :param amount: The amount by which to modify the Currency
        :return The new amount of Currency from the User.
        """
        user = self._get_currency_user(str(member.id), str(guild_id))
        user['name'] = member.display_name
        user['amount'] += amount
        return user['amount']

    def get_currency_guild_users(self, guild_id: int):
        """
        Get the dictionary of Users with their name, ID and Money on the given Guild.
        
        :param guild_id: The Guild for which to lookup the Users
        :return: A List of Users in the Format { "id": { "name": "xyz", "amount": 3 }, ... }  
        """
        return self._get_currency_guild(str(guild_id))['users']

    def _get_league_guild(self, guild_id: str):
        """
        Helper Function to get the League Configuration for the given guild ID.
        
        :param guild_id: The Guild's ID for which to perform the lookup
        :return: The Configuration for the Guild
        """
        if guild_id not in self._configs['league']:
            self._configs['league'][guild_id] = {'users': []}
        return self._configs['league'][guild_id]

    def get_league_guild_users(self, guild_id: int):
        """
        Get the people who are in the User Array for the given Guild.
        
        :param guild_id: The Guild ID for which to perform the lookups 
        :return: Summoner IDs for the Guild, if found.
        """
        return self._get_league_guild(str(guild_id))['users']

    def add_league_guild_user(self, guild_id: int, player_id: str, server: str):
        """
        Add a User to the League of Legends Players List of the given Guild.
        
        :param guild_id: The Guild on which to add the User 
        :param player_id: The Summoner ID which should be added
        :param server: The League of Legends Server where the ID lives
        :return: The refreshed List of League Users on the given Guild
        """
        self.get_league_guild_users(guild_id).append([player_id, server])
        return self.get_league_guild_users(guild_id)

    def remove_league_guild_user(self, guild_id: int, player_id: int):
        """
        Remove a User from the League of Legends Player List for the given Guild.
        
        :param guild_id: The Guild from which to remove the User 
        :param player_id: The Summoner ID that should be removed from the List
        :return: The refreshed List of League Users on the given Guild.
        """
        players = self.get_league_guild_users(guild_id)
        for item in players:
            if item[0] == player_id:
                players.remove(item)
        return self.get_league_guild_users(guild_id)

    def get_trivia(self, name: str):
        """
        Get a List of Trivia Questions and other Information for the specified Name.
        
        :param name: The topic for which to get Trivia Questions 
        :return: A dictionary containing the Mode and various questions for the Trivia game, or None if not found
        """
        return self._configs['trivia'].get(name, None)

    def get_all_trivia_topics(self):
        """
        Get all Available Trivia Topics
        
        :return: A list of available trivia topics 
        """
        return [x for x in self._configs['trivia']]

    def get_trivia_timeout_list(self):
        """
        Get the List of Users on the Trivia Timeout List
        
        :return: A list of Users on the Trivia Timeout List in the Format [ [user_id, datetime], ... ] 
        """
        return self._trivia_users

    def timeout_trivia_user(self, user_id: int) -> bool:
        """
        Set the trivia User timeout. If the datetime associated with the User is less than 5 minutes ago,
        this will return False. Otherwise, it will return True to indicate the new datetime has been set 
        and / or no previous were set.
        
        :param user_id: The User ID for which to get / set the Timeout 
        :return: True or False, see above
        """
        found = False
        for some_user_pair in self._trivia_users:
            if some_user_pair[0] == user_id:
                if datetime.datetime.now() - some_user_pair[1] > datetime.timedelta(minutes=10):
                    some_user_pair[1] = datetime.datetime.now()
                    return True
                return False
        if not found:
            self._trivia_users.append([user_id, datetime.datetime.now()])
        return True

    def timeout_user_is_not_being_time_outed(self, user_id: int) -> bool:
        """
        Returns True or False to indicate if the User will have to be time outed or not.
        Basically the Method above without assignment
        
        :param user_id: The User ID for which to check if it'S being timeouted 
        :return: True or False, see above.
        """
        for some_user_pair in self._trivia_users:
            if some_user_pair[0] == user_id:
                if datetime.datetime.now() - some_user_pair[1] > datetime.timedelta(minutes=10):
                    return True
                return False
        return True

# One central data Object to prevent Errors with multiple accesses to the Configurations
data = DataCruncher()

