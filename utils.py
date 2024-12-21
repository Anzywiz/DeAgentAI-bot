from eth_account import Account
from eth_account.messages import encode_defunct
import requests
from headers import headers, discord_gm_payload
import logging
from time import sleep
from datetime import datetime, timezone
import time
import random
import json
from dotenv import load_dotenv
import os

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

base_dir = os.getcwd()
load_dotenv()


with open("config.json", "r") as file:
    data = json.load(file)
    max_threads = data.get("maximum_number_of_threads")
    proxies = data.get("proxies")

if not proxies:
    logging.error(f"Proxies not found!")


def get_key_auth_pairs(file_path="config.json"):
    try:
        # Load data from the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"The file {file_path} is not a valid JSON file.")

    private_keys = data.get("private_keys", [])
    discord_auth_tokens = data.get("discord_auth_tokens", [])

    # Pair private keys with discord auth tokens
    result = []
    for i, private_key in enumerate(private_keys):
        discord_auth = discord_auth_tokens[i] if i < len(discord_auth_tokens) else None
        result.append((private_key, discord_auth))

    return result


class TimeoutSession(requests.Session):
    DEFAULT_TIMEOUT = 10  # Set your default timeout value here

    """
    create a timeout for requests as it doesnt have one in requests session
    """
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        super().__init__()
        self.timeout = timeout

    def request(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        return super().request(*args, **kwargs)


def get_session(use_proxies=True):
    with TimeoutSession() as session:
        if use_proxies is True:
            if proxies:  # is not None or ""
                PROXIES = {
                    'http': proxies,
                    'https': proxies
                }
                session.proxies = PROXIES

        session.headers = headers
        return session


def get_ip(session):  # TODO: Remove, longer needed
    """"open page and get ip"""

    url = 'https://worldtimeapi.org/api/ip'

    response = session.get(url)
    content = response.json()
    ip = content['client_ip']
    return ip


# sign_message
def sign_message(private_key, message):
    """
    Signs message using EVMs
    """
    message_encoded = encode_defunct(text=message)

    # Sign the message
    signed_message = Account.sign_message(message_encoded, private_key)
    return signed_message.signature.hex()


def login_user(session, private_key, platform="deagent_ai"):
    # Create an account from the private key
    account = Account.from_key(private_key)
    address = str(account.address)

    # Message to sign
    timestamp = int(time.time() * 1000)

    if platform == 'alpha_x':
        da_addr = address

        message = f"Welcome to AlphaX@{timestamp}"
        signature = sign_message(private_key, message)
        payload = {
            "wallet_address": address,
            "sign_message": message,
            "signature": f"{signature}",
            "referral_code": "",
            "chain": "Movement EVM Testnet",
            "da_addr": da_addr
        }

        url = "https://alpha-x.ai/alphax/api/common/login/"

    elif platform == "deagent_ai":
        message = f"Welcome to Deagent.ai@{timestamp}"
        signature = sign_message(private_key, message)
        payload = {
            "platform": "original",
            "signature": signature,
            "address": address,
            "invitationCode": "",
            "message": message,
            "chain": "ethereum"
        }

        url = 'https://deagent.ai/api/v1/wallet_login'

    response = session.post(url, json=payload)
    if response.status_code == 200:
        login_data = response.json()['data']
        return login_data
    else:
        raise Exception(f"Error {response.status_code}: {response.json()}")


def discord_gm(session, auth: str):
    headers = {"Authorization": auth}

    url = 'https://discord.com/api/v9/interactions'

    payload = discord_gm_payload

    with session as s:
        s.headers = headers
        r = s.post(url, json=payload)

        if r.status_code == 200 or 204:
            logging.info(f"'/Gm' sent successfully")
        else:
            raise Exception(f"Error {r.status_code}: {r.text}")


def get_twitter_task(session, uid):
    url = f"https://deagent.ai/api/v1/task/twitter_task?user_id={uid}"

    r = session.get(url)
    if r.status_code == 200:
        message = r.json()["message"]
        # logging.info(f"User {uid}: Launching Twitter Task: {message}")
    else:
        logging.error(f"User {uid}: Error {r.status_code} {r.json()}")


def verify_tasks(session, uid, task_id, task_on=False):
    if task_id == 11:
        task = 'Daily Twitter Task'
    elif task_id == 10:
        task = 'Daily discord Task'
    else:
        task = 'On task'  # Unknown tasks

    if task_on:
        url = 'https://deagent.ai/api/v1/task_on/task_on_verify_user'
    else:
        url = 'https://deagent.ai/api/v1/task/verify_user'

    payload = {"data": [{"task_id": task_id, "chain": "ethereum", "user_id": uid}]}

    resp = session.post(url, json=payload)
    if resp.status_code == 200:
        task_stage = resp.json()["data"][0]["type"]
        # logging.info(f"User {uid}: {task} {task_stage}")
    else:
        logging.error(f"User {uid}: Error {resp.status_code} {resp.json()}")


def collect_points(session, uid, task_id, task_type="daily", platform=None):
    """
    collects the reward points
    :param session:
    :param uid:
    :param task_id:
    :param task_type:
    :param platform:
    :return: the reward message response
    """
    url = 'https://deagent.ai/api/v1/task/points_collection'
    payload = {
        "user_id": f"{uid}",
        "task_id": task_id,
        "task_type": task_type,
        "chain": "ethereum"
    }
    if task_type == "newbie":
        url = 'https://deagent.ai/api/v1/task_on/task_on_points_collection'
    elif platform == "alpha_x":
        url = "https://deagent.ai/api/v1/alpha/points_collection"

    response = session.post(url, json=payload)
    sleep(5)  # end point is rate limited
    if response.status_code == 200:
        message = response.json()['message']
        return message
        # logging.info(f"User {uid}: {message}")
    else:
        logging.error(f"Error {response.status_code}: {response.json()}")


def daily_twitter_task(session, uid):
    twitter_daily_task_id = 11
    # grab twitter url to repost. No need to repost
    get_twitter_task(session, uid)

    verify_tasks(session, uid, twitter_daily_task_id)

    json_response = collect_points(session, uid, twitter_daily_task_id)
    if json_response == "User already completed the task":
        logging.error(f"User {uid}: Twitter Task failed. Connect a valid Twitter to DA")
    else:
        logging.info(f"User {uid}: Performing Twitter Daily Task: `{json_response}`")

    verify_tasks(session, uid, twitter_daily_task_id)


def daily_discord_task(session, uid):
    # discord_gm(session, discord_auth) # sending `gm` no longer required
    task_id = 10
    verify_tasks(session, uid, task_id)
    json_response = collect_points(session, uid, task_id)
    if json_response == "User already completed the task":
        logging.error(f"User {uid}: Discord Task failed, Connect a valid discord account to DA")
    else:
        logging.info(f"User {uid}: Performing Discord Daily Task: `{json_response}`")

    verify_tasks(session, uid, task_id)


def verify_alpha_x(session, uid):
    url = f"https://deagent.ai/api/v1/alpha/verify_user?task_id=34&chain=ethereum&user_id={uid}"
    r = session.get(url)
    if r.status_code == 200:
        return r.json()


def daily_alpha_x(session, uid):
    task_id = 34
    json_response = verify_alpha_x(session, uid)
    json_response = collect_points(session, uid, task_id, platform='alpha_x')
    logging.info(f"User {uid}: Alpha X Daily Task: `{json_response}`")


def perform_daily_task(private_key, discord_auth):
    session = get_session(use_proxies=True)
    headers_ = headers
    session.headers = headers_

    login_data = login_user(session, private_key)

    # update session headers with `Auth headers
    access_token = login_data["access_token"]
    headers_["Authorization"] = access_token
    session.headers = headers_

    uid = login_data["id"]

    # check which daily tasks have been performed
    log_list = get_log(session, uid)["data"][0]["log_list"]
    midnight_timestamp = get_utc_midnight_timestamp()
    performed_daily_logs = [int(log["task_id"]) for log in log_list if
                            log["task_type"] == "daily" and log["created_at"] > midnight_timestamp]

    daily_task_ids = [10, 11, 34]
    remaining_daily_task_ids = list(set(daily_task_ids) - set(performed_daily_logs))

    for task_id in remaining_daily_task_ids:
        if task_id == 10:
            # grab score before
            point_before, logged_points_b4 = get_user_log_points(session, uid)

            daily_discord_task(session, uid)

            point_after, logged_points = get_user_log_points(session, uid)
            points = point_after - point_before
            if points > 0:
                logging.info(f"User {uid}:Performed daily Discord Task. Point claimed {points}")
            else:
                logging.error(f"User {uid}: Discord Task NOT performed")

        elif task_id == 11:
            # grab score before
            point_before, logged_points_b4 = get_user_log_points(session, uid)

            daily_twitter_task(session, uid)

            point_after, logged_points = get_user_log_points(session, uid)

            points = point_after - point_before

            if points > 0:
                logging.info(f"User {uid}:Performed daily Twitter Task. Point claimed {points}")
            else:
                logging.error(f"User {uid}: Twitter Task NOT performed")
        elif task_id == 34:
            # grab score before
            point_before, logged_points_b4 = get_user_log_points(session, uid)

            daily_alpha_x(session, uid)

            point_after, logged_points = get_user_log_points(session, uid)
            logging.info(f"User {uid}:Performed Alpha X. Point claimed {point_after - point_before}")

    rank = get_rank(session, uid)
    point_final, logged_points_final = get_user_log_points(session, uid)
    logging.info(
        f"User {uid}: Daily Task Complete. Displayed: {point_final} DA. Logged: {logged_points_final}. Rank {rank}")


def get_log(session, uid: int):
    url = f'https://deagent.ai/api/v1/task/user_logs?user_id={uid}&chain=ethereum'
    r = session.get(url)
    if r.status_code == 200:
        return r.json()


def get_user_log_points(session, uid):

    log_response = get_log(session, uid)

    data = log_response["data"]
    displayed_points = data[0]['points']

    log_list = data[0]["log_list"]
    logged_points = sum([i['points'] for i in log_list])

    return displayed_points, logged_points


def task_on(session, uid, task_id, task_name):
    url = f"https://deagent.ai/api/v1/task_on/task_on?user_id={uid}&task_id={task_id}&task_name=Meson&chain=ethereum"

    r = session.get(url)
    if r.status_code != 200:
        raise Exception(f"{r.text}")

    response = collect_points(session, uid, task_id, task_type="newbie")
    logging.info(f"User {uid}: Performing Taskon Task `{task_name}`, {response.upper()}")


def get_rank(session, uid):
    url = f"https://deagent.ai/api/v1/task/get_ranking?user_id={uid}&my_rank=1"
    r = session.get(url)

    rank = r.json()['data'][0]['rank']
    return rank


def get_utc_midnight_timestamp():
    # Get the current UTC date
    now = datetime.now(timezone.utc)

    # Calculate midnight for the current UTC day
    midnight = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)

    # Return the timestamp
    return int(midnight.timestamp())


def discord_send_delete(auth, channel, msg, timeout=5):
    url = f"https://discord.com/api/v9/channels/{channel}/messages"
    param = {
        "mobile_network_type": "unknown",
        "content": str(msg),
        "nonce": int(f"13{int(time.time() * 1000)}{random.randint(100, 999)}"),
        "tts": False,
        "flags": 0
    }
    session = get_session(use_proxies=True)
    with session as session:
        headers_ = headers
        headers_["Authorization"] = auth
        session.headers = headers
        r = session.post(url, json=param)
        if r.status_code == 200:
            # little timeout
            time.sleep(timeout)
            msg_id = r.json()["id"]
            author = r.json()["author"]["username"]
            url = f"https://discord.com/api/v9/channels/{channel}/messages/{msg_id}"
            r = session.delete(url)
            if r.status_code == 200 or r.status_code == 204:
                logging.info(f"{author}: sent `{msg}` and deleted successfully")
            else:
                logging.info(f"Error {r.status_code} deleting message {r.json()}")
        else:
            logging.info(f"Error {r.status_code} Sending and deleting message `{msg}`\n{r.json()}")
