import iniparser2
import discord
import cmdtools

from lib import statics


async def error_sell(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_sell.message.channel.send(":x: No item name specified")


async def _sell(item, amount=1):
    try:
        amount = int(amount)

    except Exception:
        await _sell.message.channel.send(f":x: item amount must be an integer value")

    if item not in statics.items.keys():
        await _sell.message.channel.send(f"item `{item}` did not exists")

    else:
        filename = f"data/users/{_sell.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if amount < 1:
            await _sell.message.channel.send(":x: item amount cannot be lower than 1")

        else:

            if data["inventory"][item] < amount:
                await _sell.message.channel.send(
                    ":x: you don't have enough items to sell"
                )

            else:
                price = int((statics.items[item]["price"] / 1.8) * amount)

                data.set(item, data["inventory"][item] - 1, section="inventory")
                data.set("balance", data["stats"]["balance"] + price, section="stats")

                data.write(filename)

                embed = discord.Embed(
                    title="Sell",
                    description=f"You sold x{amount} {item} for {price} coins",
                    color=0xFF00FF,
                )

                await _sell.message.channel.send(embed=embed)
