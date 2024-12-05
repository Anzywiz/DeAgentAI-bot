import random
import uuid


def get_random_user_agent():
    base_user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Firefox/{firefox_version}",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{firefox_version}) Gecko/20100101 Firefox/{firefox_version}",
    ]

    webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 50)}"
    chrome_version = f"{random.randint(80, 100)}.0.{random.randint(4000, 5000)}.{random.randint(100, 150)}"
    firefox_version = f"{random.randint(80, 100)}.0"

    user_agent = random.choice(base_user_agents).format(
        webkit_version=webkit_version,
        chrome_version=chrome_version,
        firefox_version=firefox_version
    )

    return user_agent


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": get_random_user_agent()
}

# discord payload

nonce = str(uuid.uuid4().int)[:19]
session_id = uuid.uuid4().hex

discord_gm_payload = {
    "type": 2,
    "application_id": "1267793577149468694",
    "guild_id": "1194935697665167392",
    "channel_id": "1217388924322709545",
    "session_id": f"{session_id}",
    "data": {
        "version": "1267818679920230435",
        "id": "1267818679920230434",
        "name": "gm",
        "type": 1,
        "options": [],
        "application_command": {
            "id": "1267818679920230434",
            "type": 1,
            "application_id": "1267793577149468694",
            "version": "1267818679920230435",
            "name": "gm",
            "description": "Sign in for today",
            "dm_permission": True,
            "contexts": [0, 1, 2],
            "integration_types": [0],
            "permissions": [
                {"type": 3, "id": "1281939000227139624", "permission": False},
                {"type": 3, "id": "1276537842260119623", "permission": False}
            ],
            "global_popularity_rank": 1,
            "options": [],
            "description_localized": "Sign in for today",
            "name_localized": "gm"
        },
        "attachments": []
    },
    "nonce": f"{nonce}",
    "analytics_location": "slash_ui"
}
