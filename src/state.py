#!/usr/bin/python3
import json

state_file_path = "resources/state.json"
version = 0


class StateVersionException(Exception):
    pass


def get_state():
    with open(state_file_path, 'r') as state_file:
        data = json.load(state_file)
        if data['version'] == 0:
            data.pop('version', None)
            return data
        else:
            raise StateVersionException(f"No logic to parse state with version: {version} implemented")


def set_state(d):
    dc = d.copy()
    dc['version'] = version
    with open(state_file_path, 'w') as state_file:
        json.dump(dc, state_file, sort_keys=True, indent=4)


def set_state_value(key, value):
    dc = get_state()
    dc['version'] = version
    dc[key] = value
    with open(state_file_path, 'w') as state_file:
        json.dump(dc, state_file, sort_keys=True, indent=4)


def get_value(key):
    dc = get_state()
    return dc[key]
