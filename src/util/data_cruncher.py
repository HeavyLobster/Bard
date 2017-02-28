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

    def load_config(self, file_path):
        path = os.path.join(config_dir, file_path)
        with open(path) as f:
            return json.load(f)

    def save_config(self, json_data, file_path):
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

    def get_config(self, file, key=''):
        if key == '':
            try:
                return self._configs[file]
            except KeyError:
                print(f'Error trying to access Config {file}.')
        else:
            try:
                return self._configs[file][key]
            except KeyError:
                print(f'Error trying to access Config {file} at key \'{key}\'.')

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
        guild_id = str(guild_id)
        all_custom_reactions = list()
        try:
            for namespace in self._configs['custom_reactions'][guild_id]:
                for custom_reaction in self._configs['custom_reactions'][guild_id][namespace]:
                    all_custom_reactions.append([custom_reaction[0], custom_reaction[1], custom_reaction[2]])
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
            return None

    def get_admins_and_above(self, guild_id: int):
        guild_id = str(guild_id)
        try:
            return self._configs['users'][guild_id]['administrators'] \
                   + self._configs['users']['owner']
        except KeyError:
            print(f'Failed to fetch Admins for Server with ID {guild_id}.')

    def get_owner(self):
        return self._configs['users']['owner']

    def add_self_assignable_role(self, guild_id: int, role_id: int):
        guild_id = str(guild_id)
        if guild_id not in self._configs['roles']:
            self._configs['roles'][guild_id] = {'enabled': True, 'roles': [role_id]}
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
        return self.get_role_self_assigning_state(guild_id)

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

    def get_currency_server(self, guild_id: int):
        return self._configs['currency'].get(str(guild_id))

    def _get_currency_user(self, guild_id: int, player_id: int, money=0):
        server = self.get_currency_server(guild_id)
        if server is None:
            self._configs[guild_id] = {player_id: money}  # Starts at 0
        elif player_id not in self._configs[guild_id]:
            self._configs[guild_id].update({player_id: money})
        else:
            if self._configs[guild_id][player_id] + money <= 0:
                print(f'Can\'t change money of {player_id} on {guild_id} by {money}, would be negative.')
            else:
                self._configs[guild_id][player_id] += money
        return self._configs[guild_id][player_id]

    def get_currency_of_user(self, guild_id: int, player_id: int):
        return self._get_currency_user(guild_id, player_id, 0)

    def change_currency_of_user(self, guild_id: int, player_id: int, amount: int):
        self._get_currency_user(guild_id, player_id, amount)


# One central data Object to prevent Errors with the Configurations
data = DataCruncher()

