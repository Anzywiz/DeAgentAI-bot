from utils import perform_daily_task, get_key_auth_pairs, max_threads, logging
import random
from concurrent.futures import ThreadPoolExecutor


private_key_discord_auths = get_key_auth_pairs()
random.shuffle(private_key_discord_auths)

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = [executor.submit(perform_daily_task, private_key, discord_auth) for private_key, discord_auth in private_key_discord_auths]
    for future in futures:
        try:
            future.result()
        except Exception as e:
            logging.error(e)
            continue
