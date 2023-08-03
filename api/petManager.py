import sqlite3
import discord


pet_default_max_settings = {
    "health": {
        "potato": 100
    },
    "energy": {
        "potato": 150
    },
    "hunger": {
        "potato": 100
    },
    "evolutions": {
        "potato": 3
    },
    "type": {
        "potato": "potato"
    },
    "strength": {
        "potato": 150
    },
    "fetch": {
        "potato": 10
    },
    "effect": {
        "potato": "None"
    }
}


def get_db_value(filename, id: int, value_name: str):
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT {value_name} FROM {filename} WHERE id = {id}")
    bal = cursor.fetchone()
    try:
        cash = bal[0]
    except:
        cash = 0

    return cash


def set_db_value(filename: str, id: int, value_name: str, value):
    db = sqlite3.connect(f"main.sqlite")
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


def create_embed(title: str | None, description: str = "") -> discord.Embed:
    return discord.Embed(
        title=title, description=description
    )


def get_default_pet_profile(petID: str) -> discord.Embed:
    health = pet_default_max_settings["health"][petID]
    energy = pet_default_max_settings["energy"][petID]
    hunger = pet_default_max_settings["hunger"][petID]
    evolutions = pet_default_max_settings["evolutions"][petID]
    type = pet_default_max_settings["type"][petID]
    strength = pet_default_max_settings["strength"][petID]
    fetch = pet_default_max_settings["fetch"][petID]
    effect = pet_default_max_settings["effect"][petID]

    emb = create_embed(petID + "s profile")


