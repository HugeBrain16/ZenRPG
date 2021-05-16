import os
import discord
from discord.ext import tasks
import iniparser2
import cmdtools

from lib import utils

# setup directories
if not os.path.isdir("./data"):
    os.mkdir("./data")

if not os.path.isdir("./data/users"):
    os.mkdir("./data/users")

config = iniparser2.INI()
config.read_file("config.ini")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@tasks.loop(seconds=1)
async def update_exp():
    userids = utils.get_assigned_user_ids()

    for userid in userids:
        filename = f"data/users/{userid}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["stats"]["current_exp"] >= data["stats"]["max_exp"]:
            prev_exp = data["stats"]["current_exp"] - data["stats"]["max_exp"]

            data.set("current_exp", 0.0 + prev_exp, section="stats")
            data.set("max_exp", data["stats"]["max_exp"] * 2, section="stats")
            data.set("level", data["stats"]["level"] + 1, section="stats")

        data.write(filename)


@tasks.loop(minutes=1)
async def update_cooldown():
    userids = utils.get_assigned_user_ids()

    for userid in userids:
        filename = f"data/users/{userid}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        for cooldown in data["cooldown"].keys():
            if data["cooldown"][cooldown] > 0:
                data.set(cooldown, data["cooldown"][cooldown] - 1, section="cooldown")

        data.write(filename)


@client.event
async def on_ready():
    print("Logged in as: %s" % (client.user))

    update_cooldown.start()


@client.event
async def on_message(msg):

    cmdtext = msg.content
    cmdobj = cmdtools.Cmd(cmdtext, prefix=config["PREFIX"])
    cmdobj.parse()

    if cmdobj.name:
        if msg.author.bot is True:
            return

        cmds = utils.get_commands()

        if cmdobj.name in cmds:
            cmd = __import__(f"commands.{cmdobj.name}", fromlist=["commands"])

            cmdcall = getattr(cmd, f"_{cmdobj.name}", None)
            cmderrcall = getattr(cmd, f"error_{cmdobj.name}", None)

            if cmdcall is not None:
                if cmderrcall is not None:
                    await cmdtools.AioProcessCmd(
                        cmdobj,
                        cmdcall,
                        cmderrcall,
                        attrs={
                            "message": msg,
                            "client": client,
                        },
                    )

                else:
                    await cmdtools.AioProcessCmd(
                        cmdobj,
                        cmdcall,
                        attrs={
                            "message": msg,
                            "client": client,
                        },
                    )

            else:
                await msg.channel.send(
                    "Internal Error: No command callback for command `{cmdobj.name}`"
                )


client.run(config["TOKEN"])
