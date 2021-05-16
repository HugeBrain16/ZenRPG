import discord
import iniparser2
from lib import utils


async def _balance():
    assigned_ids = utils.get_assigned_user_ids()

    if _balance.message.author.id not in assigned_ids:
        await _balance.message.channel.send(":warning: Your id is not assigned")

    else:

        filename = f"data/users/{_balance.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        embed = discord.Embed(
            title="Balance",
            description=f"You have `{data['stats']['balance']}` coins",
            color=0xFF00FF,
        )
        embed.set_author(name=_balance.message.author.display_name)

        await _balance.message.channel.send(embed=embed)
