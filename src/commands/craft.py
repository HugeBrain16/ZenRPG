import iniparser2
import cmdtools
import discord

from lib import utils
from lib import statics


async def error_craft(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_craft.message.channel.send(":x: Item name is required")


async def _craft(item, amount=1):
    try:
        amount = int(amount)

    except Exception:
        await _craft.message.channel.send(":x: item amount value is not an integer")
        return

    assigned_ids = utils.get_assigned_user_ids()

    if _craft.message.author.id not in assigned_ids:
        await _craft.message.channel.send(":warning: Your id is not assigned")

    else:
        if item not in statics.items.keys():
            await _craft.message.channel.send(f":x: Item `{item}` did not exists")
            return

        if item not in statics.craft.keys():
            await _craft.message.channel.send(f":x: Item `{item}` is not craftable")
            return

        if amount < 1:
            await _craft.message.channel.send(f":x: Amount cannot be lower than 1")

        filename = f"data/users/{_craft.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        used = []

        for recipe in statics.craft[item]["recipes"]:
            if data["inventory"][recipe] < statics.craft[item]["recipes"][recipe]:
                await _craft.message.channel.send(
                    f":x: item required x{statics.craft[item]['recipes'][recipe]} `{recipe}`"
                )
                return

            else:
                used.append(
                    f"x{statics.craft[item]['recipes'][recipe] * amount} {recipe}"
                )
                data["inventory"][recipe] -= (statics.craft[item]["recipes"][recipe] * amount)

        data["inventory"][item] += (statics.craft[item]["result"] * amount)
        data.write(filename)

        embed = discord.Embed(title="Craft", color=0xFF00FF)
        embed.description = (
            f"Successfully crafted x{statics.craft[item]['result'] * amount} {item}\n"
        )
        embed.description = (
            embed.description + "\nItem used\n```" + "\n".join(used) + "```"
        )
        embed.set_author(name=_craft.message.author.display_name)

        await _craft.message.channel.send(embed=embed)
