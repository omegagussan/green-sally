#!/usr/bin/python3
import json

state_file_path = "resources/state.json"
version = 0


class StateVersionException(Exception):
    pass


def _get_state():
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


class State:
    def __init__(self):
        self.state = _get_state()
        pass

    def set_state_value(self, key, value):
        self.state[key] = value

    def get_value(self, key):
        return self.state[key]

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_state(self.state)
