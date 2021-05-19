import random
from lib import utils
from lib import statics
import discord
import iniparser2


async def _mine():
    assigned_ids = utils.get_assigned_user_ids()

    if _mine.message.author.id not in assigned_ids:
        await _mine.message.channel.send(":warning: Your id is not assigned")

    else:

        filename = f"data/users/{_mine.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["mine"] > 0:
            await _mine.message.channel.send(
                f":warning: command is still cooling down for {utils.fsec(data['cooldown']['mine'])}"
            )

        else:

            rng = random.randint(0, len(statics.mine) - 1)
            mine_keys = [key for key in statics.mine.keys()]
            item = mine_keys[rng]
            rng_broken = random.randint(1, 3)

            data.set("mine", 45, section="cooldown")
            data.set("current_exp", data["stats"]["current_exp"] + 1.0, section="stats")

            if data["tools"]["pickaxe"] not in statics.items:
                await _mine.message.channel.send(f":x: Equip a pickaxe to mine")
                return

            try:
                result = statics.mine[item][data["tools"]["pickaxe"]]
            except KeyError:
                result = 0

            if rng_broken == 2:
                data.set(
                    data["tools"]["pickaxe"],
                    data["inventory"][data["tools"]["pickaxe"]] - 1,
                    section="inventory",
                )
                await _mine.message.channel.send(
                    f":warning: {_mine.message.author.mention}, Your {data['tools']['pickaxe']} is broken"
                )
                data.set("pickaxe", True, section="tools")

            data.set(
                item, data.get(item, section="inventory") + result, section="inventory"
            )
            data.write(filename)

            embed = discord.Embed(
                title="Mine",
                color=0xFF00FF,
            )

            if result > 0:
                embed.description = f"You mined x{result} `{item.upper()}`"
            else:
                embed.description = "You found nothing"
            embed.set_author(name=_mine.message.author.display_name)

            await _mine.message.channel.send(embed=embed)
