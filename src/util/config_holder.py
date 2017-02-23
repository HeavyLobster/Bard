import datetime
import json
import os
import random

print('Loading Config Holder...')
config_dir = os.path.join(os.getcwd(), 'config')


class ConfigHolder:
    def __init__(self):
        # Load all Configs
        self._configs = dict()
        for file_name in os.listdir(config_dir):
            print(f'Loading Config {file_name}... ', end='')
            # Remove .json Extension for simpler access
            self._configs[file_name[:-5]] = self.load_config(file_name)
            print('done.')
        print('Done loading Config Holder.')

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
            return 'There are **no Quotes** for this guild.'
        else:
            try:
                reaction = guild[name]
            except KeyError:
                return 'No Quote found.'
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
