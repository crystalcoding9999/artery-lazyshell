import sqlite3
import discord
from time import sleep as wait
from threading import Thread
import datetime

import settings


def get_db_value(guild: str, value_name: str):
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    names = [name[0] for name in cursor.execute("SELECT name FROM guilds")]

    gname = guild

    for name in names:
        if name == guild:
            gname = name
            break

    cursor.execute(f"SELECT {value_name} FROM guilds WHERE name = '{gname}'")
    bal = cursor.fetchone()
    try:
        val = bal[0]
    except:
        val = 0

    return val


def set_db_value(guild: str, value_name: str, value):
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT ? FROM guilds WHERE name = ?", (value_name, guild))
    cash = cursor.fetchone()

    try:
        cash = cash[0]
    except:
        cash = 0

    sql = f"UPDATE guilds SET {value_name} = ? WHERE name = ?"
    val = (value, guild)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


def create_embed(title: str | None, description: str = "") -> discord.Embed:
    return discord.Embed(
        title=title, description=description
    )


def setup_guilds():
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    try:
        vals_1 = ("valkyrie", 5000, 0, 0, "")
        cursor.execute("INSERT INTO guilds(name, cash, ironcash, goldcash, perms) VALUES " + str(vals_1))
        vals_2 = ("solstice", 5000, 0, 0, "")
        cursor.execute("INSERT INTO guilds(name, cash, ironcash, goldcash, perms) VALUES " + str(vals_2))
        vals_3 = ("nyx", 5000, 0, 0, "")
        cursor.execute("INSERT INTO guilds(name, cash, ironcash, goldcash, perms) VALUES " + str(vals_3))
        vals_4 = ("zephyr", 5000, 0, 0, "")
        cursor.execute("INSERT INTO guilds(name, cash, ironcash, goldcash, perms) VALUES " + str(vals_4))
    except sqlite3.IntegrityError:
        return

    db.commit()
    cursor.close()
    db.close()


def get_guild(ctx) -> str:
    valkyrie = discord.utils.find(lambda m: m.name == 'Valkyrie', ctx.guild.roles)
    solstice = discord.utils.find(lambda m: m.name == 'Solstice', ctx.guild.roles)
    nyx = discord.utils.find(lambda m: m.name == 'Nyx', ctx.guild.roles)
    zephyr = discord.utils.find(lambda m: m.name == 'Zephyr', ctx.guild.roles)

    if valkyrie in ctx.author.roles:
        return "valkyrie"
    elif solstice in ctx.author.roles:
        return "solstice"
    elif nyx in ctx.author.roles:
        return "nyx"
    elif zephyr in ctx.author.roles:
        return "zephyr"
    else:
        return "None"


def get_guild_cash(guild: str) -> int:
    return get_db_value(guild, "cash")


def get_guild_ironcash(guild: str) -> int:
    return get_db_value(guild, "ironcash")


def get_guild_goldcash(guild: str) -> int:
    return get_db_value(guild, "goldcash")


def has_perms(id, guild: str) -> bool:
    perms = get_db_value(guild, "perms").split("-")
    return str(id) in perms


def give_perms(id, guild: str):
    if has_perms(id, guild):
        return

    perms = get_db_value(guild, "perms")
    perms = perms + str(id) + "-"

    set_db_value(guild, "perms", perms)


def remove_perms(id, guild: str):
    if not has_perms(id, guild):
        return

    perms = get_db_value(guild, "perms").split("-")

    for perm in perms:
        if perm == str(id):
            perms.remove(perm)
            break

    newPerms = ""

    for perm in perms:
        newPerms = newPerms + str(perm) + "-"

    if len(perms) == 0:
        newPerms = ""

    set_db_value(guild, "perms", newPerms)


def get_guild_worth(guild: str) -> int:
    points = 0
    points += get_guild_cash(guild)
    points += (get_guild_ironcash(guild) * 5)
    points += (get_guild_goldcash(guild) * 10)

    return points


def get_guild_leaderboard() -> list:
    worths = {
        "valkyrie": get_guild_worth("valkyrie"),
        "solstice": get_guild_worth("solstice"),
        "nyx": get_guild_worth("nyx"),
        "zephyr": get_guild_worth("zephyr")
    }

    sortedWorths = sorted(worths.items(), key=lambda x: x[1], reverse=True)

    board = []

    for guild in sortedWorths:
        board.append(guild[0])

    return board


def is_guild_master(ctx) -> bool:
    role = ctx.guild.get_role(settings.guildMasterRole)
    return role in ctx.author.roles


def add_cash(guild: str, amount: int):
    set_db_value(guild, "cash", get_guild_cash(guild) + amount)


def add_ironcash(guild: str, amount: int):
    set_db_value(guild, "ironcash", get_guild_ironcash(guild) + amount)


def add_goldcash(guild: str, amount: int):
    set_db_value(guild, "goldcash", get_guild_goldcash(guild) + amount)


def remove_cash(guild: str, amount: int):
    set_db_value(guild, "cash", get_guild_cash(guild) - amount)


def remove_ironcash(guild: str, amount: int):
    set_db_value(guild, "ironcash", get_guild_ironcash(guild) - amount)


def remove_goldcash(guild: str, amount: int):
    set_db_value(guild, "goldcash", get_guild_goldcash(guild) - amount)


def get_cash(guild: str) -> int: return get_db_value(guild, "cash")


def get_iron_cash(guild: str) -> int: return get_db_value(guild, "ironcash")


def get_gold_cash(guild: str) -> int: return get_db_value(guild, "goldcash")


def get_guild_join_time(id: int) -> int:
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT timeuntilguildjoin FROM main WHERE id = {id}")
    bal = cursor.fetchone()
    try:
        cash = bal[0]
    except:
        cash = 0

    return cash


def set_guild_join_time(id: int, value: int):
    db = sqlite3.connect(f"main.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT ? FROM main WHERE id = ?", ("timeuntilguildjoin", id))
    cash = cursor.fetchone()

    try:
        cash = cash[0]
    except:
        cash = 0

    sql = f"UPDATE main SET timeuntilguildjoin = ? WHERE id = ?"
    val = (value, id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


kill_threads: bool = False


def start():
    """
        Creates and starts new thread that runs the boost loop.
    """
    t = Thread(target=gtime_loop)
    t.run()


def guild_join_time_left(id: int) -> str:
    left = get_guild_join_time(id)
    if left == 0:
        return "either 0 or less then a minute"
    t = str(datetime.timedelta(seconds=left))
    s = t.split(":")
    ss = s[0].split(" ")

    if len(ss) == 3:
        days = ss[0]
        hours = ss[2]
        mins = s[1]
        secs = s[2]

        l = ""

        if int(days) != 0:
            l = l + str(days) + " days "
        if int(hours) != 0:
            l = l + str(hours) + " hours "
        if int(mins) != 0:
            l = l + str(mins) + " minutes "

        return l + "left"
    else:
        hours = s[0]
        mins = s[1]
        secs = s[2]

        l = ""

        if int(hours) != 0:
            l = l + str(hours) + " hours "
        if int(mins) != 0:
            l = l + str(mins) + " minutes "

        if int(hours) == 0 and int(mins) == 0:
            if int(secs) != 0:
                l = l + str(secs) + " seconds "

        return l + "left"


def gtime_loop():
    print("started guild join time loop")

    while not kill_threads:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT id FROM boosts")

        ids = [job[0] for job in cursor.execute("SELECT id FROM main")]

        for id in ids:
            if get_guild_join_time(id) != 0:
                current = get_guild_join_time(id)
                if current is None:
                    set_guild_join_time(id, 0)
                    current = 1
                new = current - 1
                set_guild_join_time(id, new)

        # wait(60)

        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
                  54, 55, 56, 57, 58, 59, 60]:
            if not kill_threads:
                wait(1)
            else:
                break

    print("ended guild join time loop")


def secToMin(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return hour, min, sec


def hoursToSec(Hours):
    return Hours * 60 * 60
