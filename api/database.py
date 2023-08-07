import sqlite3
from typing import Dict, Any

import settings
from api.boostManager import get_active_boosts


def get_db_value(filename, id: int, value_name: str):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT {value_name} FROM {filename} WHERE id = {id}")
    bal = cursor.fetchone()
    try:
        cash = bal[0]
    except:
        cash = 0

    return cash


def set_db_value(filename: str, id: int, value_name: str, value):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT {value_name} FROM {filename} WHERE id = {id}")
    cash = cursor.fetchone()

    try:
        cash = cash[0]
    except:
        cash = 0

    sql = f"UPDATE {filename} SET {value_name} = ? WHERE id = ?"
    val = (value, id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


def get_table_collums(filename: str) -> list:
    db = sqlite3.connect("main.sqlite")
    cursor = db.execute(f'SELECT * FROM {filename}')

    names = list(map(lambda x: x[0], cursor.description))

    names.remove("id")

    cursor.close()
    db.close()

    return names


def has_boost_active(id: int, boost: str) -> bool:
    return boost in get_active_boosts(id)


class Database:
    def __init__(self):
        db = sqlite3.connect(f"main.sqlite")
        cursor = db.cursor()
        self.file_name = "main"
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS main (
            id INTEGER, cash INTEGER, farm_level INTEGER, ironcash INTEGER, goldcash INTEGER, eggyolks INTEGER, timeuntilguildjoin INTEGER
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory ( 
            id INTEGER, eggcellent_statue INTEGER, delicate_shovel INTEGER, 
            egg_topper INTEGER, golden_shovel INTEGER, custom_role INTEGER, 
            custom_channel INTEGER, dev_crown INTEGER 
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS boosts (
            id INTEGER, binoculars INTEGER, lucky_drumstick INTEGER, golden_chicken INTEGER, jackpot INTEGER
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS guilds (
            name STRING, cash INTEGER, ironcash INTEGER, goldcash INTEGER, perms STRING, UNIQUE(name)
        )''')

        print("created database")

    def wipe_database(self, confirmCode: int):
        if confirmCode != 1058945:
            return
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"DELETE FROM main")
        cursor.execute(f"DELETE FROM inventory")
        cursor.execute(f"DELETE FROM boosts")
        cursor.execute(f"DELETE FROM guilds")

        self.db.commit()
        cursor.close()

        print("Database wiped.")

    def add_user(self, id: int):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM {self.file_name} WHERE id = {id}")
        result = cursor.fetchone()
        cursor.execute(f"SELECT id FROM inventory WHERE id = {id}")
        result2 = cursor.fetchone()
        cursor.execute(f"SELECT id FROM boosts WHERE id = {id}")
        result3 = cursor.fetchone()
        if result is None:
            sql_1 = (
                "INSERT INTO main(id, cash, farm_level, ironcash, goldcash, eggyolks, timeuntilguildjoin) VALUES (?, ?, ?, ?, ?, ?, ?)")
            val_1 = (id, settings.default_cash, 1, 0, 0, 0, 0)
            cursor.execute(sql_1, val_1)
        if result2 is None:
            sql_2 = ("INSERT INTO inventory(id, binoculars, lucky_drumstick, golden_chicken, eggcellent_statue, "
                     "delicate_shovel, egg_topper, golden_shovel, jackpot, "
                     "custom_role, custom_channel, dev_crown ) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val_2 = (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql_2, val_2)
        if result3 is None:
            sql_3 = (
                "INSERT INTO boosts(id, binoculars, lucky_drumstick, golden_chicken, jackpot) VALUES (?, ?, ?, ?, ?)")
            val_3 = (id, 0, 0, 0, 0)
            cursor.execute(sql_3, val_3)

        db.commit()
        cursor.close()
        db.close()

    def get_cash(self, id: int):
        self.add_user(id)

        return get_db_value("main", id, "cash")

    def give_cash(self, id: int, amount: int):
        self.add_user(id)

        old = get_db_value("main", id, "cash")
        new = old + amount

        set_db_value("main", id, "cash", new)

        print(f"gave {amount} eggs to {id}")

    def get_iron_cash(self, id: int):
        self.add_user(id)

        return get_db_value("main", id, "ironcash")

    def give_iron_cash(self, id: int, amount: int):
        self.add_user(id)

        old = get_db_value("main", id, "ironcash")
        new = old + amount

        set_db_value("main", id, "ironcash", new)

        print(f"gave {amount} iron eggs to {id}")

    def get_gold_cash(self, id: int):
        self.add_user(id)

        return get_db_value("main", id, "goldcash")

    def give_gold_cash(self, id: int, amount: int):
        self.add_user(id)

        old = get_db_value("main", id, "goldcash")
        new = old + amount

        set_db_value("main", id, "goldcash", new)

        print(f"gave {amount} gold eggs to {id}")

    def get_eggyolks(self, id: int):
        self.add_user(id)

        return get_db_value("main", id, "eggyolks")

    def give_eggyolks(self, id: int, amount: int):
        self.add_user(id)

        old = get_db_value("main", id, "eggyolks")
        new = old + amount

        set_db_value("main", id, "eggyolks", new)

        print(f"gave {amount} eggyolks to {id}")

    def get_farm_level(self, id: int):
        self.add_user(id)

        return get_db_value("main", id, "farm_level")

    def give_farm_level(self, id: int, amount: int):
        self.add_user(id)

        old = get_db_value("main", id, "farm_level")
        new = old + amount

        set_db_value("main", id, "farm_level", new)

        print(f"gave {amount} farm levels to {id}")

    def has_inventory_item(self, id: int, item: str) -> bool:
        self.add_user(id)

        item = item.replace(' ', '_')

        return get_db_value("inventory", id, item) >= 1

    def get_inventory_amount(self, id: int, item: str) -> int:
        self.add_user(id)

        item = item.replace(' ', '_')

        return get_db_value("inventory", id, item)

    def give_inventory_item(self, id: int, item: str, amount: int):
        self.add_user(id)

        item = item.replace(' ', '_')

        old = get_db_value("inventory", id, item)
        new = old + amount

        set_db_value("inventory", id, item, new)

        print(f"gave {amount} {item}s to {id}")

    def remove_inventory_item(self, id: int, item: str, amount: int):
        self.add_user(id)

        item = item.replace(' ', '_')

        old = get_db_value("inventory", id, item)
        new = old - amount

        set_db_value("inventory", id, item, new)

        print(f"took {amount} {item}s from {id}")

    def is_inventory_empty(self, id: int) -> bool:
        self.add_user(id)

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(
            f"SELECT SUM(binoculars) + SUM(lucky_drumstick) + SUM(golden_chicken) + SUM(eggcellent_statue) + SUM(delicate_shovel) + SUM(egg_topper) + SUM(golden_shovel) + SUM(jackpot) + SUM(custom_role) + SUM(custom_channel) + SUM(dev_crown) AS total_items FROM inventory WHERE id = {id}")

        total_items = cursor.fetchone()[0]
        total_items = total_items if total_items else 0

        return total_items == 0

    def get_inventory_items(self, id: int) -> dict[Any, int]:
        items = {}

        for item in get_table_collums("inventory"):
            if self.has_inventory_item(id, item):
                items[item] = self.get_inventory_amount(id, item)

        return items

    def activate_boost(self, id: int, boost: str):
        self.add_user(id)

        boost = boost.replace(' ', '_')

        old = get_db_value("boosts", id, boost)
        new = old + settings.boosts_duration

        set_db_value("boosts", id, boost, new)

        if self.has_inventory_item(id, boost):
            self.remove_inventory_item(id, boost, 1)

        print(f"{id} activated the {boost} boost")
