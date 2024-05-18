from src.util import get_settings
from browsermobproxy import Server


def get_server():
    settings = get_settings()
    conf_name = "browsermob-proxy-path"
    if conf_name not in settings:
        print(f"{conf_name} not found in settings")
        exit(1)
    server = Server(settings[conf_name])

    return server
