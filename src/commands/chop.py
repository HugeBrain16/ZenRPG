import random
import iniparser2
import discord

from lib import utils
from lib import statics


async def _chop():
    assigned_ids = utils.get_assigned_user_ids()

    if _chop.message.author.id not in assigned_ids:
        await _chop.message.channel.send(":warning: Your id is not assigned")

    else:
        filename = f"data/users/{_chop.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["chop"] > 0:
            await _chop.message.channel.send(
                f":warning: command is still cooling down for {utils.fsec(data['cooldown']['chop'])}"
            )

        else:
            rng = random.randint(1, 3)

            if data["tools"]["axe"] in statics.chop:
                wood = statics.chop[data["tools"]["axe"]]

                if rng == 2:
                    data.set(
                        data["tools"]["axe"],
                        data["inventory"][data["tools"]["axe"]] - 1,
                        section="inventory",
                    )
                    await _chop.message.channel.send(
                        f":warning: {_chop.message.author.mention} Your `{data['tools']['axe']}` is broken!"
                    )
                    data.set("axe", True, section="tools")

            else:
                wood = 1

            data["inventory"]["wood"] += wood
            data["stats"]["current_exp"] += 1.0
            data["cooldown"]["chop"] = 30
            data.write(filename)

            embed = discord.Embed(
                title="Chop",
                description=f"You chopped x{wood} wood",
                color=0xFF00FF,
            )
            embed.set_author(name=_chop.message.author.display_name)

            await _chop.message.channel.send(embed=embed)
