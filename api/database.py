import json
import os
from api.user import User, from_String
from settings import default_cash


class Database():
    def __init__(self) -> None:
        if not os.path.exists("./database"):
            os.mkdir("./database")
        else:
            pass

    def add_user(self, user: User):
        if os.path.exists("./database"):
            with open(f"./database/{user.id}.json", "w") as f:
                json.dump(user, f, cls=CustomEncoder)

            pass

    def get_user(self, id: int) -> User:
        if os.path.exists("./database"):
            if os.path.exists("./database/{0}.json".format(id)):
                with open("./database/{0}.json".format(id), "r") as file:
                    return from_String(file.read())

        u = User(id, default_cash, 1, 0, 0, 0, [])

        self.add_user(u)

        return u

    def remove_user(self, id: int):
        if os.path.exists("./database"):
            if os.path.exists(f"./database/{id}.json"):
                os.remove(f"./database/{id}.json")

    def give_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.cash += amount
        self.add_user(u)

    def give_level(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.farm_level += amount
        self.add_user(u)

    def give_iron_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.ironcash += amount
        self.add_user(u)

    def give_gold_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.goldcash += amount
        self.add_user(u)

    def give_yolk_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.eggyolks += amount
        self.add_user(u)

    def give_inv_item(self, id: int, amount: int, obj: str):
        u = self.get_user(id)
        self.remove_user(id)
        i = 1
        while i <= amount:
            u.inventory.append(obj)
            i += 1
        self.add_user(u)

    def remove_inv_item(self, id: int, amount: int, obj: str):
        i = 1
        while i >= amount:
            if self.has_inventory(id, obj):
                self.get_user(id).inventory.remove(obj)
                i += 1
            else:
                return

    def has_inventory(self, id: int, object: str) -> bool:
        return object in self.get_user(id).inventory


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__  # Convert the object to a dictionary
        return super().default(obj)
