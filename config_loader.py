import os
import json

CONFIG_PATH = os.path.expanduser("~/.xitecli/config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("Config not found. Please run `xitecli configure`.")
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    # Ensure both sections exist
    if "minio" not in config:
        raise ValueError("Missing 'minio' section in config.")
    if "r2" not in config:
        config["r2"] = {}

    return config


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
