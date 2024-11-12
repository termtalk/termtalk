from core.config_loader import load_config
from core.storage import Storage
import sys


def init():

    storage = Storage()
    verbose = storage.get("verbose")
    config = load_config(verbose)
    if config:
        storage.set("config", config)
    else:
        print("Configuration loading failed.")
        sys.exit(1)
    