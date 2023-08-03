import datetime
import sqlite3
from threading import Thread
from time import sleep as wait

kill_threads = False

boosts = ["binoculars", "lucky_drumstick", "golden_chicken", "jackpot"]


def start():
    """
        Creates and starts new thread that runs the boost loop.
    """
    t = Thread(target=boost_loop)
    t.run()


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


def set_db_value(filename, id: int, value_name: str, value):
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


def get_active_boosts(id: int) -> list:
    global boosts
    active_boosts = []

    for boost in boosts:
        if get_db_value("boosts", id, boost) > 0:
            active_boosts.append(boost)

    return active_boosts


def boost_time_left(id: int, boost:str) -> str:
    left = get_db_value("boosts", id, boost)
    t = str(datetime.timedelta(seconds=left))
    s = t.split(":")
    hours = s[0]
    mins = s[1]
    secs = s[2]

    l = ""

    if int(hours) != 0:
        l = l + hours + " hours "
    if int(mins) != 0:
        l = l + mins + " minutes "
    """
    if int(secs) != 0:
        l = l + secs + " seconds "
    """

    l = l + "left"

    return l

def boost_time_left_int(id:int, boost:str) -> int:
    return get_db_value("boosts", id, boost)

def boost_loop():
    global boosts
    print("started boost loop")

    while not kill_threads:
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT id FROM boosts")

        ids = [job[0] for job in cursor.execute("SELECT id FROM boosts")]

        for id in ids:
            for boost in boosts:
                current_val = get_db_value("boosts", id, boost)
                if current_val > 0:
                    new_val = current_val - 1
                    set_db_value("boosts", id, boost, new_val)

        #wait(60)

        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                  55, 56, 57, 58, 59, 60]:
            if not kill_threads:
                wait(1)
            else:
                break

    print("ended boost loop")


def secToMin(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return hour, min, sec

def hoursToSec(Hours):
    return Hours * 60 * 60
