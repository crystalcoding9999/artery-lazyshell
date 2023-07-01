import json
import api


class User():
    def __init__(self, id: int, cash: 0, level: 1, icash: 0, gcash: 0, yolks: 0, inventory: list) -> None:
        self.id = id
        self.cash = cash
        self.farm_level = level
        self.ironcash = icash
        self.goldcash = gcash
        self.eggyolks = yolks
        self.inventory = inventory

    def to_string(self) -> str:
        data = {
            "id": self.id,
            "cash": self.cash,
            "farm_level": self.farm_level,
            "ironcash": self.ironcash,
            "goldcash": self.goldcash,
            "eggyolks": self.eggyolks,
            "inventory": self.inventory
        }
        return str(data)


def from_String(s: str) -> User:
    jdata = json.loads(s)

    if not isinstance(jdata, dict):
        jdata = {}  # Create an empty dictionary if the loaded data is not a dictionary

    id = check_or_replace(jdata, "id", 0)
    cash = check_or_replace(jdata, "cash", 0)
    farm_level = check_or_replace(jdata, "farm_level", 1)
    ironcash = check_or_replace(jdata, "ironcash", 0)
    goldcash = check_or_replace(jdata, "goldcash", 0)
    yolks = check_or_replace(jdata, "eggyolks", 0)
    inventory = check_or_replace(jdata, "inventory", [])

    return User(id, cash, farm_level, ironcash, goldcash, yolks, inventory)


def check_or_replace(jdata:dict, key, default):
    if key in jdata:
        return jdata[key]
    else:
        jdata[key] = default
        return jdata[key]
