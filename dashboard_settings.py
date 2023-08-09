import requests

REDIRECT_URI = "http://localhost:2710/oauth/callback"
OAUTH_URL = "https://discord.com/api/oauth2/authorize?client_id=1121487989403558049&redirect_uri=http%3A%2F%2Flocalhost%3A2710%2Foauth%2Fcallback&response_type=code&scope=identify%20guilds"
CLIENT_ID = 1121487989403558049
CLIENT_SECRET = "9N9jmnp8sp8ECz2srlk2qsZUFKgvT3oT"

settings_type_names = ['nonedit', 'server', 'boosts', 'guilds', 'harvest command', 'hunt command', 'dupe command',
                       'bargain command', 'dig command', 'explore command', 'level 1 farm', 'level 2 farm',
                       "level 3 farm", "level 4 farm", "level 5 farm", 'store']

subcategory_mapping = {

}

settings_types = {
    'bot_prefix': 'nonedit',
    'default_cash': 'nonedit',
    'cash_name': 'server',
    'iron_cash_name': 'server',
    'gold_cash_name': 'server',
    'yolk_cash_name': 'server',
    'guild_id': 'server',
    'announce_channel_id': 'server',
    'mailbox_channel_id': 'server',
    'staff_role': 'server',
    'bot_channel': 'server',
    'talk_blacklisted_channels': 'server',
    'boosts_duration': 'boosts',
    'guild_join_cooldown': 'guilds',
    'harvest_cooldown': 'harvest command',
    'hunt_cooldown': 'hunt command',
    'hunt_chance': 'hunt command',
    'hunt_locations': 'hunt command',
    'dupe_cooldown': 'dupe command',
    'dupe_chance': 'dupe command',
    'bargain_cooldown': 'bargain command',
    'bargain_chance': 'bargain command',
    'dig_cooldown': 'dig command',
    'explore_cooldown': 'explore command',
    'explore_locations': 'explore command',
    'level_1_farm_min': "level 1 farm",
    'level_1_farm_max': "level 1 farm",
    'level_1_explore_min': "level 1 farm",
    'level_1_explore_max': "level 1 farm",
    'level_1_bargain_max': "level 1 farm",
    'level_2_unlock_cost': "level 2 farm",
    'level_2_farm_min': "level 2 farm",
    'level_2_farm_max': "level 2 farm",
    'level_2_explore_min': "level 2 farm",
    'level_2_explore_max': "level 2 farm",
    'level_2_bargain_max': "level 2 farm",
    'level_3_unlock_cost': "level 3 farm",
    'level_3_farm_min': "level 3 farm",
    'level_3_farm_max': "level 3 farm",
    'level_3_explore_min': "level 3 farm",
    'level_3_explore_max': "level 3 farm",
    'level_3_bargain_max': "level 3 farm",
    'level_4_unlock_cost': "level 4 farm",
    'level_4_farm_min': "level 4 farm",
    'level_4_farm_max': "level 4 farm",
    'level_4_silver_chance': "level 4 farm",
    'level_4_gold_chance': "level 4 farm",
    'level_4_explore_min': "level 4 farm",
    'level_4_explore_max': "level 4 farm",
    'level_4_bargain_max': "level 4 farm",
    'level_5_unlock_cost': "level 5 farm",
    'level_5_farm_min': "level 5 farm",
    'level_5_farm_max': "level 5 farm",
    'level_5_silver_chance': "level 5 farm",
    'level_5_gold_chance': "level 5 farm",
    'level_5_explore_min': "level 5 farm",
    'level_5_explore_max': "level 5 farm",
    'level_5_bargain_max': "level 5 farm",
    'object_ids': 'store',
    'object_descs': 'store',
    'object_costs': 'store',
    'object_egg_types': 'store',
    'object_types': 'store',
    'emojis': 'server',
    'guilds': 'guilds',
    'guildMasterRole': 'guilds'
}


def get_token(code: str):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resp = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()['access_token']


def get_user_guilds(token: str):
    resp = requests.get("https://discord.com/api/v6/users/@me/guilds", headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return resp.json()


def get_bot_guilds(token: str):
    resp = requests.get("https://discord.com/api/v6/users/@me/guilds", headers={"Authorization": f"Bot {token}"})
    resp.raise_for_status()
    return resp.json()


def get_mutual_guilds(user_guilds: list, bot_guilds: list):
    return [guild for guild in user_guilds if guild['id'] in map(lambda i: i['id'], bot_guilds)
            and (guild['permissions'] & 0x0000000000020000) == 0x0000000000020000]


def get_guild_data(guild_id: int, token: str):
    resp = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}", headers={"Authorization": f"Bot {token}"})
    try:
        resp.raise_for_status()
        return resp.json()
    except:
        return None
