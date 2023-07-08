import os
import json
from api.database import Database


# Assuming you have already defined the Database class


def add_json_files_to_database(database):
    database_directory = "database"  # Specify the directory where your JSON files are located

    # Iterate through each file in the directory
    for filename in os.listdir(database_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(database_directory, filename)

            # Read the contents of the JSON file
            with open(filepath, "r") as file:
                json_data = json.load(file)

            # Extract the required attributes from the JSON data
            id = json_data.get("id")
            cash = json_data.get("cash")
            farm_level = json_data.get("farm_level")
            ironcash = json_data.get("ironcash")
            goldcash = json_data.get("goldcash")
            eggyolks = json_data.get("eggyolks")
            inventory = json_data.get("inventory", [])

            # Add the user to the database
            database.add_user(id)

            # Update the user's attributes in the database
            database.give_cash(id, cash)
            database.give_farm_level(id, farm_level-1)
            database.give_iron_cash(id, ironcash)
            database.give_gold_cash(id, goldcash)
            database.give_eggyolks(id, eggyolks)

            # Update the user's inventory in the database
            for item in inventory:
                item_name = item.get("name")
                item_amount = item.get("amount")
                if item_name and item_amount:
                    database.give_inventory_item(id, item_name, item_amount)

            print(f"Added data from {filename} to the database.")


# Create an instance of the Database class
database = Database()

# Call the function to add JSON files to the database
add_json_files_to_database(database)