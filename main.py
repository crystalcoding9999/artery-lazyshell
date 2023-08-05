import os
import random
import time
from datetime import date, datetime
import shutil

import discord
from discord.ext import commands

import api.boostManager
import settings
from api import Database
import threading
from keep_alive import keep_alive

inte = discord.Intents.default()
inte.messages = True
inte.message_content = True
inte.members = True

false = False
true = True

bot = commands.Bot(
    command_prefix=settings.bot_prefix,  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=inte,
    help_command=None
)

bot.author_id = 1102272783712522331  # Change to your discord id!!!

database = Database()
server: discord.Guild | None = None


@bot.event
async def on_ready():  # When the bot is ready
    global server
    server = bot.get_guild(settings.guild_id)
    print("logged in as {0.user}".format(bot))


@bot.event
async def on_message(ctx):
    if ctx.channel.id not in settings.talk_blacklisted_channels:
        await eggy_check(ctx, True)

    if isinstance(ctx.channel, discord.Thread):
        if ctx.author.id == 235148962103951360 and ctx.channel.id == 1122532250915975208:
            try:
                await ctx.delete()
            except discord.errors.NotFound:
                pass

    await bot.process_commands(ctx)


"""
@bot.command("help")
async def help(ctx, page: int = 1):
    emb = discord.Embed(
        title="commands"
    )

    if bot.get_guild(settings.guild_id).get_role(settings.staff_role) in ctx.author.roles:
        if page == 1:
            emb.description = "**Announce**\nMake an announcement for everyone to see\n\n" \
                              "**Basket**\nShow you all the eggs you have\n\n" \
                              "**Buy**\nBuy something from the market\n\n" \
                              "**Crack**\nCrack an egg open to get egg yolks (**Requires Egg Topper**)\n\n" \
                              "**Dig**\nDig up some eggs (**Requires Delicate Shovel or Golden Shovel**)\n\n" \
                              "**Dupe**\nDo what science cant and clone some eggs\n\n"
            emb.set_footer(text="page 1/3")
        elif page == 2:
            emb.description = "**Harvest**\nHarvest the eggs that the chickens laid\n\n" \
                              "**Help**\nShow this list\n\n" \
                              "**Hunt**\nTry and see if you can find some eggs lying around\n\n" \
                              "**Inventory**\nShow you all the items you own\n\n" \
                              "**Nick**\nTake some eggs from someone\n\n" \
                              "**Pay**\nGive the previously taken eggs back"
            emb.set_footer(text="page 2/3")
        elif page == 3:
            emb.description = "**Profile**\nShow some more information about your farm\n\n" \
                              "**Shop**\nGo visit the store\n\n" \
                              "**Share**\nShare some eggs with your friends\n\n" \
                              "**Explore**\nGo explore for some eggs\n\n" \
                              "**Bargain**\nBargain for your eggs"
            emb.set_footer(text="page 3/3")
    else:
        if page == 1:
            emb.description = "**Basket**\nShow you all the eggs you have\n\n" \
                              "**Buy**\nBuy something from the market\n\n" \
                              "**Crack**\nCrack an egg open to get egg yolks (**Requires Egg Topper**)\n\n" \
                              "**Dig**\nDig up some eggs (**Requires Delicate Shovel or Golden Shovel**)\n\n" \
                              "**Dupe**\nDo what science cant and clone some eggs\n\n" \
                              "**Harvest**\nHarvest the eggs that the chickens laid\n\n"
            emb.set_footer(text="page 1/3")
        elif page == 2:
            emb.description = "**Help**\nShow this list\n\n" \
                              "**Hunt**\nTry and see if you can find some eggs lying around\n\n" \
                              "**Inventory**\nShow you all the items you own\n\n" \
                              "**Profile**\nShow some more information about your farm\n\n" \
                              "**Shop**\nGo visit the store\n\n" \
                              "**Share**\nShare some eggs with your friends"
            emb.set_footer(text="page 2/3")
        elif page == 3:
            emb.description = "**Explore**\nGo explore for some eggs\n\n" \
                              "**Bargain**\nBargain for your eggs"
            emb.set_footer(text="page 3/3")

    await ctx.channel.send(embed=emb)
"""


@bot.group("help")
async def help_group(ctx):
    if ctx.invoked_subcommand is not None:
        return

    desc = "Economy ```+help economy```\nGuilds ```+help guilds```"

    emb = create_embed("What do you need help with", desc)
    await ctx.channel.send(embed=emb)


@help_group.command("economy", aliases=["e", "eco"])
async def help_eco(ctx, page: int = 1):
    emb = discord.Embed(
        title="Economy Commands"
    )

    if bot.get_guild(settings.guild_id).get_role(settings.staff_role) in ctx.author.roles:
        if page == 1:
            emb.description = "**Announce**\nMake an announcement for everyone to see\n\n" \
                              "**Basket**\nShow you all the eggs you have\n\n" \
                              "**Buy**\nBuy something from the market\n\n" \
                              "**Crack**\nCrack an egg open to get egg yolks (**Requires Egg Topper**)\n\n" \
                              "**Dig**\nDig up some eggs (**Requires Delicate Shovel or Golden Shovel**)\n\n" \
                              "**Dupe**\nDo what science cant and clone some eggs\n\n"
            emb.set_footer(text="page 1/3")
        elif page == 2:
            emb.description = "**Harvest**\nHarvest the eggs that the chickens laid\n\n" \
                              "**Help**\nShow this list\n\n" \
                              "**Hunt**\nTry and see if you can find some eggs lying around\n\n" \
                              "**Inventory**\nShow you all the items you own\n\n" \
                              "**Nick**\nTake some eggs from someone\n\n" \
                              "**Pay**\nGive the previously taken eggs back"
            emb.set_footer(text="page 2/3")
        elif page == 3:
            emb.description = "**Profile**\nShow some more information about your farm\n\n" \
                              "**Shop**\nGo visit the store\n\n" \
                              "**Share**\nShare some eggs with your friends\n\n" \
                              "**Explore**\nGo explore for some eggs\n\n" \
                              "**Bargain**\nBargain for your eggs"
            emb.set_footer(text="page 3/3")
    else:
        if page == 1:
            emb.description = "**Basket**\nShow you all the eggs you have\n\n" \
                              "**Buy**\nBuy something from the market\n\n" \
                              "**Crack**\nCrack an egg open to get egg yolks (**Requires Egg Topper**)\n\n" \
                              "**Dig**\nDig up some eggs (**Requires Delicate Shovel or Golden Shovel**)\n\n" \
                              "**Dupe**\nDo what science cant and clone some eggs\n\n" \
                              "**Harvest**\nHarvest the eggs that the chickens laid\n\n"
            emb.set_footer(text="page 1/3")
        elif page == 2:
            emb.description = "**Help**\nShow this list\n\n" \
                              "**Hunt**\nTry and see if you can find some eggs lying around\n\n" \
                              "**Inventory**\nShow you all the items you own\n\n" \
                              "**Profile**\nShow some more information about your farm\n\n" \
                              "**Shop**\nGo visit the store\n\n" \
                              "**Share**\nShare some eggs with your friends"
            emb.set_footer(text="page 2/3")
        elif page == 3:
            emb.description = "**Explore**\nGo explore for some eggs\n\n" \
                              "**Bargain**\nBargain for your eggs"
            emb.set_footer(text="page 3/3")

    await ctx.channel.send(embed=emb)


@help_group.command("guilds", aliases=["g", "guild"])
async def help_guilds(ctx, page: int = 1):
    emb = discord.Embed(
        title="Guild Commands"
    )

    desc = ""

    if page == 1:
        desc = "**Guilds**\nShows a list of all the guilds\n\n" \
               "**Guild**\nShows your guilds profile\n\n" \
               "**Guild Profile**\nShows a guilds profile\n\n" \
               "**Guild Deposit**\nDeposit egg/silver eggs/golden eggs into your guild bank\n\n" \
               "**Guild Withdraw**\nWithdraw eggs/silver eggs/golden eggs from you guild bank (**Requires guild permissions!**)"
    elif page == 2:
        desc = "**Guild Join**\nJoin a guild (**7 day cooldown!**)\n\n" \
               "**Guild Leave**\nLeave your guild\n\n" \
               "**Guild Perms Check**\nSee if you have guild permissions\n\n" \
               "**Guild Leaderboard**\npretty self explanatory"

    if page == 2 and api.guildManager.is_guild_master(ctx) is True and ctx.guild.get_role(settings.guildMasterRole) in ctx.author.roles:
        desc = desc + "\n\n" \
                      "**Guild Perms Add**\nAdd guild permissions to a user\n\n" \
                      "**Guild Perms Remove**\nRemove guild permissions from a user"


    emb.description = desc
    await ctx.channel.send(embed=emb)


@bot.command("announce", aliases=["a"])
@commands.has_role(settings.staff_role)
async def announce(ctx, *, args):
    achannel = bot.get_channel(settings.announce_channel_id)
    splits = args.split("|")

    if len(splits) <= 1:
        await ctx.channel.send(
            "wrong use! {0}announce (title)|(announcement)|(?banner). yes the '|' is neccesary".format(
                settings.bot_prefix))
        return

    argument = splits[0]
    announcement = splits[1]

    if len(splits) == 3:
        banner = splits[2]
    else:
        banner = None

    emb = discord.Embed(
        title=argument,
        description=announcement
    )

    emb.set_image(url=banner)

    current_time = date.today()

    emb.set_footer(text=str(current_time),
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121495423580901386/image0.gif")

    await achannel.send(embed=emb)
    await ctx.channel.send(embed=emb)


@announce.error
async def announce_error(ctx, error):
    await error_handling(ctx, error, "announce")


@bot.command("basket", aliases=["eggs", "b"])
async def basket(ctx, person: discord.Member = None):
    if person is None:
        person = ctx.author
    await eggy_check(ctx, False)
    authorID = person.id
    desc = "You currently have" + "\n<:eggy:1121872437055869048> {0} {1}".format(int(database.get_cash(authorID)),
                                                                                 settings.cash_name) \
           + "\n<:silvereggy:1122255924669726800> {0} {1}".format(int(database.get_iron_cash(authorID)),
                                                                  settings.iron_cash_name) \
           + "\n<:goldeneggy:1121874261649399879> {0} {1}".format(int(database.get_gold_cash(authorID)),
                                                                  settings.gold_cash_name) \
           + "\n<:eggyolk:1121874358730772600> {0} {1}".format(int(database.get_eggyolks(authorID)),
                                                               settings.yolk_cash_name)
    emb = discord.Embed(
        description=desc
    )

    emb.set_author(name="{0}'s Egg Basket".format(person.name),
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")

    await ctx.channel.send(embed=emb)
    return False


@bot.command("transfer", aliases=["share"])
@commands.cooldown(1, 8, commands.BucketType.user)
async def transfer(ctx, target: discord.Member, what: str = None, amount: int = 0):
    await eggy_check(ctx, False)
    if what is None or amount == 0:
        await ctx.channel.send(
            embed=create_embed("What", "What would you like to share: ```\neggs\nsilvereggs\ngoldeneggs```").set_footer(
                text="Example Usage:\n+share @user item 1 10\n+share @user eggs 10"))
        return
    authorID = ctx.author.id
    targetID = target.id
    emb = discord.Embed(
        title="if you see this something went wrong"
    )
    emb.set_author(name="Egg Basket",
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
    if what == "eggs" or what == "egg" or what == "eggy" or what == "eggys":
        if database.get_cash(authorID) >= amount:
            database.give_cash(authorID, -amount)
            database.give_cash(targetID, amount)
            emb = discord.Embed(
                title="success",
                description="successfully shared {3} {0} {1} with {2}".format(amount, settings.cash_name, target,
                                                                              settings.emojis["eggy"])
            )
        else:
            emb = discord.Embed(
                title="failed!",
                description="you dont have enough eggs to share with {0}".format(target)
            )
    elif what == "silvereggs" or what == "silveregg" or what == "silvereggy" or what == "silvereggys":
        if database.get_iron_cash(authorID) >= amount:
            database.give_iron_cash(authorID, -amount)
            database.give_iron_cash(targetID, amount)
            emb = discord.Embed(
                title="success",
                description="successfully shared {3} {0} {1} with {2}".format(amount, settings.iron_cash_name, target,
                                                                              settings.emojis["silver eggy"])
            )
        else:
            emb = discord.Embed(
                title="failed!",
                description="you dont have enough silver eggs to share with {0}".format(target)
            )
    elif what == "goldeneggs" or what == "goldenegg" or what == "goldeneggy" or what == "goldeneggys":
        if database.get_gold_cash(authorID) >= amount:
            database.give_gold_cash(authorID, -amount)
            database.give_gold_cash(targetID, amount)
            emb = discord.Embed(
                title="success",
                description="successfully shared {3} {0} {1} with {2}".format(amount, settings.gold_cash_name, target,
                                                                              settings.emojis["golden eggy"])
            )
        else:
            emb = discord.Embed(
                title="failed!",
                description="you dont have enough golden eggs to share with {0}".format(target)
            )

    await ctx.channel.send(embed=emb)


@transfer.error
async def transfer_error(ctx, error):
    await error_handling(ctx, error, "transfer")


@bot.command("gift")
@commands.cooldown(1, 8, commands.BucketType.user)
async def gift(ctx, target: discord.Member, item_id: int, amount: int = 1):
    await eggy_check(ctx, False)
    authorID = ctx.author.id
    targetID = target.id
    emb = discord.Embed(
        title="if you see this something went wrong"
    )
    emb.set_author(name="Egg Basket",
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")

    item: str | None = id_to_object(item_id)

    if item is None:
        await ctx.channel.send(
            embed=create_embed("What", "what do you want to gift?\nplease specify the item id found in the shop"))
        return
    elif not database.get_inventory_amount(authorID, item) <= amount:
        await ctx.channel.send(
            embed=create_embed("Failed", "you dont own (enough of) this item")
        )
        return
    elif database.has_inventory_item(targetID, item) and (item != "eggcellent_statue" and item != "egg topper"):
        await ctx.channel.send(
            embed=create_embed("Failed", "they already own this item!")
        )
        return
    else:
        database.remove_inventory_item(authorID, item, amount)
        database.give_inventory_item(targetID, item, amount)
        emb = create_embed("Success", "Successfully gave {0} {1} to {2}".format(amount, item, target))

    await ctx.channel.send(embed=emb)


@bot.command("harvest", aliases=["h"])
@commands.cooldown(1, settings.harvest_cooldown, commands.BucketType.user)
async def harvest(ctx):
    await eggy_check(ctx, False)
    authorID = ctx.author.id
    flevel = database.get_farm_level(authorID)
    if flevel == 1:
        earned = random.randint(settings.level_1_farm_min, settings.level_1_farm_max)
    elif flevel == 2:
        earned = random.randint(settings.level_2_farm_min, settings.level_2_farm_max)
    elif flevel == 3:
        earned = random.randint(settings.level_3_farm_min, settings.level_3_farm_max)
    elif flevel == 4:
        earned = random.randint(settings.level_4_farm_min, settings.level_4_farm_max)
    elif flevel == 5:
        earned = random.randint(settings.level_5_farm_min, settings.level_5_farm_max)
    else:
        await ctx.channel.send("looks like you have a bugged farm level please contact @crystalcoding_!")
        return

    #    if database.has_inventory_item(authorID, "golden_chicken"):
    #        earned *= 1.5
    #        earned = int(round(earned, 0))

    if database.has_inventory_item(authorID, "golden_chicken"):
        earned *= 1.5
        earned = int(round(earned, 0))

    emb = discord.Embed(
        description="successfully harvested {2} {0} {1}".format(earned, settings.cash_name, settings.emojis["eggy"])
    )

    emb.set_author(name="Egg Basket",
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")

    database.give_cash(authorID, earned)
    await ctx.channel.send(embed=emb)


@harvest.error
async def harvest_error(ctx, error):
    await error_handling(ctx, error, "harvest")


"""
@bot.command("shop", aliases=["store", "market"])
async def shop(ctx, store: str = "list"):
    await eggy_check(ctx, False)
    authorID = ctx.author.id
    if store == "economy" or store == "eco" or store == "e":
        emb = discord.Embed(
            title=None,
        )

        flevel = database.get_farm_level(authorID)
        cost = settings.level_2_unlock_cost
        if flevel == 1:
            cost = settings.level_2_unlock_cost
        elif flevel == 2:
            cost = settings.level_3_unlock_cost
        elif flevel == 3:
            cost = settings.level_4_unlock_cost
        elif flevel == 4:
            cost = settings.level_5_unlock_cost

        bin_id = settings.object_ids["binoculars"]
        ld_id = settings.object_ids["lucky drumstick"]
        gc_id = settings.object_ids["golden chicken"]
        es_id = settings.object_ids["eggcellent statue"]
        ds_id = settings.object_ids["delicate shovel"]
        et_id = settings.object_ids["egg topper"]
        gs_id = settings.object_ids["golden shovel"]
        jp_id = settings.object_ids["jackpot"]

        if flevel != 5:
            fl_desc = "{3}**Farm Upgrade**: {1} {2}\nUpgrade your farm to level {0}".format((flevel + 1), cost,
                                                                                            settings.eggy_emoji,
                                                                                            settings.emojis["farm"], )
        else:
            fl_desc = "{0}**Farm Upgrade**:\nYou already have the max level farm!".format(settings.emojis["farm"])

        if not database.has_inventory_item(authorID, "binoculars"):
            bin_desc = "{2}**Binoculars**: {0} {1}\n{3}".format(settings.object_costs["binoculars"],
                                                                settings.emojis["silver eggy"],
                                                                settings.emojis["binoculars"],
                                                                settings.object_descs["binoculars"])
        else:
            bin_desc = "{2}**Binoculars** (**owned**): {0} {1}\n{3}".format(
                settings.object_costs["binoculars"],
                settings.emojis["silver eggy"],
                settings.emojis["binoculars"],
                settings.object_descs["binoculars"])

        if not database.has_inventory_item(authorID, "lucky_drumstick"):
            ld_desc = "{2}**Lucky Drumstick**: {1} {0}\n{3}".format(
                settings.emojis["silver eggy"],
                settings.object_costs["lucky drumstick"],
                settings.emojis["lucky drumstick"],
                settings.object_descs["lucky drumstick"])
        else:
            ld_desc = "{2}**Lucky Drumstick** (**owned**): {1} {0}\n{3}".format(
                settings.emojis["silver eggy"],
                settings.object_costs["lucky drumstick"],
                settings.emojis["lucky drumstick"],
                settings.object_descs["lucky drumstick"])

        if not database.has_inventory_item(authorID, "golden_chicken"):
            gc_desc = "{2}**Golden Chicken**: {1} {0}\n{3}".format(
                settings.emojis["silver eggy"],
                settings.object_costs["golden chicken"],
                settings.emojis["golden chicken"],
                settings.object_descs["golden chicken"])
        else:
            gc_desc = "{2}**Golden Chicken** (**owned**): {1} {0}\n{3}".format(
                settings.emojis["silver eggy"],
                settings.object_costs["golden chicken"],
                settings.emojis["golden chicken"],
                settings.object_descs["golden chicken"])

        if not database.has_inventory_item(authorID, "eggcellent_statue"):
            es_desc = "{2}**Eggcellent Statue**: {1} {0}\n{3}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["eggcellent statue"],
                settings.emojis["eggcellent statue"],
                settings.object_descs["eggcellent statue"])
        else:
            count = database.get_inventory_amount(authorID, "eggcellent_statue")
            es_desc = "{3}**Eggcellent Statue** (**{2} owned**): {1} {0}\n{3}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["eggcellent statue"],
                count,
                settings.emojis["eggcellent statue"],
                settings.object_descs["eggcellent statue"])

        if not database.has_inventory_item(authorID, "delicate_shovel"):
            ds_desc = "{2}**Delicate Shovel**: {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.object_costs["delicate shovel"],
                settings.emojis["delicate shovel"],
                settings.object_descs["delicate shovel"])
        else:
            ds_desc = "{2}**Delicate Shovel** (**owned**): {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.object_costs["delicate shovel"],
                settings.emojis["delicate shovel"],
                settings.object_descs["delicate shovel"])

        if not database.has_inventory_item(authorID, "egg_topper"):
            et_desc = "{2}**Egg Topper**: {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.object_costs["egg topper"],
                settings.emojis["egg topper"],
                settings.object_descs["egg topper"])
        else:
            count = database.get_inventory_amount(authorID, "egg topper")
            et_desc = "{3}**Egg Topper** (**{2} owned**): {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.object_costs["egg topper"],
                count,
                settings.emojis["egg topper"],
                settings.object_descs["egg topper"])

        if not database.has_inventory_item(authorID, "golden_shovel"):
            gs_desc = "{2}**Golden Shovel**: {1} {0}\n{3}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["golden shovel"],
                settings.emojis["golden shovel"],
                settings.object_descs["golden shovel"])
        else:
            gs_desc = "{2}**Golden Shovel** (**owned**): {1} {0}\n{3}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["golden shovel"],
                settings.emojis["golden shovel"],
                settings.object_descs["golden shovel"])

        if not database.has_inventory_item(authorID, "jackpot"):
            jp_desc = "{2}**Jackpot**: {1} {0}\n{3}" \
                .format(settings.emojis["silver eggy"],
                        settings.object_costs["jackpot"],
                        settings.emojis["jackpot"],
                        settings.object_descs["jackpot"])
        else:
            jp_desc = "{2}**Jackpot** (**owned**): {1} {0}\n{3}" \
                .format(settings.emojis["silver eggy"],
                        settings.object_costs["jackpot"],
                        settings.emojis["jackpot"],
                        settings.object_descs["jackpot"])

        # emb.add_field(name="more coming soon", value="probably...", inline=False)

        bin_desc += f"\n`item id: {bin_id}`"
        ld_desc += f"\n`item id: {ld_id}`"
        gc_desc += f"\n`item id: {gc_id}`"
        es_desc += f"\n`item id: {es_id}`"
        ds_desc += f"\n`item id: {ds_id}`"
        et_desc += f"\n`item id: {et_id}`"
        gs_desc += f"\n`item id: {gs_id}`"
        jp_desc += f"\n`item id: {jp_id}`"

        # emb.description = fl_desc + "\n" + bin_desc + "\n" + ld_desc + "\n" + gc_desc
        emb.description = fl_desc \
                          + "\n\n" \
                          + et_desc \
                          + "\n\n" \
                          + ds_desc \
                          + "\n\n" \
                          + jp_desc \
                          + "\n\n" \
                          + gc_desc \
                          + "\n\n" \
                          + bin_desc \
                          + "\n\n" \
                          + ld_desc \
                          + "\n\n" \
                          + es_desc \
                          + "\n\n" \
                          + gs_desc

        emb.set_author(name="The Egg Market",
                       icon_url="https://cdn.discordapp.com/attachments/1122532250915975208/1123268970674401392"
                                "/360_F_526917681_vsjPlB6iYUPQvRqTYoElv8fDErQy24Lp-removebg-preview.png")

        await ctx.channel.send(embed=emb)
    elif store == "server" or store == "serv" or store == "s":
        emb = discord.Embed(
            title=None,
        )

        if not database.has_inventory_item(authorID, "custom_role"):
            cr_desc = "**Custom Role**: {1} {0}\n{2}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["custom role"],
                settings.object_descs["custom role"])
        else:
            cr_desc = "**Custom Role** (**owned**): {1} {0}\n{2}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["custom channel"],
                settings.object_descs["custom role"])

        if not database.has_inventory_item(authorID, "custom_channel"):
            cc_desc = "**Custom Channel**: {1} {0}\n{2}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["custom channel"],
                settings.object_descs["custom channel"])
        else:
            cc_desc = "**Custom Channel** (**owned**): {1} {0}\n{2}".format(
                settings.emojis["golden eggy"],
                settings.object_costs["custom channel"],
                settings.object_descs["custom channel"])

        emb.set_author(name="The Server Market",
                       icon_url="https://cdn.discordapp.com/attachments/1122532250915975208/1123268970674401392/360_F_526917681_vsjPlB6iYUPQvRqTYoElv8fDErQy24Lp-removebg-preview.png")

        emb.description = cr_desc + "\n\n" + cc_desc

        await ctx.channel.send(embed=emb)
    else:
        emb = discord.Embed(
            title="Which store would you like to go to?",
            description="The Economy Store ```+shop economy```\nThe Server Store ```+shop server```"
        )
        await ctx.channel.send(embed=emb)
"""


@bot.command("shop", aliases=["store", "market"])
async def shop(ctx, store: str = "list"):
    await eggy_check(ctx, False)
    authorID = ctx.author.id
    eco_aliases = ["e", "eco", "economy"]
    serv_aliases = ["s", "serv", "server"]
    boost_aliases = ["b", "boost", "boosts", "boosters", "booster"]
    if store in eco_aliases:
        desc = ""

        if database.get_farm_level(authorID) != 5:
            next = database.get_farm_level(authorID) + 1
            desc = settings.emojis["farm"] + "**farm upgrade**: " + str(settings.object_costs[("farm_" + str(next))]) + \
                   "" + settings.emojis["eggy"] + "\nUpgrade your farm to level " + str(next) + "\n"

        sorted_ids = sorted(settings.object_ids.items(), key=lambda x: x[1])

        for itemID in sorted_ids:
            try:
                item = id_to_object(itemID[1])
                if item is None:
                    continue
                if settings.object_types[item] != "multi item" and settings.object_types[item] != "item":
                    continue
                itm_desc = ""
                if item in settings.emojis:
                    itm_desc = settings.emojis[item]

                itm_desc = itm_desc + "**" + item + "**"

                if database.has_inventory_item(authorID, item):
                    if item in settings.object_types:
                        if settings.object_types[item] == "multi item":
                            itm_desc = itm_desc + " (**" + str(
                                database.get_inventory_amount(authorID, item)) + " owned**)"
                        else:
                            itm_desc = itm_desc + " (**owned**)"

                itm_desc = itm_desc + ": " + str(settings.object_costs[item])

                emoji = settings.emojis["eggy"]
                if settings.object_egg_types[item] == "silver":
                    emoji = settings.emojis["silver eggy"]
                elif settings.object_egg_types[item] == "gold":
                    emoji = settings.emojis["golden eggy"]

                itm_desc = itm_desc + " " + emoji + "\n" + settings.object_descs[item] + "\n`item id: " + str(
                    settings.object_ids[item]) + "`" + "\n"

                desc = desc + itm_desc
            except IndexError:
                break

        emb = create_embed(None, desc)

        emb.set_author(name="The Egg Market",
                       icon_url="https://cdn.discordapp.com/attachments/1122532250915975208/1123268970674401392"
                                "/360_F_526917681_vsjPlB6iYUPQvRqTYoElv8fDErQy24Lp-removebg-preview.png")

        await ctx.channel.send(embed=emb)
    elif store in serv_aliases:
        desc = ""

        sorted_ids = sorted(settings.object_ids.items(), key=lambda x: x[1])

        for itemID in sorted_ids:
            try:
                item = id_to_object(itemID[1])
                if item is None:
                    continue
                if settings.object_types[item] != "server item":
                    continue
                itm_desc = ""
                if item in settings.emojis:
                    itm_desc = settings.emojis[item]

                itm_desc = itm_desc + "**" + item + "**"

                if database.has_inventory_item(authorID, item):
                    if item in settings.object_types:
                        if settings.object_types[item] == "multi item":
                            itm_desc = itm_desc + " (**" + str(
                                database.get_inventory_amount(authorID, item)) + " owned**)"
                        else:
                            itm_desc = itm_desc + " (**owned**)"

                itm_desc = itm_desc + ": " + str(settings.object_costs[item])

                emoji = settings.emojis["eggy"]
                if settings.object_egg_types[item] == "silver":
                    emoji = settings.emojis["silver eggy"]
                elif settings.object_egg_types[item] == "gold":
                    emoji = settings.emojis["golden eggy"]

                itm_desc = itm_desc + " " + emoji + "\n" + settings.object_descs[item] + "\n`item id: " + str(
                    settings.object_ids[item]) + "`" + "\n"

                desc = desc + itm_desc
            except IndexError:
                break

        emb = create_embed(None, desc)

        emb.set_author(name="The Egg Market",
                       icon_url="https://cdn.discordapp.com/attachments/1122532250915975208/1123268970674401392"
                                "/360_F_526917681_vsjPlB6iYUPQvRqTYoElv8fDErQy24Lp-removebg-preview.png")

        await ctx.channel.send(embed=emb)
    elif store in boost_aliases:
        desc = ""

        sorted_ids = sorted(settings.object_ids.items(), key=lambda x: x[1])

        for itemID in sorted_ids:
            try:
                item = id_to_object(itemID[1])
                if item is None:
                    continue
                if settings.object_types[item] != "boost":
                    continue
                itm_desc = ""
                if item in settings.emojis:
                    itm_desc = settings.emojis[item]

                itm_desc = itm_desc + "**" + item + "**"

                if database.has_inventory_item(authorID, item):
                    if item in settings.object_types:
                        if settings.object_types[item] == "multi item":
                            itm_desc = itm_desc + " (**" + str(
                                database.get_inventory_amount(authorID, item)) + " owned**)"
                        else:
                            itm_desc = itm_desc + " (**owned**)"

                itm_desc = itm_desc + ": " + str(settings.object_costs[item])

                emoji = settings.emojis["eggy"]
                if settings.object_egg_types[item] == "silver":
                    emoji = settings.emojis["silver eggy"]
                elif settings.object_egg_types[item] == "gold":
                    emoji = settings.emojis["golden eggy"]

                itm_desc = itm_desc + " " + emoji + "\n" + settings.object_descs[item] + "\n`item id: " + str(
                    settings.object_ids[item]) + "`" + "\n"

                desc = desc + itm_desc
            except IndexError:
                break

        desc = desc + "\nall boosts last 2 hours!"

        emb = create_embed(None, desc)

        emb.set_author(name="The Egg Market",
                       icon_url="https://cdn.discordapp.com/attachments/1122532250915975208/1123268970674401392"
                                "/360_F_526917681_vsjPlB6iYUPQvRqTYoElv8fDErQy24Lp-removebg-preview.png")

        await ctx.channel.send(embed=emb)
    else:
        emb = discord.Embed(
            title="Which store would you like to go to?",
            description="The Economy Store ```+shop economy```\nThe Server Store ```+shop server```\nThe Boosters Store```+shop boosts```"
        )
        await ctx.channel.send(embed=emb)


"""
@bot.command("buy", aliases=["purchase"])
async def buy(ctx, *, item):
    await eggy_check(ctx, False)
    authorID = ctx.author.id
    if isinstance(item, int):
        item = id_to_object(item)
    if item == "farm" or item == "farm upgrade":
        newlevel = database.get_farm_level(authorID) + 1
        cost = settings.level_2_unlock_cost
        if newlevel == 2:
            cost = settings.level_2_unlock_cost
        elif newlevel == 3:
            cost = settings.level_3_unlock_cost
        elif newlevel == 4:
            cost = settings.level_4_unlock_cost
        elif newlevel == 5:
            cost = settings.level_5_unlock_cost
        elif newlevel >= 6:
            await ctx.channel.send("you already have the max farm level!")
            return

        if database.get_cash(authorID) >= cost:
            database.give_cash(authorID, -cost)
            database.give_farm_level(authorID, 1)
            await ctx.channel.send(
                "successfully purchased the level {0} farm upgrade for {1} {2}".format(newlevel, cost,
                                                                                       settings.cash_name))
        else:
            await ctx.channel.send("you don't have enough eggs to purchase this")
    elif item == "binoculars":
        cost = settings.binocular_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_iron_cash(authorID, -cost)
            database.give_inventory_item(authorID, "binoculars", 1)
            await ctx.channel.send(
                "successfully purchased the binoculars for {2} {0} {1}".format(cost, settings.cash_name,
                                                                               settings.emojis["silver eggy"]))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    elif item == "luckydrumstick" or item == "lucky drumstick" or item == "lucky_drumstick":
        cost = settings.lucky_drumstick_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_iron_cash(authorID, -cost)
            database.give_inventory_item(authorID, "lucky_drumstick", 1)
            await ctx.channel.send(
                "successfully purchased the lucky drumstick for {2} {0} {1}".format(cost, settings.cash_name,
                                                                                    settings.emojis["silver eggy"]))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    elif item == "goldenchicken" or item == "golden chicken" or item == "gold chicken" or item == "golden_chicken" or item == "gold_chicken":
        cost = settings.golden_chicken_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_iron_cash(authorID, -cost)
            database.give_inventory_item(authorID, "golden_chicken", 1)
            await ctx.channel.send(
                "successfully purchased the golden chicken for {2} {0} {1}".format(cost, settings.iron_cash_name,
                                                                                   settings.emojis["silver eggy"]))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    elif item == "custom role" or item == "customrole" or item == "custom_role":
        cost = settings.custom_role_cost
        mchannel = bot.get_channel(settings.mailbox_channel_id)
        srole = bot.get_guild(settings.guild_id).get_role(settings.staff_role)
        if mchannel is None or srole is None:
            await ctx.channel.send("something went wrong! purchase cancelled!")
            return
        elif database.get_gold_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "custom_role", 1)
            await ctx.channel.send(
                "successfully purchased the custom role for {2} {0} {1}. staff will contact you shortly to grant you your role".format(
                    cost, settings.gold_cash_name,
                    settings.emojis["golden eggy"]))
            await mchannel.send("{1.mention}! {0.mention} bought custom role!".format(ctx.author, srole))
        else:
            await ctx.channel.send("you don't have enough golden eggs to purchase this")
    elif item == "custom channel" or item == "customchannel" or item == "custom channel":
        cost = settings.custom_channel_cost
        mchannel = bot.get_channel(settings.mailbox_channel_id)
        srole = bot.get_guild(settings.guild_id).get_role(settings.staff_role)
        if mchannel is None or srole is None:
            await ctx.channel.send("something went wrong! purchase cancelled!")
            return
        elif database.get_gold_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "custom_channel", 1)
            await ctx.channel.send(
                "successfully purchased the custom channel for {2} {0} {1}. staff will contact you shortly to grant you your channel".format(
                    cost, settings.gold_cash_name,
                    settings.emojis["golden eggy"]))
            await mchannel.send("{1.mention}! {0.mention} bought custom channel!".format(ctx.author, srole))
        else:
            await ctx.channel.send("you don't have enough golden eggs to purchase this")
    elif item == "egg statue" or item == "eggy statue" or item == "egg_statue" or item == "eggy_stateu" or item == "eggcellent statue" or item == "eggcellent_statue":
        cost = settings.egg_statue_cost
        if database.get_gold_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "eggcellent_statue", 1)
            await ctx.channel.send(
                "successfully purchased a eggcellent statue for {2} {0} {1}".format(cost, settings.gold_cash_name,
                                                                                    settings.emojis["golden eggy"]))
        else:
            await ctx.channel.send("you don't have enough golden eggs to purchase this")
    elif item == "egg topper" or item == "eggy topper" or item == "egg_topper" or item == "eggy_topper":
        cost = settings.egg_toper_cost
        if database.get_cash(authorID) >= cost:
            database.give_cash(authorID, -cost)
            database.give_inventory_item(authorID, "egg_topper", 1)
            await ctx.channel.send(
                "successfully purchased the egg topper for {2} {0} {1}".format(cost, settings.cash_name,
                                                                               settings.eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough eggs to purchase this")
    elif item == "shovel" or item == "delicate shovel" or item == "delicate_shovel":
        cost = settings.delicate_shovel_cost
        if database.get_cash(authorID) >= cost:
            database.give_cash(authorID, -cost)
            database.give_inventory_item(authorID, "delicate_shovel", 1)
            await ctx.channel.send(
                "successfully purchased the delicate shovel for {2} {0} {1}".format(cost, settings.cash_name,
                                                                                    settings.eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough eggs to purchase this")
    elif item == "gshovel" or item == "golden shovel" or item == "golden_shovel":
        cost = settings.golden_shovel_cost
        if database.get_gold_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "golden_shovel", 1)
            await ctx.channel.send(
                "successfully purchased the golden shovel for {2} {0} {1}".format(cost, settings.gold_cash_name,
                                                                                  settings.emojis["golden eggy"]))
        else:
            await ctx.channel.send("you don't have enough golden eggs to purchase this")
    elif item == "jackpot" or item == "jpot" or item == "jackp":
        cost = settings.jackpot_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "jackpot", 1)
            await ctx.channel.send(
                "successfully purchased the jackpot for {2} {0} {1}".format(cost, settings.iron_cash_name,
                                                                            settings.emojis["silver eggy"]))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    else:
        await ctx.channel.send("invalid item")
"""


@bot.command("buy", aliases=["purchase"])
async def buy(ctx, *, item):
    await eggy_check(ctx, False)
    authorID = ctx.author.id

    try:
        item = int(item)
    except ValueError:
        item = item

    if isinstance(item, int):
        item = id_to_object(item)

    if item == "farm":
        item = "farm_" + str(database.get_farm_level(authorID) + 1)
        if item == "farm_6":
            await ctx.channel.send("you already own the max level farm")
            return

    if item is None or item not in settings.object_costs:
        await ctx.channel.send("invalid item")
        return

    cost = settings.object_costs[item]
    can_buy = False
    if settings.object_egg_types[item] == "":
        can_buy = database.get_cash(authorID) >= cost
    elif settings.object_egg_types[item] == "silver":
        can_buy = database.get_iron_cash(authorID) >= cost
    elif settings.object_egg_types[item] == "gold":
        can_buy = database.get_gold_cash(authorID) >= cost

    if not can_buy:
        await ctx.channel.send("you dont have enough {0} eggs to buy this".format(settings.object_egg_types[item]))
        return

    emoji = settings.emojis["eggy"]

    if not item.startswith("farm"):
        database.give_inventory_item(authorID, item, 1)
    else:
        database.give_farm_level(authorID, 1)

    if settings.object_egg_types[item] == "":
        database.give_cash(authorID, -cost)
    elif settings.object_egg_types[item] == "silver":
        database.give_iron_cash(authorID, -cost)
        emoji = settings.emojis["silver eggy"]
    elif settings.object_egg_types[item] == "gold":
        database.give_gold_cash(authorID, -cost)
        emoji = settings.emojis["golden eggy"]

    await ctx.channel.send(embed=create_embed("Success", "Successfully bought {0} for {1} {2} {3} eggs"
                                              .format(item, emoji, cost, settings.object_egg_types[item])))


@buy.error
async def buy_error(ctx, error):
    await error_handling(ctx, error, "buy")


@bot.command("sell")
async def sell(ctx, *, item):
    await eggy_check(ctx, False)
    authorID = ctx.author.id

    try:
        item = int(item)
    except ValueError:
        item = item
    if isinstance(item, int):
        item = id_to_object(item)

    if item is None and item not in settings.object_ids:
        await ctx.channel.send("invalid item")
        return

    if not database.has_inventory_item(authorID, item):
        await ctx.channel.send("you dont own this item!")
        return

    return_eggs = int(round((settings.object_costs[item] / 2) + 0.1))
    database.give_inventory_item(authorID, item, -1)

    emoji = settings.emojis["eggy"]

    if settings.object_egg_types[item] == "":
        database.give_cash(authorID, return_eggs)
    elif settings.object_egg_types[item] == "silver":
        database.give_iron_cash(authorID, return_eggs)
        emoji = settings.emojis["silver eggy"]
    elif settings.object_egg_types[item] == "gold":
        database.give_gold_cash(authorID, return_eggs)
        emoji = settings.emojis["golden eggy"]

    await ctx.channel.send(embed=create_embed("Sold!", "Successfully sold the {0} for {1} {2} {3} eggs"
                                              .format(item, emoji, return_eggs, settings.object_egg_types[item])))


class guildButtons(discord.ui.View):

    def __init__(self):
        print("created guild buttons")
        super().__init__(timeout=None)

    @discord.ui.button(label="join valkyrie", style=discord.ButtonStyle.red)
    async def mistake(self, interaction: discord.Interaction, button: discord.ui.Button):
        for guild in settings.guilds:
            r = interaction.guild.get_role(settings.guilds[guild])
            if r in interaction.user.roles:
                await interaction.response.send_message("you are already in a guild!")
                return
        role = interaction.guild.get_role(settings.guilds["valkyrie"])
        api.guildManager.set_guild_join_time(interaction.user.id, 604800)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(embed=create_embed("~~Made a mistake~~ Joined Valkyrie"))

    @discord.ui.button(label="join solstice", style=discord.ButtonStyle.primary)
    async def solstice(self, interaction: discord.Interaction, button: discord.ui.Button):
        for guild in settings.guilds:
            r = interaction.guild.get_role(settings.guilds[guild])
            if r in interaction.user.roles:
                await interaction.response.send_message("you are already in a guild!")
                return
        role = interaction.guild.get_role(settings.guilds["solstice"])
        api.guildManager.set_guild_join_time(interaction.user.id, 604800)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(embed=create_embed("Joined Solstice"))

    @discord.ui.button(label="join nyx", style=discord.ButtonStyle.green)
    async def nyx(self, interaction: discord.Interaction, button: discord.ui.Button):
        for guild in settings.guilds:
            r = interaction.guild.get_role(settings.guilds[guild])
            if r in interaction.user.roles:
                await interaction.response.send_message("you are already in a guild!")
                return
        role = interaction.guild.get_role(settings.guilds["nyx"])
        api.guildManager.set_guild_join_time(interaction.user.id, 604800)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(embed=create_embed("Joined Nyx"))

    @discord.ui.button(label="join zephyr", style=discord.ButtonStyle.gray)
    async def zephyr(self, interaction: discord.Interaction, button: discord.ui.Button):
        for guild in settings.guilds:
            r = interaction.guild.get_role(settings.guilds[guild])
            if r in interaction.user.roles:
                await interaction.response.send_message("you are already in a guild!")
                return
        role = interaction.guild.get_role(settings.guilds["zephyr"])
        api.guildManager.set_guild_join_time(interaction.user.id, 604800)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(embed=create_embed("Joined Zephyr"))


@bot.command("guilds")
async def guilds(ctx):
    if api.guildManager.get_guild(ctx) == "None":
        await ctx.channel.send(embed=create_embed("Guilds",
                                                  "this is a list of all the currently active guilds:\n- valkyrie\n- solstice\n- nyx\n- "
                                                  "zephyr\nif you've made a choice you can use the buttons below:"),
                               view=guildButtons())
        return
    await ctx.channel.send(embed=create_embed("Guilds",
                                              "this is a list of all the currently active guilds:\n- valkyrie\n- solstice\n- nyx\n- "
                                              "zephyr"))


@bot.group()
async def guild(ctx):
    if ctx.invoked_subcommand is not None:
        return

    if api.guildManager.get_guild(ctx) == "None":
        await ctx.channel.send(
            embed=create_embed("error", "you do not have a guild! join one with +guild join or +guilds"))
    else:
        await guilds_profile(ctx, api.guildManager.get_guild(ctx))


@guild.command("profile")
async def guilds_profile(ctx, guild: str = ""):
    if guild == "" or guild not in settings.guilds:
        guild = api.guildManager.get_guild(ctx)

    if guild == "None" or guild == "":
        await ctx.channel.send("guild not found!")
        return

    guild = guild.lower()
    if guild not in settings.guilds:
        await ctx.channel.send("This guild does not exist!")
        return

    member_count = str(len(ctx.guild.get_role(settings.guilds[guild]).members))
    worth = str(api.guildManager.get_guild_worth(guild))
    cash = str(api.guildManager.get_guild_cash(guild))
    ironcash = str(api.guildManager.get_guild_ironcash(guild))
    goldcash = str(api.guildManager.get_guild_goldcash(guild))

    if guild == "zephyr":
        desc = "Total Worth: " + worth + "\n" \
               + settings.emojis["eggy"] + " " + cash + "\n" \
               + settings.emojis["silver eggy"] + " " + ironcash + "\n" \
               + settings.emojis["golden eggy"] + " " + goldcash + "\n" \
                                                                   "Member Count: " + member_count + "\n\n" \
                                                                                                     "Join us at zephyr, where the winds of friendship will grant us victory over all who oppose us. Be it friend or foe, all are welcome at zephyr.\n\n" \
                                                                                                     "We offer assistance in all walks of life. Ofcourse with a little fee for our assistance in interguild affairs. We will share and dwell in the spoils of war, protect justice and fairness across the land, and do so as a team.\n\n" \
                                                                                                     "We believe in freedom and justice and peace. Here at zephyr, we have no enemies... just minor annoying inconveniences.\n\n" \
                                                                                                     "So dont be shy, join us now!"

        emb = create_embed("Zephyr Statistics", desc)
        emb.set_image(url="https://cdn.discordapp.com/attachments/1102274225378693223/1136320199893717082/image.png")

        await ctx.channel.send(embed=emb)
    elif guild == "nyx":
        desc = "Total worth: " + worth + "\n" \
               + settings.emojis["eggy"] + " " + cash + "\n" \
               + settings.emojis["silver eggy"] + " " + ironcash + "\n" \
               + settings.emojis["golden eggy"] + " " + goldcash + "\n" \
                                                                   "Member Count: " + member_count + "\n\n" \
                                                                                                     "Be it to bomb people in brawlhalla or throw bombs as klee at timmies pigeons, it's fun right.\n\n" \
                                                                                                     "Be prepared to actually have good teammates and not rage over team diff." \
                                                                                                     "Be it garticphone or other minigames i can carry and train us to be a strong reliable guild.\n\n" \
                                                                                                     "A thing only my guild can provide is also good advices and emotional support as bonus! And even of you don't have a talen for minigames i can train you to be a pro.\n\n" \
                                                                                                     "_We shall be victorious with the help of chaos and our ability to hide in the shadows to attack in the night_"

        emb = create_embed("Nyx Statistics", desc)
        emb.set_image(
            url="https://cdn.discordapp.com/attachments/1132334113416826880/1134923290557808760/a3443518535_10.jpg")

        await ctx.channel.send(embed=emb)
    elif guild == "solstice":
        desc = "Total worth: " + worth + "\n" \
               + settings.emojis["eggy"] + " " + cash + "\n" \
               + settings.emojis["silver eggy"] + " " + ironcash + "\n" \
               + settings.emojis["golden eggy"] + " " + goldcash + "\n" \
                                                                   "Member Count: " + member_count + "\n\n" \
                                                                                                     "Embrace the harmony of the duality of the elements!\n" \
                                                                                                     "Whether that be on a winning hot streak or to show of your cool skills to the crowd, Solstice is the place to be.\n\n" \
                                                                                                     "Come dusk or dawn, you will be the ray of sunlight the world needs (and to outshine your enemies)\n\n" \
                                                                                                     "_Illuminating your path to greatness_"

        emb = create_embed("Solstice Statistics", desc)
        emb.set_image(url="https://cdn.discordapp.com/attachments/1132334113416826880/1135234083534929920/IMG_2649.png")

        await ctx.channel.send(embed=emb)
    elif guild == "valkyrie":
        desc = "Total worth: " + worth + "\n" \
               + settings.emojis["eggy"] + " " + cash + "\n" \
               + settings.emojis["silver eggy"] + " " + ironcash + "\n" \
               + settings.emojis["golden eggy"] + " " + goldcash + "\n" \
                                                                   "Member Count: " + member_count + "\n\n" \
                                                                                                     "Want to join a friendly yet competitive clan? Want to perhaps, win with pride? Sick and tired of leaders saying it all them? Not respecting your existence? Want to have, a getaway?\n\n" \
                                                                                                     "Well my friend, let me introduce you to Valkyrie\n\n" \
                                                                                                     "Composed of many talented members, we together rise up against tyranny. Like eagles, fight day or night, we will still reign king. Join the action, join the pact. Spread the words, spread your wings.\n\n" \
                                                                                                     "Why wait? Join us now!\n\n" \
                                                                                                     "_Puganums, Vincimus, Regnamus. \nWe fight, we win, we reign._"

        emb = create_embed("Valkyrie Statistics", desc)
        emb.set_image(url="https://cdn.discordapp.com/attachments/1102274225378693223/1136320294672420914/image.png")

        await ctx.channel.send(embed=emb)


@guild.command("deposit")
async def deposit(ctx, amount: int = 0, what: str = "eggs"):
    if api.guildManager.get_guild(ctx) == "None":
        await ctx.channel.send("you do not have a guild!")
        return

    if amount <= 0:
        await ctx.channel.send("you cant deposit this amount!")
        return

    authorID = ctx.author.id

    normal = ["eggs", "eggys", "egg", "eggy"]
    silver = ["silver eggs", "silver_eggs", "silver eggys", "silver_eggy", "silver_egg"]
    gold = ["gold eggs", "gold_eggs", "gold eggys", "gold_eggy", "gold_egg", "golden eggs", "golden_eggs",
            "golden eggys", "goldeb_eggy", "goldeb_egg"]

    guild = api.guildManager.get_guild(ctx)

    if what in normal:
        if database.get_cash(authorID) < amount:
            await ctx.channel.send("you cant afford to deposit this amount!")
        else:
            database.give_cash(authorID, -amount)
            api.guildManager.add_cash(guild, amount)
            await ctx.channel.send("deposited " + str(amount) + " eggs into the guild bank")
    elif what in silver:
        if database.get_iron_cash(authorID) < amount:
            await ctx.channel.send("you cant afford to deposit this amount!")
        else:
            database.give_iron_cash(authorID, -amount)
            api.guildManager.add_ironcash(guild, amount)
            await ctx.channel.send("deposited " + str(amount) + " silver eggs into the guild bank")
    elif what in gold:
        if database.get_gold_cash(authorID) < amount:
            await ctx.channel.send("you cant afford to deposit this amount!")
            return
        else:
            database.give_gold_cash(authorID, -amount)
            api.guildManager.add_goldcash(guild, amount)
            await ctx.channel.send("deposited " + str(amount) + " golden eggs into the guild bank")
    else:
        await ctx.channel.send("invalid egg type!")
        return


@guild.command("withdraw")
async def withdraw(ctx, amount: int = 0, what: str = "eggs"):
    guild = api.guildManager.get_guild(ctx)
    if guild == "None":
        await ctx.channel.send("you do not have a guild!")
        return

    authorID = ctx.author.id

    if not api.guildManager.has_perms(authorID, guild) and not api.guildManager.is_guild_master(ctx):
        await ctx.channel.send("you do not have permissions to withdraw from the guild bank!")
        return

    normal = ["eggs", "eggys", "egg", "eggy"]
    silver = ["silver eggs", "silver_eggs", "silver eggys", "silver_eggy", "silver_egg"]
    gold = ["gold eggs", "gold_eggs", "gold eggys", "gold_eggy", "gold_egg", "golden eggs", "golden_eggs",
            "golden eggys", "goldeb_eggy", "goldeb_egg"]

    if what in normal:
        if api.guildManager.get_guild_cash(guild) < amount:
            await ctx.channel.send("there are not enough eggs in the guild bank to withdraw this much!")
        else:
            database.give_cash(authorID, amount)
            api.guildManager.add_cash(guild, -amount)
            await ctx.channel.send("withdrew " + str(amount) + " eggs from the guild bank")
    elif what in silver:
        if api.guildManager.get_guild_ironcash(guild) < amount:
            await ctx.channel.send("there are not enough silver eggs in the guild bank to withdraw this much!")
        else:
            database.give_iron_cash(authorID, amount)
            api.guildManager.add_ironcash(guild, -amount)
            await ctx.channel.send("withdrew " + str(amount) + " silver eggs from the guild bank")
    elif what in gold:
        if api.guildManager.get_guild_goldcash(guild) < amount:
            await ctx.channel.send("there are not enough golden eggs in the guild bank to withdraw this much!")
        else:
            database.give_gold_cash(authorID, amount)
            api.guildManager.add_goldcash(guild, -amount)
            await ctx.channel.send("withdrew " + str(amount) + " golden eggs from the guild bank")
    else:
        await ctx.channel.send("invalid egg type!")
        return


@guild.command("join")
async def guilds_join(ctx, guild: str = ""):
    if api.guildManager.get_guild(ctx) != "None":
        await ctx.channel.send("you already have a guild!")
        return
    if api.guildManager.get_guild_join_time(ctx.author.id) != 0:
        await ctx.channel.send("you cannot join another guild yet! you have `" + api.guildManager.guild_join_time_left(
            ctx.author.id) + "` until you can join a guild again")
        return
    if guild == "" or guild not in settings.guilds:
        await ctx.channel.send("what guild would u like to join", view=guildButtons())
        return

    role = ctx.guild.get_role(settings.guilds[guild])
    api.guildManager.set_guild_join_time(ctx.author.id, 604800)
    await ctx.author.add_roles(role)
    await ctx.channel.send(embed=create_embed("Joined", "Joined " + guild))


@guild.command("leave")
async def guilds_leave(ctx):
    if api.guildManager.get_guild(ctx) == "None":
        await ctx.channel.send("you dont have a guild!")
        return

    for guild in settings.guilds:
        id = settings.guilds[guild]
        role = ctx.guild.get_role(id)
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(embed=create_embed("Left", "Left " + guild))
            return

    await ctx.channel.send("woops something went wrong")


@guild.group(name="perms")
async def guild_perms(ctx):
    if ctx.invoked_subcommand is None:
        if api.guildManager.is_guild_master(ctx):
            await ctx.channel.send(embed=create_embed("add or remove?",
                                                      "you can add or remove permissions using +guilds perms add or +guilds perms remove"))
        else:
            await ctx.channel.send("only the guild master can do this")


@guild.command("test")
async def guilds_test(ctx):
    await ctx.channel.send(view=guildButtons())


@guild_perms.command("add")
async def guild_perms_add(ctx, who: discord.Member):
    if not api.guildManager.is_guild_master(ctx):
        await ctx.channel.send("only the guild master can do this")
        return

    if api.guildManager.has_perms(who.id, api.guildManager.get_guild(ctx)):
        await ctx.channel.send("this user already has guild permissions!")
        return

    api.guildManager.give_perms(who.id, api.guildManager.get_guild(ctx))

    await ctx.channel.send("successfully gave guild permissions!")


@guild_perms.command("remove")
async def guild_perms_remove(ctx, who: discord.Member):
    if not api.guildManager.is_guild_master(ctx):
        await ctx.channel.send("only the guild master can do this")
        return

    if not api.guildManager.has_perms(who.id, api.guildManager.get_guild(ctx)):
        await ctx.channel.send("this user does not have guild permissions!")
        return

    api.guildManager.remove_perms(who.id, api.guildManager.get_guild(ctx))

    await ctx.channel.send("successfully removed guild permissions!")


@guild_perms.command("check")
async def guild_perms_check(ctx):
    if api.guildManager.get_guild(ctx) == "None":
        await ctx.channel.send("you are not in a guild!")
        return
    if api.guildManager.has_perms(ctx.author.id, api.guildManager.get_guild(ctx)):
        await ctx.channel.send("you have perms")
    else:
        await ctx.channel.send("you dont have perms")


@guild.command("leaderboard")
async def leaderboard(ctx):
    board = api.guildManager.get_guild_leaderboard()
    num1, value1 = board[0], api.guildManager.get_guild_worth(board[0])
    num2, value2 = board[1], api.guildManager.get_guild_worth(board[1])
    num3, value3 = board[2], api.guildManager.get_guild_worth(board[2])
    num4, value4 = board[3], api.guildManager.get_guild_worth(board[3])

    desc = "This is the current guild leaderboard:\n" \
           "1. " + str(num1) + " (worth " + str(value1) + ")\n" \
                                                          "2. " + str(num2) + " (worth " + str(value2) + ")\n" \
                                                                                                         "3. " + str(
        num3) + " (worth " + str(value3) + ")\n" \
                                           "4. " + str(num4) + " (worth " + str(value4) + ")\n"

    await ctx.channel.send(embed=create_embed("Guild Leaderboard", desc))


@bot.command("pay", aliases=["give"])
@commands.has_role(settings.staff_role)
async def pay(ctx, target: discord.Member, amount: int, what):
    targetID = target.id
    if ctx.author == target:
        await ctx.channel.send("you cant give yourself shit")
        return
    if what == "egg" or what == "eggs":
        database.give_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully paid {3} {0} {1} to {2}".format(amount, settings.cash_name, target,
                                                                      settings.emojis["eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "segg" or what == "silveregg" or what == "silvereggs":
        database.give_iron_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully payed {3} {0} {1} to {2}".format(amount, settings.iron_cash_name, target,
                                                                       settings.emojis["silver eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "gegg" or what == "goldegg" or what == "goldeggs" or what == "goldenegg" or what == "goldeneggs":
        database.give_gold_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully payed {3} {0} {1} to {2}".format(amount, settings.gold_cash_name, target,
                                                                       settings.emojis["golden eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "eggyolk" or what == "eggyolks" or what == "yolk" or what == "yolks":
        database.give_eggyolks(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully payed {3} {0} {1} to {2}".format(amount, settings.yolk_cash_name, target,
                                                                       settings.emojis["eggyolk"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))
    else:
        await ctx.channel.send("there is no object with that name")


@pay.error
async def pay_error(ctx, error):
    await error_handling(ctx, error, "pay")


@bot.command("inventory", aliases=["inv", "wares", "i"])
async def inventory(ctx, person: discord.Member = None):
    if person is None:
        person = ctx.author
    authorID = person.id
    if database.is_inventory_empty(authorID):
        emb = discord.Embed(
            title="{0}'s warehouse".format(person.name),
            description="your inventory is currently empty!"
        )

        await ctx.channel.send(embed=emb)
    else:
        emb = discord.Embed(
            title="{0}'s warehouse".format(person.name)
        )

        if authorID == 802159357306470430:
            emb.add_field(name="unlucky", value="you are just very unlucky")

        """
        if database.has_inventory_item(authorID, "binoculars"):
            emb.add_field(name="Binoculars", value="You have the binoculars", inline=True)
        if database.has_inventory_item(authorID, "lucky drumstick"):
            emb.add_field(name="Lucky Drumstick", value="You have the lucky drumstick", inline=True)
        if database.has_inventory_item(authorID, "golden_chicken"):
            emb.add_field(name="Golden Chicken", value="You have the golden chicken")
        if egg_topper == 1:
            emb.add_field(name="Egg Topper", value="You have a egg topper")
        elif egg_topper >= 2:
            emb.add_field(name="Egg Topper", value="You have {0} egg toppers".format(egg_topper))
        if database.has_inventory_item(authorID, "delicate_shovel"):
            emb.add_field(name="Delicate Shovel", value="You have the delicate shovel")
        if database.has_inventory_item(authorID, "golden_shovel"):
            emb.add_field(name="Golden Shovel", value="You have the golden shovel")
        if statue == 1:
            emb.add_field(name="Eggcellent Statue", value="You have a eggcellent statue")
        elif statue >= 2:
            emb.add_field(name="Eggcellent Statue", value="You have {0} eggcellent statues".format(statue))
        """

        items = database.get_inventory_items(authorID)

        singles = []
        duplicates = {}

        for item in items.keys():
            amount = items[item]
            if amount == 1:
                singles.append(item)
            else:
                duplicates[item] = amount

        for sitem in singles:
            sitem = sitem.replace("_", " ")
            emb.add_field(name=sitem, value="You have a " + sitem)

        for ditem in duplicates.keys():
            amount = duplicates[ditem]
            ditem = ditem.replace("_", " ")
            emb.add_field(name=ditem, value="You have " + str(amount) + " " + ditem + "s")

        await ctx.channel.send(embed=emb)


@bot.command("profile", aliases=["prof"])
async def profile(ctx, who: discord.Member = None):
    await eggy_check(ctx, False)
    if who is None:
        who = ctx.author
    authorID = who.id
    emb = discord.Embed(
        title=""
    )

    emb.add_field(name="{0}Farm Level".format(settings.emojis["farm"]),
                  value="You are currently farm level {0}".format(database.get_farm_level(authorID)),
                  inline=False)

    emb.add_field(name="Basket",
                  value="You currently have:" + "\n" +
                        "{2} {0} {1}".format(database.get_cash(authorID), settings.cash_name,
                                             settings.emojis["eggy"]) + "\n" +
                        "{2} {0} {1}".format(database.get_iron_cash(authorID), settings.iron_cash_name,
                                             settings.emojis["silver eggy"]) + "\n" +
                        "{2} {0} {1}".format(database.get_gold_cash(authorID), settings.gold_cash_name,
                                             settings.emojis["golden eggy"]) + "\n" +
                        "{2} {0} {1}".format(database.get_eggyolks(authorID), settings.yolk_cash_name,
                                             settings.emojis["eggyolk"]),
                  inline=False)

    if authorID == bot.author_id:
        emb.set_author(name="god's profile", url=None, icon_url=ctx.author.avatar)
    else:
        emb.set_author(name="{0}'s profile".format(ctx.author.name), url=None, icon_url=ctx.author.avatar)

    boost_desc = ""

    for boost in api.boostManager.get_active_boosts(authorID):
        boost_desc = boost_desc + boost + " `" + api.boostManager.boost_time_left(authorID, boost) + "`\n"

    if boost_desc != "":
        emb.add_field(name="Active boosts", value=boost_desc, inline=False)
    else:
        emb.add_field(name="Active boosts", value="you have no active boosts!", inline=False)

    await ctx.channel.send(embed=emb)


@bot.command("nick", aliases=["yoink", "take"])
@commands.has_role(settings.staff_role)
async def nick(ctx, target: discord.Member, amount: int, what):
    targetID = target.id
    amount = -amount
    if what == "egg" or what == "eggs":
        database.give_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully nicked {3} {0} {1} from {2}".format(amount, settings.cash_name, target,
                                                                          settings.emojis["eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "segg" or what == "silveregg" or what == "silvereggs":
        database.give_iron_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully nicked {3} {0} {1} from {2}".format(amount, settings.iron_cash_name, target,
                                                                          settings.emojis["silver eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "gegg" or what == "goldegg" or what == "goldeggs" or what == "goldenegg" or what == "goldeneggs":
        database.give_gold_cash(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully nicked {3} {0} {1} from {2}".format(amount, settings.gold_cash_name, target,
                                                                          settings.emojis["golden eggy"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))

        await ctx.channel.send(embed=emb)
    elif what == "eggyolk" or what == "eggyolks" or what == "yolk" or what == "yolks":
        database.give_eggyolks(targetID, amount)
        emb = discord.Embed(
            title="success",
            description="successfully nicked {3} {0} {1} from {2}".format(amount, settings.yolk_cash_name, target,
                                                                          settings.emojis["eggyolk"])
        )

        emb.set_author(name="Egg Basket",
                       icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")
        emb.set_footer(text=str(date.today()))
    else:
        await ctx.channel.send("there is no object with that name")


@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("you do not have permission to do this!")
    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ConversionError):
        await ctx.channel.send("invalid arguments! {0}nick (target) (amount)".format(settings.bot_prefix))


@bot.command("hunt", aliases=["search", "hu"])
@commands.cooldown(1, settings.hunt_cooldown, commands.BucketType.user)
async def hunt(ctx):
    await eggy_check(ctx, False)
    rolled = random.randint(1, 100)
    if rolled <= settings.hunt_chance:
        rolled_place = settings.hunt_locations[random.randint(0, (len(settings.hunt_locations) - 1))]
        rolled_eggs = 0
        flevel = database.get_farm_level(ctx.author.id)
        if flevel == 1:
            rolled_eggs = random.randint(settings.level_1_farm_min, settings.level_1_farm_max)
        elif flevel == 2:
            rolled_eggs = random.randint(settings.level_2_farm_min, settings.level_2_farm_max)
        elif flevel == 3:
            rolled_eggs = random.randint(settings.level_3_farm_min, settings.level_3_farm_max)
        elif flevel == 4:
            rolled_eggs = random.randint(settings.level_4_farm_min, settings.level_4_farm_max)
        elif flevel == 5:
            rolled_eggs = random.randint(settings.level_5_farm_min, settings.level_5_farm_max)

        #        if database.has_inventory_item(ctx.author.id, "binoculars"):
        #            rolled_eggs = rolled_eggs * 2

        if database.has_boost_active(ctx.author.id, "binoculars"):
            rolled_eggs = rolled_eggs * 2

        database.give_cash(ctx.author.id, rolled_eggs)

        emb = discord.Embed(
            title="Found some {0}".format(settings.cash_name),
            description="You found {0} {3} {1} {2}".format(rolled_eggs, settings.cash_name, rolled_place,
                                                           settings.emojis["eggy"])
        )

        await ctx.send(embed=emb)
    else:
        await ctx.channel.send("you didn't find any eggs")


@hunt.error
async def hunt_error(ctx, error):
    await error_handling(ctx, error, "hunt")


@bot.command("dupe", aliases=["duplicate"])
async def dupe(ctx, amount: str | int = 1):
    await eggy_check(ctx, False)
    max_eggs = 25 + (25 * database.get_farm_level(ctx.author.id))
    if amount == "all" or amount == "max":
        amount = database.get_cash(ctx.author.id)
        if amount > max_eggs:
            amount = max_eggs
    else:
        try:
            amount = int(amount)
        except ValueError:
            await ctx.channel.send("invalid arguments! {0}dupe (amount)".format(settings.bot_prefix))
            return
    if amount > max_eggs:
        await ctx.channel.send("you cant duplicate so many eggs theres a max of {0}".format(max_eggs))
        return
    authorID = ctx.author.id
    amount = int(amount)
    if not database.get_cash(authorID) >= amount:
        await ctx.channel.send("you dont have enough eggs")
        return
    rolled = random.randint(1, 100)
    if rolled <= settings.dupe_chance:
        #        if database.has_inventory_item(authorID, "jackpot"):
        #            amount = int(round(amount * 1.5))

        if database.has_boost_active(authorID, "jackpot"):
            amount = int(round(amount * 1.5))

        database.give_cash(authorID, amount)
        await ctx.channel.send("you successfully duplicated {0} {1}".format(amount, settings.cash_name))
    else:
        database.give_cash(authorID, -amount)
        await ctx.channel.send("oops you dropped the eggs on your way to the machine")


@bot.command("crack", aliases=["cr"])
@commands.cooldown(1, 2, commands.BucketType.user)
async def crack(ctx):
    authorID = ctx.author.id
    if database.has_inventory_item(authorID, "egg_topper"):
        rolled = random.randint(1, 100)
        if rolled <= 50:
            rolled = random.randint(1, 100)
            if rolled <= 25:
                database.give_eggyolks(authorID, 2)
                await ctx.channel.send("you found 2 egg yolks inside the egg but the egg topper broke")
            else:
                database.give_eggyolks(authorID, 1)
                await ctx.channel.send("you found 1 egg yolk inside the egg but the egg topper broke")
        else:
            await ctx.channel.send("you broke the egg and the egg topper")
        database.remove_inventory_item(authorID, "egg topper", 1)
        database.give_cash(authorID, -1)
    else:
        await ctx.channel.send("you need the egg topper to use this command!")


@bot.command("dig")
@commands.cooldown(1, settings.dig_cooldown, commands.BucketType.user)
async def dig(ctx):
    authorID = ctx.author.id
    if database.has_inventory_item(authorID, "delicate_shovel") or database.has_inventory_item(authorID,
                                                                                               "golden_shovel"):
        flevel = database.get_farm_level(authorID)
        rolled = 0
        if flevel == 1:
            rolled = random.randint(settings.level_1_farm_min - 1, settings.level_1_farm_max - 1)
        elif flevel == 2:
            rolled = random.randint(settings.level_2_farm_min - 1, settings.level_2_farm_max - 1)
        elif flevel == 3:
            rolled = random.randint(settings.level_3_farm_min - 1, settings.level_3_farm_max - 1)
        elif flevel == 4:
            rolled = random.randint(settings.level_4_farm_min - 1, settings.level_4_farm_max - 1)
        elif flevel == 5:
            rolled = random.randint(settings.level_5_farm_min - 1, settings.level_5_farm_max - 1)

        if rolled <= 0:
            await ctx.channel.send("you broke the eggs while digging them up")
            return

        if database.has_inventory_item(authorID, "golden_shovel"):
            rolled = round(rolled * 1.5)

        database.give_cash(authorID, rolled)
        await ctx.channel.send("you dug up {0} eggs".format(rolled))
    else:
        await ctx.channel.send("you dont own a shovel")


@bot.command("explore", aliases=["ex"])
@commands.cooldown(1, settings.explore_cooldown, commands.BucketType.user)
async def explore(ctx):
    await eggy_check(ctx, False)
    flevel = database.get_farm_level(ctx.author.id)
    rolled = 0
    location = settings.explore_locations[random.randint(1, len(settings.explore_locations))]
    if flevel == 1:
        rolled = random.randint(settings.level_1_explore_min, settings.level_1_explore_max)
    elif flevel == 2:
        rolled = random.randint(settings.level_2_explore_min, settings.level_2_explore_max)
    elif flevel == 3:
        rolled = random.randint(settings.level_3_explore_min, settings.level_3_explore_max)
    elif flevel == 4:
        rolled = random.randint(settings.level_4_explore_min, settings.level_4_explore_max)
    elif flevel == 5:
        rolled = random.randint(settings.level_5_explore_min, settings.level_5_explore_max)

    database.give_cash(ctx.author.id, rolled)

    if rolled <= -1:
        emb = discord.Embed(
            title="oops",
            description="oops you dropped {0} eggs while exploring".format((-rolled))
        )
    elif rolled == 0:
        emb = discord.Embed(
            title="tough luck",
            description="you didn't find any eggs"
        )
    else:
        emb = discord.Embed(
            title="success",
            description="you found {0} eggs {1}".format(rolled, location)
        )

    await ctx.channel.send(embed=emb)


@explore.error
async def explore_error(ctx, error):
    await error_handling(ctx, error, "explore")


@bot.command("bargain", aliases=["ba"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def bargain(ctx, amount: int):
    await eggy_check(ctx, False)
    rolled = random.randint(1, 2)
    authorID = ctx.author.id

    flevel = database.get_farm_level(authorID)

    if flevel == 1 and amount > settings.level_1_bargain_max:
        await ctx.channel.send(embed=create_embed("nothing", "you can only bargain {0} eggs at a time"
                                                  .format(settings.level_1_bargain_max)))
        return
    elif flevel == 2 and amount > settings.level_2_bargain_max:
        await ctx.channel.send(embed=create_embed("nothing", "you can only bargain {0} eggs at a time"
                                                  .format(settings.level_2_bargain_max)))
        return
    elif flevel == 3 and amount > settings.level_3_bargain_max:
        await ctx.channel.send(embed=create_embed("nothing", "you can only bargain {0} eggs at a time"
                                                  .format(settings.level_3_bargain_max)))
        return
    elif flevel == 4 and amount > settings.level_4_bargain_max:
        await ctx.channel.send(embed=create_embed("nothing", "you can only bargain {0} eggs at a time"
                                                  .format(settings.level_4_bargain_max)))
        return
    elif flevel == 5 and amount > settings.level_5_bargain_max:
        await ctx.channel.send(embed=create_embed("nothing", "you can only bargain {0} eggs at a time"
                                                  .format(settings.level_5_bargain_max)))
        return

    eggs_min = 0
    eggs_max = 0

    if amount <= 10:
        eggs_min = amount - 5
        eggs_max = amount + 5
    elif 10 < amount <= 50:
        eggs_min = amount - 10
        eggs_max = amount + 10
    elif 50 < amount <= 100:
        eggs_min = amount - 20
        eggs_max = amount + 20
    elif 100 < amount <= 150:
        eggs_min = amount - 40
        eggs_max = amount + 40
    elif 150 < amount <= 200:
        eggs_min = amount - 50
        eggs_max = amount + 50
    elif 200 < amount <= 250:
        eggs_min = amount - 75
        eggs_max = amount + 75
    elif 250 < amount:
        eggs_min = amount - 100
        eggs_max = amount + 100

    if database.get_cash(authorID) < amount:
        await ctx.channel.send(embed=create_embed("nothing", "you don't have enough eggs to bargain"))
    elif rolled == 1:
        await ctx.channel.send(embed=create_embed("nothing", "you haven't gained or lost anything from your bargain"))
    elif rolled == 2:
        profit = random.randint(eggs_min, eggs_max)
        if profit == amount:
            await ctx.channel.send(embed=create_embed("nothing", "you didn't manage to bargain for your eggs"))
        elif profit > amount:
            #            if database.has_inventory_item(authorID, "jackpot"):
            #                profit = int(round(profit * 1.5))

            if database.has_inventory_item(authorID, "jackpot"):
                profit = int(round(profit * 1.5, 0))

            await ctx.channel.send(embed=create_embed("profit",
                                                      f"you bargained your {amount} eggs for {profit} eggs"
                                                      f" (you got {(profit - amount)} eggs)"))
            database.give_cash(authorID, (profit - amount))
        elif profit < amount:
            await ctx.channel.send(embed=create_embed("loss",
                                                      f"you bargained your {amount} eggs for {profit} eggs"
                                                      f" (you lost {(amount - profit)} eggs)"))
            database.give_cash(authorID, (amount - profit))


@bargain.error
async def bargain_error(ctx, error):
    await error_handling(ctx, error, "bargain")


@bot.command("use", aliases=["use_boost"])
async def use(ctx, boost):
    await eggy_check(ctx, False)
    authorID = ctx.author.id

    if not database.has_inventory_item(authorID, boost):
        await ctx.channel.send("you do not own this boost!")
        return

    if settings.object_types[boost] is None:
        await ctx.channel.send("this boost does not exist!")
        return

    if settings.object_types[boost] != "boost":
        await ctx.channel.send("this item is not a boost!")
        return

    database.activate_boost(authorID, boost)

    emb = create_embed("boosted", "activated your " + boost + "!\nit will last for 2 hours")

    await ctx.channel.send(embed=emb)


async def error_handling(ctx, error, command):
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingRole):
        await ctx.channel.send("https://tenor.com/view/no-nope-non-rick-rick-and-morty-gif-20999440")
    elif isinstance(error, commands.MissingRequiredArgument):
        if command == "announce":
            await ctx.channel.send(
                "missing required argument! {0}announce (title)|(announcement)|(?banner). yes the '|' is neccesary".format(
                    settings.bot_prefix))
        elif command == "transfer":
            await ctx.channel.send("missing required argument! {0}share (target) (amount)".format(settings.bot_prefix))
        elif command == "buy":
            await ctx.channel.send("missing required argument! {0}buy (item)".format(settings.bot_prefix))
        elif command == "pay":
            await ctx.channel.send(
                "missing required argument! {0}pay (target) (amount) (what)".format(settings.bot_prefix))
        elif command == "bargain":
            await ctx.channel.send("missing required argument! {0}bargain (amount)".format(settings.bot_prefix))
    elif isinstance(error, commands.ConversionError):
        if command == "transfer":
            await ctx.channel.send("invalid arguments! {0}share (target) (amount)".format(settings.bot_prefix))
        elif command == "pay":
            await ctx.channel.send("invalid arguments! {0}pay (target) (amount)".format(settings.bot_prefix))
        elif command == "dupe":
            await ctx.channel.send("invalid arguments! {0}dupe (amount)".format(settings.bot_prefix))
        elif command == "bargain":
            await ctx.channel.send("invalid arguments! {0}bargain (amount)".format(settings.bot_prefix))
    elif isinstance(error, commands.CommandOnCooldown):
        if command == "harvest":
            await ctx.channel.send(
                f"The eggs arent ready to harvest. you should check again in {error.retry_after:.0f} seconds.")
        elif command == "hunt":
            await ctx.channel.send(
                f"you just went searching you should get some rest and go again in {error.retry_after:.0f} seconds.")
        elif command == "dupe":
            await ctx.channel.send(
                f"the machine is still charging it should be done in {error.retry_after:.0f} seconds.")
        elif command == "dig" or command == "explore":
            await ctx.channel.send(f"you are still resting you can go again in {error.retry_after:.0f} seconds.")
        elif command == "bargain":
            await ctx.channel.send(f"you just went bargaining you can go again in {error.retry_after:.0f} seconds.")


async def eggy_check(ctx, chatted: bool):
    authorID = ctx.author.id
    flevel = database.get_farm_level(authorID)
    if flevel >= 2:
        has_a_chance = (random.randint(1, 4) == 1)
        if has_a_chance:
            silver = (random.randint(1, 2) == 1)
            rolled = random.randint(1, 100)
            #            if database.has_inventory_item(authorID, "lucky_drumstick"):
            #                rolled *= 1.5
            #                if rolled > 100:
            #                    rolled = 100

            if database.has_boost_active(authorID, "lucky_drumstick"):
                rolled *= 1.5
                if rolled > 100:
                    rolled = 100

            silver_chance = 20 + (20 * (flevel - 2))
            silver_double_chance = 10 + (10 * (flevel - 2))
            gold_chance = 25 + (25 * (flevel - 3))
            can_get_gold = False
            if chatted == False and gold_chance <= rolled:
                can_get_gold = True
            elif chatted == True and gold_chance <= rolled and flevel == 5:
                can_get_gold = True

            if silver and silver_chance <= rolled:
                amount_of_eggs = 1
                if silver_double_chance <= random.randint(1, 100):
                    amount_of_eggs = 2

                emb = create_embed("you found a silver egg", "you found {2} {0} {1}"
                                   .format(amount_of_eggs, settings.iron_cash_name, settings.emojis["silver eggy"]))
                database.give_iron_cash(authorID, amount_of_eggs)
                await ctx.channel.send(embed=emb)
            elif can_get_gold:
                emb = create_embed("you found a gold egg", "you found {1} 1 {0}"
                                   .format(settings.gold_cash_name, settings.emojis["golden eggy"]))
                database.give_gold_cash(authorID, 1)
                await ctx.channel.send(embed=emb)


@bot.command("test_emojis")
@commands.has_role(863434428570796043)
async def test_emojis(ctx):
    await ctx.channel.send(settings.emojis["farm"]
                           + "," + settings.emojis["eggy"]
                           + "," + settings.emojis["eggyolk"]
                           + "," + settings.emojis["golden eggy"]
                           + "," + settings.emojis["silver eggy"]
                           + "," + settings.emojis["binoculars"]
                           + "," + settings.emojis["golden chicken"]
                           + "," + settings.emojis["lucky drumstick"]
                           + "," + settings.emojis["delicate shovel"]
                           + "," + settings.emojis["egg topper"]
                           )
    time.sleep(2.5)
    await ctx.channel.purge(limit=2)


@test_emojis.error
async def test_emojis_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("https://tenor.com/view/no-nope-non-rick-rick-and-morty-gif-20999440")


def create_embed(title: str | None, description: str = "") -> discord.Embed:
    return discord.Embed(
        title=title, description=description
    )


def id_to_object(obj_id: int) -> str | None:
    for value in settings.object_ids:
        if settings.object_ids[value] == obj_id:
            return value

    return None


def object_to_id(obj: str) -> int | None:
    return settings.object_ids[obj]


def backup_database():
    if os.path.exists("main.sqlite"):
        now = str(date.today()) + "_" + str(datetime.now())
        now = now.replace(":", "_")

        target_dir = "./backups"
        src_file = "./main.sqlite"
        dst_file = target_dir + "/" + now + "_backup_main.sqlite"
        dst_file = dst_file.replace(" ", "_").replace("-", "_")
        shutil.copy(src_file, dst_file)


token = None

if not os.path.exists("./backups"):
    os.mkdir("./backups")

if os.path.exists("./token.txt"):
    with open("./token.txt", "r") as f:
        lines = f.readlines()
        token = lines[0]
        print("loaded token from token.txt")
else:
    token = os.environ['TOKEN']

if token is None:
    print("no token!")
else:
    backup_database()

    keep_alive()
    threading.Thread(target=api.boostManager.start).start()
    threading.Thread(target=api.guildManager.start).start()

    api.guildManager.setup_guilds()
    bot.run(token)  # Starts the bot

    print("attempting shutdown (may take up to a few minutes due to threads)")

    api.boostManager.kill_threads = True
    api.guildManager.kill_threads = True
