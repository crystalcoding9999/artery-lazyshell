import api

test_database = api.Database()

test_database.add_user(0)

test_database.give_inventory_item(0, "binoculars", 1)
