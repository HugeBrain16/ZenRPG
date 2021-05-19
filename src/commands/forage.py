import random
import iniparser2
import discord

from lib import utils
from lib import statics


async def _forage():
    assigned_ids = utils.get_assigned_user_ids()

    if _forage.message.author.id not in assigned_ids:
        await _forage.message.channel.send(":warning: Your id is not assigned")

    else:
        filename = f"data/users/{_forage.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["forage"] > 0:
            await _forage.message.channel.send(
                f":warning: command is still cooling down for {utils.fsec(data['cooldown']['forage'])}"
            )

        else:

            rng_result = random.randint(1, 5)
            rng_item = random.randint(0, len(statics.forage) - 1)
            item = statics.forage[rng_item]

            data.set(item, data["inventory"][item] + rng_result, section="inventory")
            data.set("current_exp", data["stats"]["current_exp"] + 1.0, section="stats")
            data.set("forage", 15, section="cooldown")
            data.write(filename)

            embed = discord.Embed(
                title="Forage",
                description=f"You found x{rng_result} `{item}`",
                color=0xFF00FF,
            )
            embed.set_author(name=_forage.message.author.display_name)

            await _forage.message.channel.send(embed=embed)
