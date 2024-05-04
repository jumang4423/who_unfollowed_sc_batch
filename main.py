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

from src.util import get_id_by_url, make_tmp_dir
from src.driver import get_driver

SC_USER_ID = ""


def get_follower_cnt(uid):
    while True:
        try:
            url = f"https://soundcloud.com/{uid}"
            r = requests.get(url)
            r_text = r.text
            el = "followers_count"
            follower_cnt = re.search(f'"{el}":(\d+)', r_text).group(1)
            return int(follower_cnt)
        except:
            print("???")
            time.sleep(10)


def get_followers_by_fetched(driver):
    el = "userBadgeListItem__heading"
    followers_obj = driver.find_elements(By.CLASS_NAME, el)
    return followers_obj


def get_followers(driver):
    url = f"https://soundcloud.com/{SC_USER_ID}/followers"
    driver.get(url)

    # start scrolling
    all_followers = get_follower_cnt(SC_USER_ID)
    print(f"{SC_USER_ID} has {all_followers} followers.")
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
    followers = []
    for follower_obj in followers_obj:
        follower_url = follower_obj.get_attribute("href")
        follower_id = get_id_by_url(follower_url)
        followers.append(follower_id)
    return followers


def save_followers(followers):
    cur_unix = int(time.time())
    with open(f"tmp/{SC_USER_ID}_{cur_unix}.json", "w") as f:
        f.write(json.dumps(followers, ensure_ascii=False))


def update_followers():
    driver = get_driver()
    followers = get_followers(driver)
    save_followers(followers)


def get_sorted_timestamps(user_id):
    files = os.listdir("tmp")
    files = [f for f in files if f.startswith(user_id)]
    files = sorted(files, reverse=True)
    return files


def get_set_two_timestamp() -> list[tuple]:
    """
    get user latest two timestamp json
    """
    files = get_sorted_timestamps(SC_USER_ID)
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
    def __init__(self, id, unfollowed, newly_followed):
        self.id = id
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
    for id in latest_followers:
        if id not in second_latest_followers:
            user_state = UserDiffState(id, False, True)
            diff_follower.append(user_state)
    for id in second_latest_followers:
        if id not in latest_followers:
            user_state = UserDiffState(id, True, False)
            diff_follower.append(user_state)
    return diff_follower


def display_diff(diff_follower):
    if len(diff_follower) == 0:
        print("(No diff)")
        return
    for user_state in diff_follower:
        state = "unfollowed" if user_state.unfollowed else "followed"
        print(f"[{state}] (@{user_state.id})")


def get_history_cnt():
    files = os.listdir("tmp")
    files = [f for f in files if f.startswith(SC_USER_ID)]
    return len(files)


def ask_op():
    print(
        "(0)update_cur_followers, (1)display_diff_history (2)diff_other_artist (3)filter_than_1000_followers_artist: ",
        end="",
    )
    op = int(input())
    return op


def ask_artist():
    print("Enter comparison artist id: ", end="")
    artist_id = input()
    return artist_id


def get_username_by_argument():
    print("Enter username: ", end="")
    username = input()
    return username


def save_comp(u1, u2, mutual, diff):
    with open(f"tmp/mut_{u1}_{u2}.json", "w") as f:
        f.write(json.dumps(list(mutual), ensure_ascii=False))
    with open(f"tmp/diff_{u1}_{u2}.json", "w") as f:
        f.write(json.dumps(list(diff), ensure_ascii=False))


def ask_filename():
    print("Enter filename from tmp (hoge.json): ", end="")
    filename = input()
    # check availability
    if not os.path.exists(f"tmp/{filename}"):
        print("File not found")
        exit(1)
    return filename


def two_diff(com_artist_id):
    me_latest_timestamp = get_sorted_timestamps(SC_USER_ID)
    if len(me_latest_timestamp) == 0:
        print("No history of me")
        exit(1)
    me_latest_timestamp = me_latest_timestamp[0]
    com_latest_timestamp = get_sorted_timestamps(com_artist_id)
    if len(com_latest_timestamp) == 0:
        print("No history of comparison artist")
        exit(1)
    com_latest_timestamp = com_latest_timestamp[0]
    me_followers = []
    com_followers = []
    with open(f"tmp/{me_latest_timestamp}", "r") as f:
        me_followers = json.load(f)
    with open(f"tmp/{com_latest_timestamp}", "r") as f:
        com_followers = json.load(f)
    me_followers = set(me_followers)
    com_followers = set(com_followers)
    mut = []
    diff = []
    for f in com_followers:
        if f in me_followers:
            mut.append(f)
        else:
            diff.append(f)
    return mut, diff


def get_rank_filtered(followers):
    THREADHOLD = 1000
    filtered = []
    for follower in tqdm(followers, desc="Filtering..."):
        follower_cnt = get_follower_cnt(follower)
        if follower_cnt > THREADHOLD:
            filtered.append(follower)
    return filtered


if __name__ == "__main__":
    make_tmp_dir()
    op = ask_op()
    if op == 0:
        SC_USER_ID = get_username_by_argument()
        update_followers()
        latest, second_latest = get_latesest_two_timestamp()
        diff_follower = get_diff_follower(latest, second_latest)
        # remove second latest timestamp if no diff, save space
        if len(diff_follower) == 0:
            if second_latest is not None:
                os.remove(f"tmp/{second_latest}")
                print("No diff, removed second latest timestamp.")
    elif op == 1:
        SC_USER_ID = get_username_by_argument()
        diffs = get_set_two_timestamp()
        diffs.reverse()
        for latest, second_latest in diffs:
            print(f"- {latest}")
            diff_follower = get_diff_follower(latest, second_latest)
            display_diff(diff_follower)
    elif op == 2:
        SC_USER_ID = get_username_by_argument()
        com_artist_id = ask_artist()
        mut, diff = two_diff(com_artist_id)
        print(f"found {len(mut)} mutual")
        print(f"found {len(diff)} diff")
        print("saving...")
        save_comp(SC_USER_ID, com_artist_id, mut, diff)
    elif op == 3:
        filename = ask_filename()
        with open(f"tmp/{filename}", "r") as f:
            followers = json.load(f)
        ranked = get_rank_filtered(followers)
        print(f"filtered {len(ranked)}")
        with open(f"tmp/ranked_{filename}", "w") as f:
            f.write(json.dumps(ranked, ensure_ascii=False))

    else:
        print("huh?")
        exit(1)
