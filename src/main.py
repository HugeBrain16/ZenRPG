import os
import importlib
import discord
from discord.ext import tasks
import iniparser2
import cmdtools

from lib import utils
from lib import statics

# setup directories
if not os.path.isdir("./data"):
    os.mkdir("./data")

if not os.path.isdir("./data/users"):
    os.mkdir("./data/users")

if not os.path.isdir("./data/guilds"):
    os.mkdir("./data/guilds")

if not os.path.isdir("./data/fields"):
    os.mkdir("./data/fields")

config = iniparser2.INI()
config.read_file("config.ini")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@tasks.loop(seconds=1)
async def update_user_database():
    users = utils.get_assigned_user_ids()

    for user in users:
        filename = f"data/users/{user}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data.has_section("inventory") is False:
            data.set_section("inventory")

        for item in statics.items.keys():
            if data.has_property(item, section="inventory") is False:
                data["inventory"][item] = 0

        if data.has_section("cooldown") is False:
            data.set_section("cooldown")

        for cooldown in statics.cooldowns:
            if data.has_property(cooldown, section="cooldown") is False:
                data["cooldown"][cooldown] = 0

        if data.has_section("tools") is False:
            data.set_section("tools")

        for tool in statics.tools:
            if data.has_property(tool, section="tools") is False:
                data["tools"][tool] = True

        data.write(filename)


@tasks.loop(seconds=1)
async def update_guild_exp():
    guilds = utils.get_guilds_data()

    for gid, guild in enumerate(guilds):
        filename = f"data/guilds/{gid}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["stats"]["current_exp"] >= data["stats"]["max_exp"]:
            prev_exp = data["stats"]["current_exp"] - data["stats"]["max_exp"]

            data["stats"]["current_exp"] = 0.0 + prev_exp
            data["stats"]["max_exp"] *= 2
            data["stats"]["level"] += 1

        data.write(filename)


@tasks.loop(seconds=1)
async def update_exp():
    userids = utils.get_assigned_user_ids()

    for userid in userids:
        filename = f"data/users/{userid}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["stats"]["current_exp"] >= data["stats"]["max_exp"]:
            prev_exp = data["stats"]["current_exp"] - data["stats"]["max_exp"]

            data["stats"]["current_exp"] = 0.0 + prev_exp
            data["stats"]["max_exp"] *= 2
            data["stats"]["level"] += 1

        data.write(filename)


@tasks.loop(seconds=1)
async def update_cooldown():
    userids = utils.get_assigned_user_ids()

    for userid in userids:
        filename = f"data/users/{userid}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        for cooldown in data["cooldown"].keys():
            if data["cooldown"][cooldown] > 0:
                data["cooldown"][cooldown] -= 1

        data.write(filename)


@tasks.loop(seconds=1)
async def update_fields():
    fields = utils.get_fields()

    for field in fields:
        filename = f"data/fields/{field}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        for plot in data.sections():
            if data[plot]["progress"] > 0 and data[plot]["plant"] in statics.items:
                data[plot]["progress"] -= 1

        data.write(filename)


@client.event
async def on_ready():
    print("Logged in as: %s" % (client.user))

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"My prefix is {config['PREFIX']}"
        )
    )

    update_cooldown.start()
    update_exp.start()
    update_guild_exp.start()
    update_user_database.start()
    update_fields.start()


@client.event
async def on_message(msg):

    cmdtext = msg.content
    cmd = cmdtools.Cmd(cmdtext, prefix=config["PREFIX"])

    if cmd.name:
        if msg.author.bot is True:
            return

        cmds = utils.get_commands()

        if cmd.name in cmds:
            cmdobj = importlib.import_module(f"commands.{cmd.name}")

            cmdcall = getattr(cmdobj, f"_{cmd.name}", None)
            cmderrcall = getattr(cmdobj, f"error_{cmd.name}", None)

            if cmdcall is not None:
                if cmderrcall is not None:
                    await cmd.aio_process_cmd(
                        cmdcall,
                        cmderrcall,
                        attrs={
                            "message": msg,
                            "client": client,
                        },
                    )

                else:
                    await cmd.aio_process_cmd(
                        cmdcall,
                        attrs={
                            "message": msg,
                            "client": client,
                        },
                    )

            else:
                await msg.channel.send(
                    f"Internal Error: No command callback for command `{cmd.name}`"
                )


client.run(config["TOKEN"])
