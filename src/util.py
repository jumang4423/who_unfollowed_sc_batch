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
    if not os.path.exists("tmp/followers_cache.json"):
        with open("tmp/followers_cache.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("tmp/force_cache.json"):
        with open("tmp/force_cache.json", "w") as f:
            json.dump({}, f)


def get_home_dir():
    return os.path.expanduser("~")
