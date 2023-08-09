import dashboard
from settings import settings, BotConfig
import os

if os.path.exists('./bot_config.json'):
    os.remove('./bot_config.json')
    settings = BotConfig()

dashboard.run(True)
