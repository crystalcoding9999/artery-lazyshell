import json


class BotConfig:
    def __init__(self):
        # Load data from JSON file if it exists
        try:
            with open("bot_config.json", "r") as json_file:
                bot_config_data = json.load(json_file)
                self.__dict__.update(bot_config_data)
        except FileNotFoundError:
            # Default values in case the JSON file doesn't exist
            self.bot_prefix = "+"
            self.default_cash = 0
            self.cash_name = "eggs"
            self.iron_cash_name = "silver eggs"
            self.gold_cash_name = "gold eggs"
            self.yolk_cash_name = "egg yolk"
            self.guild_id = 811510380152356864
            self.announce_channel_id = 834171208903294996
            self.mailbox_channel_id = 842522206201970719
            self.staff_role = 842686615092199444
            self.bot_channel = 1124677768240705596

            self.talk_blacklisted_channels = [
                842522206201970719, 842527822231896115, 1122532250915975208,
                842527903064522752, 842566675655950366, 846469567635390494,
                887403364575502398, 842522103315169320, 842516587978031115
            ]

            # Cooldowns
            self.boosts_duration = 7200  # 2 hours in minutes
            self.guild_join_cooldown = 604800  # 1 week in seconds
            self.harvest_cooldown = 20

            self.hunt_cooldown = 20
            self.hunt_chance = 50
            self.hunt_locations = ["in a bush", "near the river", "in a barn"]

            self.dupe_cooldown = 5
            self.dupe_chance = 50

            self.bargain_cooldown = 5
            self.bargain_chance = 80

            self.dig_cooldown = 20
            self.explore_cooldown = 20
            self.explore_locations = [
                "in an old factory", "in an old barn", "in the city", "at the park"
            ]

            # Farms
            self.level_1_farm_min = 0
            self.level_1_farm_max = 5
            self.level_1_silver_chance = 5
            self.level_1_silver_double = 0
            self.level_1_gold_chance = 0
            self.level_1_explore_min = -5
            self.level_1_explore_max = 5
            self.level_1_bargain_max = 100

            self.level_2_unlock_cost = 500
            self.level_2_farm_min = 1
            self.level_2_farm_max = 7
            self.level_2_silver_chance = 10
            self.level_2_silver_double = 15
            self.level_2_gold_chance = 0
            self.level_2_explore_min = -3
            self.level_2_explore_max = 8
            self.level_2_bargain_max = 150

            self.level_3_unlock_cost = 2000
            self.level_3_farm_min = 6
            self.level_3_farm_max = 12
            self.level_3_silver_chance = 15
            self.level_3_silver_double = 20
            self.level_3_gold_chance = 0
            self.level_3_explore_min = -1
            self.level_3_explore_max = 10
            self.level_3_bargain_max = 200

            self.level_4_unlock_cost = 5000
            self.level_4_farm_min = 9
            self.level_4_farm_max = 15
            self.level_4_silver_chance = 10
            self.level_3_silver_double = 30
            self.level_4_gold_chance = 1
            self.level_4_explore_min = 3
            self.level_4_explore_max = 12
            self.level_4_bargain_max = 250

            self.level_5_unlock_cost = 20000
            self.level_5_farm_min = 14
            self.level_5_farm_max = 20
            self.level_5_silver_chance = 25
            self.level_3_silver_double = 40
            self.level_5_gold_chance = 10
            self.level_5_explore_min = 5
            self.level_5_explore_max = 15
            self.level_5_bargain_max = 300

            # Object Data
            self.object_ids = {
                "binoculars": 5, "lucky drumstick": 6, "golden chicken": 4,
                "eggcellent statue": 7, "delicate shovel": 2, "egg topper": 1,
                "golden shovel": 8, "jackpot": 3, "custom role": 501, "custom channel": 502
            }

            self.object_descs = {
                "binoculars": "Find 1.5x as much eggs when hunting.",
                "lucky drumstick": "Higher chance to find silver eggs while chatting.",
                "golden chicken": "Increase your harvest by 1.5x.",
                "eggcellent statue": "A statue to signify your devotion to egg.",
                "delicate shovel": "Can be used to dig out lost eggs from the soil.",
                "egg topper": "Can be used to make an egg into egg yolk.",
                "golden shovel": "Does the work of a shovel but 1.5x better!",
                "jackpot": "Increase bargain and dupe profit by 1.5x",
                "custom role": "A custom role with a color and name of your choice.",
                "custom channel": "A custom channel that you can invite your friends to."
            }

            self.object_costs = {
                "farm_2": 500, "farm_3": 2000, "farm_4": 5000, "farm_5": 20000,
                "binoculars": 50, "lucky drumstick": 150, "golden chicken": 25,
                "eggcellent statue": 10, "delicate shovel": 100, "egg topper": 5,
                "golden shovel": 20, "jackpot": 20, "custom role": 100, "custom channel": 1000
            }

            self.object_egg_types = {
                "farm_2": "", "farm_3": "", "farm_4": "", "farm_5": "",
                "binoculars": "silver", "lucky drumstick": "silver", "golden chicken": "silver",
                "eggcellent statue": "gold", "delicate shovel": "", "egg topper": "",
                "golden shovel": "gold", "jackpot": "silver", "custom role": "gold", "custom channel": "gold"
            }

            self.object_types = {
                "binoculars": "boost", "lucky drumstick": "boost", "golden chicken": "boost",
                "eggcellent statue": "multi item", "delicate shovel": "item", "egg topper": "multi item",
                "golden shovel": "item", "jackpot": "boost", "custom role": "server item",
                "custom channel": "server item"
            }

            self.emojis = {
                "eggy": "<:eggy:1139539060516470976>",
                "silver eggy": "<:silvereggy:1139539079067873353>",
                "golden eggy": "<:goldeneggy:1139539073963397171>",
                "eggyolk": "<:eggyolk:1139539062651363338>",
                "egg topper": "<:topper:1139539081609629696>",
                "delicate shovel": "<:shovel:1139539078132543578>",
                "lucky drumstick": "<:drumstick:1139539088328900709>",
                "golden chicken": "<:goldenchicken:1139539071442620487>",
                "binoculars": "<:binoculars:1139539086114304020>",
                "farm": "<:farm:1139539068376584192>",
                "eggcellent statue": "<:eggystatue:1139539064912089148>",
                "golden shovel": "<:goldenshovel:1139539076538716220>",
                "jackpot": "<:jackpot:1139539083509637232>"
            }

            self.guilds = {
                "valkyrie": 1132357137050370188,
                "solstice": 1132357250422419517,
                "nyx": 1132357131455180943,
                "zephyr": 1132344076063223858
            }

            self.guildMasterRole = 863434428570796043

            self.save_to_json()

    def save_to_json(self):
        bot_config_data = vars(self)
        with open("bot_config.json", "w") as json_file:
            json.dump(bot_config_data, json_file, indent=4)

    def update_settings(self, settings_dict):
        # Update settings with values from the provided dictionary
        self.__dict__.update(settings_dict)
        # Save the updated settings to the JSON file
        self.save_to_json()

    @classmethod
    def load_from_json(cls):
        try:
            with open("bot_config.json", "r") as json_file:
                bot_config_data = json.load(json_file)
                bot_config_instance = cls()
                bot_config_instance.__dict__.update(bot_config_data)
                return bot_config_instance
        except FileNotFoundError:
            # If the JSON file doesn't exist, return a new instance with default values
            return cls()


settings = BotConfig()
