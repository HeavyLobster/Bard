import datetime
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
            print(f'Failed to fetch Moderators for Server with ID {guild_id}.')
            return self._configs['users']['owner']

    def get_admins_and_above(self, guild_id: int):
        guild_id = str(guild_id)
        try:
            return self._configs['users'][guild_id]['administrators'] \
                   + self._configs['users']['owner']
        except KeyError:
            print(f'Failed to fetch Admins for Server with ID {guild_id}.')
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
            self._configs['currency'][guild_id] = {'chance': 3, 'channels': [], 'users': []}
        return self._configs['currency'][guild_id]

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

# One central data Object to prevent Errors with multiple accesses to the Configurations
data = DataCruncher()

