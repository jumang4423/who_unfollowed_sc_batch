SC_USER_ID = "jumang4423"

from selenium import webdriver
import time
import json
import os
import requests
from tqdm import tqdm
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import firefox options
from selenium.webdriver.firefox.options import Options


def get_id_by_url(url):
    return url.split("/")[-1]


def make_tmp_dir():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")


def get_follower_cnt():
    url = f"https://soundcloud.com/{SC_USER_ID}"
    r = requests.get(url)
    r_text = r.text
    el = "followers_count"
    follower_cnt = re.search(f'"{el}":(\d+)', r_text).group(1)
    return int(follower_cnt)


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument(
        "--profile /home/jumang4423/snap/firefox/common/.mozilla/firefox/irk0149j.jumango",
    )
    driver = webdriver.Firefox(options=options)
    return driver


def get_followers_by_fetched(driver):
    el = "userBadgeListItem__heading"
    followers_obj = driver.find_elements(By.CLASS_NAME, el)
    return followers_obj


def get_followers(driver):
    url = f"https://soundcloud.com/{SC_USER_ID}/followers"
    driver.get(url)

    # start scrolling
    all_followers = get_follower_cnt()
    pbar = tqdm(total=all_followers, desc="Fetching followers...")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            followers_cnt = len(get_followers_by_fetched(driver))
            pbar.update(followers_cnt - pbar.n)
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.loading.regular.m-padded")
                )
            )
        except:
            pbar.close()
            break

    # finally extract the followers
    followers_obj = get_followers_by_fetched(driver)
    followers = {}
    for follower_obj in followers_obj:
        follower_url = follower_obj.get_attribute("href")
        follower_id = get_id_by_url(follower_url)
        followers[follower_id] = follower_obj.text
    return followers


def save_followers(followers):
    cur_unix = int(time.time())
    with open(f"tmp/{SC_USER_ID}_{cur_unix}.json", "w") as f:
        f.write(json.dumps(followers))


def update_followers():
    driver = get_driver()
    followers = get_followers(driver)
    save_followers(followers)


def get_set_two_timestamp() -> list[tuple]:
    """
    get user latest two timestamp json
    """
    files = os.listdir("tmp")
    files = [f for f in files if f.startswith(SC_USER_ID)]
    files = sorted(files, reverse=True)
    if len(files) < 2:
        return []
    diffs = []
    while True:
        if len(files) < 2:
            break
        latest = files.pop(0)
        second_latest = files[0]
        diffs.append((latest, second_latest))

    return diffs


def get_latesest_two_timestamp():
    """
    get user latest two timestamp json
    """
    diffs = get_set_two_timestamp()
    if len(diffs) == 0:
        return None, None
    return diffs[0]


class UserDiffState:
    def __init__(self, id, name, unfollowed, newly_followed):
        self.id = id
        self.name = name
        self.unfollowed = unfollowed
        self.newly_followed = newly_followed


def get_diff_follower(latest, sencond_latest) -> list[UserDiffState]:
    if latest is None:
        print("warning: no latest timestamp")
        return []
    with open(f"tmp/{latest}", "r") as f:
        latest_followers = json.load(f)
    with open(f"tmp/{second_latest}", "r") as f:
        second_latest_followers = json.load(f)
    diff_follower = []
    for id, name in latest_followers.items():
        if id not in second_latest_followers:
            user_state = UserDiffState(id, name, False, True)
            diff_follower.append(user_state)
    for id, name in second_latest_followers.items():
        if id not in latest_followers:
            user_state = UserDiffState(id, name, True, False)
            diff_follower.append(user_state)
    return diff_follower


def display_diff(diff_follower):
    if len(diff_follower) == 0:
        print("(No diff)")
        return
    for user_state in diff_follower:
        state = "unfollowed" if user_state.unfollowed else "followed"
        print(f"[{state}] {user_state.name} (@{user_state.id})")


def get_op():
    print("(0): update followers, (1): display diff")
    op = int(input())
    return op


if __name__ == "__main__":
    make_tmp_dir()
    follower_cnt = get_follower_cnt()
    print(f"{SC_USER_ID} has {follower_cnt} followers.")
    op = get_op()
    if op == 0:
        update_followers()
        latest, second_latest = get_latesest_two_timestamp()
        diff_follower = get_diff_follower(latest, second_latest)
        # remove second latest timestamp if no diff, save space
        if len(diff_follower) == 0:
            if second_latest is not None:
                os.remove(f"tmp/{second_latest}")
                print("No diff, removed second latest timestamp.")
    elif op == 1:
        diffs = get_set_two_timestamp()
        diffs.reverse()
        for latest, second_latest in diffs:
            print(f"- {latest}")
            diff_follower = get_diff_follower(latest, second_latest)
            display_diff(diff_follower)
