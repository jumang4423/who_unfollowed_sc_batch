from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from configparser import ConfigParser
from src.util import get_home_dir, get_settings


def get_default_profile_path():
    settings = get_settings()
    dot_mozilla_path = settings[".mozilla_path"]
    config = ConfigParser()
    settings_path = f"{dot_mozilla_path}/firefox/profiles.ini"
    config.read(settings_path)
    profile_path = None
    for section in config.sections():
        if (
            config.has_option(section, "Default")
            and config.get(section, "Default") == "1"
        ):
            profile_path = config.get(section, "Path")
            break
    if profile_path is None:
        print("Default profile not found")
        exit(1)
    return f"{dot_mozilla_path}/firefox/{profile_path}"


def get_driver():
    default_profile_path = get_default_profile_path()
    print(f"Using profile: {default_profile_path}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--profile {default_profile_path}")
    driver = webdriver.Firefox(options=options)
    return driver
