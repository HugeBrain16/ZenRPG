import iniparser2
import discord

from lib import utils
from lib import statics


async def _field():
    assigned_ids = utils.get_assigned_user_ids()

    if _field.message.author.id not in assigned_ids:
        await _field.message.channel.send(":warning: Your id is not assigned")

    else:
        fields = utils.get_fields()

        if _field.message.author.id not in fields:
            await _field.message.channel.send(f":x: You don't have a field")

        else:

            filename = f"data/fields/{_field.message.author.id}.ini"

            data = iniparser2.INI(convert_property=True)
            data.read_file(filename)

            embed = discord.Embed(
                title=f"{_field.message.author.display_name}'s Field", color=0xFF00FF
            )

            for pid, plot in enumerate(data.sections()):
                if data[plot]["progress"] > 0 and data[plot]["plant"] in statics.items:
                    embed.add_field(
                        name=f"Plot {pid}",
                        value=f"Growing {data[plot]['plant']}...",
                        inline=False,
                    )
                elif (
                    data[plot]["progress"] == 0 and data[plot]["plant"] in statics.items
                ):
                    embed.add_field(
                        name=f"Plot {pid}",
                        value=f"{data[plot]['plant']} is ready to be harvested",
                        inline=False,
                    )
                else:
                    embed.add_field(name=f"Plot {pid}", value="Empty", inline=False)
            await _field.message.channel.send(embed=embed)
