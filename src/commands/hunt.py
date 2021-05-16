import random
from lib import utils
from lib import statics
import discord
import iniparser2


async def _hunt():
    assigned_ids = utils.get_assigned_user_ids()

    if _hunt.message.author.id not in assigned_ids:
        await _hunt.message.channel.send(":warning: Your id is not assigned")

    else:

        filename = f"data/users/{_hunt.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["hunt"] > 0:
            await _hunt.message.channel.send(
                f":warning: command is still cooling down for {data['cooldown']['hunt']} minute(s)."
            )

        else:

            rng = random.randint(0, len(statics.hunt) - 1)
            item = statics.hunt[rng]

            data.set("hunt", 2, section="cooldown")
            data.set("current_exp", data["stats"]["current_exp"] + 1.5, section="stats")
            data.set(item, data.get(item, section="inventory") + 1, section="inventory")
            data.write(filename)

            embed = discord.Embed(
                title="Hunt",
                description=f"You brought back a(n) `{item.upper()}`",
                color=0xFF00FF,
            )
            embed.set_author(name=_hunt.message.author.display_name)

            await _hunt.message.channel.send(embed=embed)
