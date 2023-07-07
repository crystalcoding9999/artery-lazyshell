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
        try:
            if os.path.exists("./database"):
                if os.path.exists("./database/{0}.json".format(id)):
                    with open("./database/{0}.json".format(id), "r") as file:
                        return from_String(file.read())
        except Exception as e:
            print(e)
            return self.get_user(id)
      
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
        print("gave {0} {1} cash they now have {2}".format(id, amount, u.id))
        self.add_user(u)

    def give_level(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.farm_level += amount
        print("gave {0} {1} level they now have {2}".format(id, amount, u.farm_level))
        self.add_user(u)

    def give_iron_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.ironcash += amount
        print("gave {0} {1} iron cash they now have {2}".format(id, amount, u.ironcash))
        self.add_user(u)

    def give_gold_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.goldcash += amount
        print("gave {0} {1} gold cash they now have {2}".format(id, amount, u.goldcash))
        self.add_user(u)

    def give_yolk_cash(self, id: int, amount: int):
        u = self.get_user(id)
        self.remove_user(id)
        u.eggyolks += amount
        print("gave {0} {1} yolk cash they now have {2}".format(id, amount, u.eggyolks))
        self.add_user(u)

    def give_inv_item(self, id: int, amount: int, obj: str):
        u = self.get_user(id)
        self.remove_user(id)
        i = 1
        while i <= amount:
            u.inventory.append(obj)
            i += 1
        print("gave {0} {1} {2}".format(id, amount, obj))
        self.add_user(u)

    def remove_inv_item(self, id: int, amount: int, obj: str):
        i = 1
        while i >= amount:
            if self.has_inventory(id, obj):
                self.get_user(id).inventory.remove(obj)
                i += 1
            else:
                break

        print("took {0} {1} {2}".format(id, amount, obj))

    def has_inventory(self, id: int, object: str) -> bool:
        return object in self.get_user(id).inventory


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__  # Convert the object to a dictionary
        return super().default(obj)
