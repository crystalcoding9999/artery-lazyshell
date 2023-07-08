import sqlite3
import settings


class Database:
    def __init__(self):
        db = sqlite3.connect(f"main.sqlite")
        cursor = db.cursor()
        self.file_name = "main"
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS main (
            id INTEGER, cash INTEGER, farm_level INTEGER, ironcash INTEGER, goldcash INTEGER, eggyolks INTEGER
        )''')

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS inventory ( id INTEGER, binoculars INTEGER, lucky_drumstick 
        INTEGER, golden_chicken INTEGER, eggcellent_statue INTEGER, delicate_shovel INTEGER, egg_topper INTEGER, 
        golden_shovel INTEGER, jackpot INTEGER, custom_role INTEGER, custom_channel INTEGER )''')

        print("created database")

    def wipe_database(self):
        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"DELETE FROM main")
        cursor.execute(f"DELETE FROM inventory")

        db.commit()
        cursor.close()
        db.close()

        print("Database wiped.")

    def add_user(self, id:int):
        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM {self.file_name} WHERE id = {id}")
        result = cursor.fetchone()
        cursor.execute(f"SELECT id FROM inventory WHERE id = {id}")
        result2 = cursor.fetchone()
        if result is None:
            sql_1 = ("INSERT INTO main(id, cash, farm_level, ironcash, goldcash, eggyolks) VALUES (?, ?, ?, ?, ?, ?)")
            val_1 = (id, settings.default_cash, 1, 0, 0, 0)
            cursor.execute(sql_1, val_1)
        if result2 is None:
            sql_2 = ("INSERT INTO inventory(id, binoculars, lucky_drumstick, golden_chicken, eggcellent_statue, " +
                     "delicate_shovel, egg_topper, golden_shovel, jackpot, custom_role, custom_channel) VALUES (?, ?, " +
                     "?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val_2 = (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql_2, val_2)

        db.commit()
        cursor.close()
        db.close()

    def get_cash(self, id:int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT cash FROM {self.file_name} WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_cash(self, id:int, amount:int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT cash FROM {self.file_name} WHERE id = {id}")
        cash = cursor.fetchone()

        try:
            cash = cash[0]
        except:
            cash = 0

        sql = (f"UPDATE {self.file_name} SET cash = ? WHERE id = ?")
        val = (cash + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} eggs to {id}")

        db.commit()
        cursor.close()
        db.close()

    def get_iron_cash(self, id: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT ironcash FROM {self.file_name} WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_iron_cash(self, id: int, amount: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT ironcash FROM {self.file_name} WHERE id = {id}")
        cash = cursor.fetchone()

        try:
            cash = cash[0]
        except:
            cash = 0

        sql = (f"UPDATE main SET ironcash = ? WHERE id = ?")
        val = (cash + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} iron eggs to {id}")

        db.commit()
        cursor.close()
        db.close()

    def get_gold_cash(self, id: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT goldcash FROM {self.file_name} WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_gold_cash(self, id: int, amount: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT goldcash FROM {self.file_name} WHERE id = {id}")
        cash = cursor.fetchone()

        try:
            cash = cash[0]
        except:
            cash = 0

        sql = (f"UPDATE main SET goldcash = ? WHERE id = ?")

        val = (cash + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} gold eggs to {id}")

        db.commit()
        cursor.close()
        db.close()

    def get_eggyolks(self, id: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT eggyolks FROM {self.file_name} WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_eggyolks(self, id: int, amount: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT eggyolks FROM {self.file_name} WHERE id = {id}")
        cash = cursor.fetchone()

        try:
            cash = cash[0]
        except:
            cash = 0

        sql = (f"UPDATE {self.file_name} SET eggyolks = ? WHERE id = ?")
        val = (cash + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} eggyolks to {id}")

        db.commit()
        cursor.close()
        db.close()

    def get_farm_level(self, id: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT farm_level FROM {self.file_name} WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_farm_level(self, id: int, amount: int):
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT farm_level FROM {self.file_name} WHERE id = {id}")
        cash = cursor.fetchone()

        try:
            cash = cash[0]
        except:
            cash = 0

        sql = (f"UPDATE {self.file_name} SET farm_level = ? WHERE id = ?")
        val = (cash + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} to {id}")

        db.commit()
        cursor.close()
        db.close()

    def has_inventory_item(self, id: int, item: str) -> bool:
        self.add_user(id)

        item = item.replace(' ', '_')

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT {item} FROM inventory WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        if cash == 0:
            return False
        else:
            return True

    def get_inventory_amount(self, id: int, item: str) -> bool:
        self.add_user(id)

        item = item.replace(' ', '_')

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT {item} FROM inventory WHERE id = {id}")
        bal = cursor.fetchone()
        try:
            cash = bal[0]
        except:
            cash = 0

        return cash

    def give_inventory_item(self, id: int, item: str, amount: int):
        self.add_user(id)

        item = item.replace(' ', '_')

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT {item} FROM inventory WHERE id = {id}")
        item_db = cursor.fetchone()

        try:
            item_db = item_db[0]
        except:
            item_db = 0

        sql = (f"UPDATE inventory SET {item} = ? WHERE id = ?")
        val = (item_db + amount, id)
        cursor.execute(sql, val)

        print(f"gave {amount} {item}s to {id}")

        db.commit()
        cursor.close()
        db.close()

    def remove_inventory_item(self, id: int, item: str, amount: int):
        self.add_user(id)

        item = item.replace(' ', '_')

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT {item} FROM inventory WHERE id = {id}")
        item_db = cursor.fetchone()

        try:
            item_db = item_db[0]
        except:
            item_db = 0

        sql = (f"UPDATE inventory SET {item} = ? WHERE id = ?")
        val = (item_db - amount, id)
        cursor.execute(sql, val)

        print(f"took {amount} {item}s from {id}")

        db.commit()
        cursor.close()
        db.close()

    def is_inventory_empty(self, id: int) -> bool:
        self.add_user(id)

        db = sqlite3.connect(f"{self.file_name}.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT SUM(binoculars, lucky_drumstick, golden_chicken, eggcellent_statue, delicate_shovel, " +
                       f"egg_topper, golden_shovel, jackpot, custom_role, custom_channel) " +
                       f"FROM inventory WHERE id = {id}")
        total_items = cursor.fetchone()[0]
        total_items = total_items if total_items else 0

        return total_items == 0
