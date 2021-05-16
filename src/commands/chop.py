import random
import iniparser2
import discord

from lib import utils


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
                f":warning: command is still cooling down for {data['cooldown']['chop']} minutes"
            )

        else:
            rng = random.randint(1, 5)

            data.set("wood", data["inventory"]["wood"] + rng, section="inventory")
            data.set("current_exp", data["stats"]["current_exp"] + 1.0, section="stats")
            data.set("chop", 1, section="cooldown")
            data.write(filename)

            embed = discord.Embed(
                title="Chop",
                description=f"You brought back x{rng} wood",
                color=0xFF00FF,
            )
            embed.set_author(name=_chop.message.author.display_name)

            await _chop.message.channel.send(embed=embed)
