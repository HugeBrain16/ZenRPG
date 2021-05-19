import iniparser2
import cmdtools
import discord

from lib import utils
from lib import statics


async def error_buy(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_buy.message.channel.send(":x: Item name is required")


async def _buy(item, amount=1):
    try:
        amount = int(amount)
    except Exception:
        await _buy.message.channel.send(f":x: item amount must be an integer value.")
        return

    assigned_ids = utils.get_assigned_user_ids()

    if _buy.message.author.id not in assigned_ids:
        await _buy.message.channel.send(":warning: Your id is not assigned")

    else:

        filename = f"data/users/{_buy.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if item not in statics.items:
            await _buy.message.channel.send(f":x: Item `{item}` did not exists")
            return

        if statics.items[item]["purchasable"] is False:
            await _buy.message.channel.send(f":x: You cannot buy this item, `{item}`")
            return

        if amount < 1:
            await _buy.message.channel.send(":x: item amount cannot be lower than 1")
            return

        price = statics.items[item]["price"] * amount

        if data["stats"]["balance"] < amount:
            await _buy.message.channel.send(
                f":x: You need **{price}** coins to buy x{amount} `{item}`"
            )
            return

        data.set(item, data["inventory"][item] + amount, section="inventory")
        data.set("balance", data["stats"]["balance"] - price, section="stats")

        data.write(filename)

        embed = discord.Embed(title="Buy", color=0xFF00FF)
        embed.description = f"You bought x{amount} `{item}` for **{price}** coins"
        embed.set_author(name=_buy.message.author.display_name)

        await _buy.message.channel.send(embed=embed)
