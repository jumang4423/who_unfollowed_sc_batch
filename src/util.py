import os
import json


def get_id_by_url(url):
    return url.split("/")[-1]


def make_tmp_dir():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    if not os.path.exists("tmp/diff_cache.json"):
        with open("tmp/diff_cache.json", "w") as f:
            json.dump({}, f)


def get_home_dir():
    return os.path.expanduser("~")


def get_settings():
    filep = "settings.json"
    if not os.path.exists(filep):
        print("settings.json not found")
        exit(1)
    with open(filep, "r") as f:
        settings = json.load(f)
    # validation
    dot_mozilla_path = settings[".mozilla_path"]
    if not os.path.exists(dot_mozilla_path):
        print(".mozilla_path not found")
        print(f"edit settings.json: {dot_mozilla_path}")
        exit(1)

    return settings
