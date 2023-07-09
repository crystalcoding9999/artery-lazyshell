import os
import random
import time
from datetime import date, datetime
import shutil

import discord
from discord.ext import commands

import settings
from api import Database
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
guild: discord.Guild = None


@bot.event
async def on_ready():  # When the bot is ready
    global guild
    guild = bot.get_guild(settings.guild_id)
    print("logged in as {0.user}".format(bot))


@bot.event
async def on_signal(signal):
    if signal == "SIGINT":
        print("Received SIGINT signal. Exiting gracefully...")
        await send_farewell()


async def send_farewell():
    channel = guild.get_channel(settings.bot_channel)
    emb = discord.Embed(
        title="cya",
        description="aight imma head out",
        colour=discord.Color.red()
    )

    await channel.send(embed=emb)
    await bot.close()


@bot.event
async def on_message(ctx):
    if not ctx.channel.id == 842522103315169320:
        await eggy_check(ctx, True)

    if isinstance(ctx.channel, discord.Thread):
        if ctx.author.id == 235148962103951360 and ctx.channel.id == 1122532250915975208:
            await ctx.delete()

    await bot.process_commands(ctx)


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
                                                                              settings.eggy_emoji)
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
                                                                              settings.silver_eggy_emoji)
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
                                                                              settings.golden_eggy_emoji)
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

    if database.has_inventory_item(authorID, "golden_chicken"):
        earned *= 1.5
        earned = int(round(earned, 0))

    emb = discord.Embed(
        description="successfully harvested {2} {0} {1}".format(earned, settings.cash_name, settings.eggy_emoji)
    )

    emb.set_author(name="Egg Basket",
                   icon_url="https://cdn.discordapp.com/attachments/1121483496435753100/1121876394905981069/download__2_-removebg-preview.png")

    database.give_cash(authorID, earned)
    await ctx.channel.send(embed=emb)


@harvest.error
async def harvest_error(ctx, error):
    await error_handling(ctx, error, "harvest")


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
                                                                                            settings.farm_emoji, )
        else:
            fl_desc = "{0}**Farm Upgrade**:\nYou already have the max level farm!".format(settings.farm_emoji)

        if not database.has_inventory_item(authorID, "binoculars"):
            bin_desc = "{2}**Binoculars**: {0} {1}\n{3}".format(settings.binocular_cost,
                                                                settings.silver_eggy_emoji,
                                                                settings.binoculars_emoji,
                                                                settings.object_descs["binoculars"])
        else:
            bin_desc = "{2}**Binoculars** (**owned**): {0} {1}\n{3}".format(
                settings.binocular_cost,
                settings.silver_eggy_emoji,
                settings.binoculars_emoji,
                settings.object_descs["binoculars"])

        if not database.has_inventory_item(authorID, "lucky_drumstick"):
            ld_desc = "{2}**Lucky Drumstick**: {1} {0}\n{3}".format(
                settings.silver_eggy_emoji,
                settings.lucky_drumstick_cost,
                settings.drumstick_emoji,
                settings.object_descs["lucky drumstick"])
        else:
            ld_desc = "{2}**Lucky Drumstick** (**owned**): {1} {0}\n{3}".format(
                settings.silver_eggy_emoji,
                settings.lucky_drumstick_cost,
                settings.drumstick_emoji,
                settings.object_descs["lucky drumstick"])

        if not database.has_inventory_item(authorID, "golden_chicken"):
            gc_desc = "{2}**Golden Chicken**: {1} {0}\n{3}".format(
                settings.silver_eggy_emoji,
                settings.golden_chicken_cost,
                settings.chicken_emoji,
                settings.object_descs["golden chicken"])
        else:
            gc_desc = "{2}**Golden Chicken** (**owned**): {1} {0}\n{3}".format(
                settings.silver_eggy_emoji,
                settings.golden_chicken_cost,
                settings.chicken_emoji,
                settings.object_descs["golden chicken"])

        if not database.has_inventory_item(authorID, "eggcellent_statue"):
            es_desc = "{2}**Eggcellent Statue**: {1} {0}\n{3}".format(
                settings.golden_eggy_emoji,
                settings.egg_statue_cost,
                settings.eggy_statue_emoji,
                settings.object_descs["eggcellent statue"])
        else:
            count = database.get_inventory_amount(authorID, "eggcellent_statue")
            es_desc = "{3}**Eggcellent Statue** (**{2} owned**): {1} {0}\n{3}".format(
                settings.golden_eggy_emoji,
                settings.egg_statue_cost,
                count,
                settings.eggy_statue_emoji,
                settings.object_descs["eggcellent statue"])

        if not database.has_inventory_item(authorID, "delicate_shovel"):
            ds_desc = "{2}**Delicate Shovel**: {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.delicate_shovel_cost,
                settings.shovel_emoji,
                settings.object_descs["delicate shovel"])
        else:
            ds_desc = "{2}**Delicate Shovel** (**owned**): {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.delicate_shovel_cost,
                settings.shovel_emoji,
                settings.object_descs["delicate shovel"])

        if not database.has_inventory_item(authorID, "egg_topper"):
            et_desc = "{2}**Egg Topper**: {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.egg_toper_cost,
                settings.topper_emoji,
                settings.object_descs["egg topper"])
        else:
            count = database.get_inventory_amount(authorID, "egg topper")
            et_desc = "{3}**Egg Topper** (**{2} owned**): {1} {0}\n{3}".format(
                settings.eggy_emoji,
                settings.egg_toper_cost,
                count,
                settings.topper_emoji,
                settings.object_descs["egg topper"])

        if not database.has_inventory_item(authorID, "golden_shovel"):
            gs_desc = "{2}**Golden Shovel**: {1} {0}\n{3}".format(
                settings.golden_eggy_emoji,
                settings.golden_shovel_cost,
                settings.golden_shovel_emoji,
                settings.object_descs["golden shovel"])
        else:
            gs_desc = "{2}**Golden Shovel** (**owned**): {1} {0}\n{3}".format(
                settings.golden_eggy_emoji,
                settings.golden_shovel_cost,
                settings.golden_shovel_emoji,
                settings.object_descs["golden shovel"])

        if not database.has_inventory_item(authorID, "jackpot"):
            jp_desc = "{2}**Jackpot**: {1} {0}\n{3}" \
                .format(settings.silver_eggy_emoji,
                        settings.jackpot_cost,
                        settings.jackpot_emoji,
                        settings.object_descs["jackpot"])
        else:
            jp_desc = "{2}**Jackpot** (**owned**): {1} {0}\n{3}" \
                .format(settings.silver_eggy_emoji,
                        settings.jackpot_cost,
                        settings.jackpot_emoji,
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
                settings.golden_eggy_emoji,
                settings.custom_role_cost,
                settings.object_descs["custom role"])
        else:
            cr_desc = "**Custom Role** (**owned**): {1} {0}\n{2}".format(
                settings.golden_eggy_emoji,
                settings.custom_role_cost,
                settings.object_descs["custom role"])

        if not database.has_inventory_item(authorID, "custom_channel"):
            cc_desc = "**Custom Channel**: {1} {0}\n{2}".format(
                settings.golden_eggy_emoji,
                settings.custom_channel_cost,
                settings.object_descs["custom channel"])
        else:
            cc_desc = "**Custom Channel** (**owned**): {1} {0}\n{2}".format(
                settings.golden_eggy_emoji,
                settings.custom_channel_cost,
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
                                                                               settings.silver_eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    elif item == "luckydrumstick" or item == "lucky drumstick" or item == "lucky_drumstick":
        cost = settings.lucky_drumstick_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_iron_cash(authorID, -cost)
            database.give_inventory_item(authorID, "lucky_drumstick", 1)
            await ctx.channel.send(
                "successfully purchased the lucky drumstick for {2} {0} {1}".format(cost, settings.cash_name,
                                                                                    settings.silver_eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    elif item == "goldenchicken" or item == "golden chicken" or item == "gold chicken" or item == "golden_chicken" or item == "gold_chicken":
        cost = settings.golden_chicken_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_iron_cash(authorID, -cost)
            database.give_inventory_item(authorID, "golden_chicken", 1)
            await ctx.channel.send(
                "successfully purchased the golden chicken for {2} {0} {1}".format(cost, settings.iron_cash_name,
                                                                                   settings.silver_eggy_emoji))
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
                    settings.golden_eggy_emoji))
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
                    settings.golden_eggy_emoji))
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
                                                                                    settings.golden_eggy_emoji))
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
                                                                                  settings.golden_eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough golden eggs to purchase this")
    elif item == "jackpot" or item == "jpot" or item == "jackp":
        cost = settings.jackpot_cost
        if database.get_iron_cash(authorID) >= cost:
            database.give_gold_cash(authorID, -cost)
            database.give_inventory_item(authorID, "jackpot", 1)
            await ctx.channel.send(
                "successfully purchased the jackpot for {2} {0} {1}".format(cost, settings.iron_cash_name,
                                                                            settings.silver_eggy_emoji))
        else:
            await ctx.channel.send("you don't have enough silver eggs to purchase this")
    else:
        await ctx.channel.send("invalid item")


@buy.error
async def buy_error(ctx, error):
    await error_handling(ctx, error, "buy")


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
                                                                      settings.eggy_emoji)
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
                                                                       settings.silver_eggy_emoji)
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
                                                                       settings.golden_eggy_emoji)
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
                                                                       settings.eggyolk_emoji)
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

        egg_topper = database.get_inventory_amount(authorID, "egg_topper")
        statue = database.get_inventory_amount(authorID, "eggcellent_statue")

        if authorID == 802159357306470430:
            emb.add_field(name="unlucky", value="you are just very unlucky")

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

        await ctx.channel.send(embed=emb)


@bot.command("profile", aliases=["prof"])
async def profile(ctx, who: discord.Member = None):
    await eggy_check(ctx, False)
    if who == None:
        who = ctx.author
    authorID = who.id
    emb = discord.Embed(
        title=""
    )

    emb.add_field(name="{0}Farm Level".format(settings.farm_emoji),
                  value="You are currently farm level {0}".format(database.get_farm_level(authorID)),
                  inline=False)

    emb.add_field(name="Basket",
                  value="You currently have:" + "\n" +
                        "{2} {0} {1}".format(database.get_cash(authorID), settings.cash_name,
                                             settings.eggy_emoji) + "\n" +
                        "{2} {0} {1}".format(database.get_iron_cash(authorID), settings.iron_cash_name,
                                             settings.silver_eggy_emoji) + "\n" +
                        "{2} {0} {1}".format(database.get_gold_cash(authorID), settings.gold_cash_name,
                                             settings.golden_eggy_emoji) + "\n" +
                        "{2} {0} {1}".format(database.get_eggyolks(authorID), settings.yolk_cash_name,
                                             settings.eggyolk_emoji),
                  inline=False)

    if authorID == bot.author_id:
        emb.set_author(name="god's profile", url=None, icon_url=ctx.author.avatar)
    else:
        emb.set_author(name="{0}'s profile".format(ctx.author.name), url=None, icon_url=ctx.author.avatar)

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
                                                                          settings.eggy_emoji)
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
                                                                          settings.silver_eggy_emoji)
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
                                                                          settings.golden_eggy_emoji)
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
                                                                          settings.eggyolk_emoji)
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

        if database.has_inventory_item(ctx.author.id, "binoculars"):
            rolled_eggs = rolled_eggs * 2

        database.give_cash(ctx.author.id, rolled_eggs)

        emb = discord.Embed(
            title="Found some {0}".format(settings.cash_name),
            description="You found {0} {3} {1} {2}".format(rolled_eggs, settings.cash_name, rolled_place,
                                                           settings.eggy_emoji)
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
        if database.has_inventory_item(authorID, "jackpot"):
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
            if database.has_inventory_item(authorID, "jackpot"):
                profit = int(round(profit * 1.5))
            await ctx.channel.send(embed=create_embed("profit",
                                                      f"you bargained your {amount} eggs for {profit} eggs"
                                                      f" (you got {(profit - amount)} eggs)"))
            database.give_cash(authorID, (profit - amount))
        elif profit < amount:
            await ctx.channel.send(embed=create_embed("profit",
                                                      f"you bargained your {amount} eggs for {profit} eggs"
                                                      f" (you lost {(amount - profit)} eggs)"))
            database.give_cash(authorID, (amount - profit))


@bargain.error
async def bargain_error(ctx, error):
    await error_handling(ctx, error, "bargain")


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
            if database.has_inventory_item(authorID, "lucky_drumstick"):
                rolled *= 1.5
                if rolled > 100:
                    rolled = 100
            if silver:
                get_chance = 20 + (20 * (flevel - 2))
                double_chance = 10 + (10 * (flevel - 2))
                if get_chance >= rolled:
                    get = 1
                if double_chance >= random.randint(1, 100):
                    get = 2
                database.give_iron_cash(authorID, get)
                await ctx.channel.send(embed=create_embed("Lucky", "you found {0} {1} silver eggs".format(get,
                                                                                                          settings.silver_eggy_emoji)))
            else:
                if not chatted and flevel >= 3:
                    get_chance = 20 + (20 * (flevel - 3))
                    double_chance = 10 + (10 * (flevel - 3))
                    if get_chance >= rolled:
                        get = 1
                    if double_chance >= random.randint(1, 100):
                        get = 2
                    database.give_gold_cash(authorID, get)
                    await ctx.channel.send(embed=create_embed("Lucky", "you found {0} {1} gold eggs".format(get,
                                                                                                            settings.golden_eggy_emoji)))


@bot.command("test_emojis")
@commands.has_role(863434428570796043)
async def test_emojis(ctx):
    await ctx.channel.send(settings.farm_emoji
                           + "," + settings.eggy_emoji
                           + "," + settings.eggyolk_emoji
                           + "," + settings.golden_eggy_emoji
                           + "," + settings.silver_eggy_emoji
                           + "," + settings.binoculars_emoji
                           + "," + settings.chicken_emoji
                           + "," + settings.drumstick_emoji
                           + "," + settings.shovel_emoji
                           + "," + settings.topper_emoji
                           )
    time.sleep(2.5)
    await ctx.channel.purge(limit=2)


@test_emojis.error
async def test_emojis_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.channel.send("https://tenor.com/view/no-nope-non-rick-rick-and-morty-gif-20999440")


def create_embed(title: str, description: str = "") -> discord.Embed:
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


if not os.path.exists("./backups"):
    os.mkdir("./backups")

if os.path.exists("./token.txt"):
    with open("./token.txt", "r") as f:
        lines = f.readlines()
        token = lines[0]
        print("loaded token from token.txt")
else:
    token = os.getenv("TOKEN")
    if token is not None:
        keep_alive()  # Starts a webserver to be pinged.
    print("loaded token from os secrets")

backup_database()

bot.run(token)  # Starts the bot
