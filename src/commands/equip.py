import iniparser2
import cmdtools

from lib import utils
from lib import statics


async def error_equip(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_equip.message.channel.send(":x: Item name is required")


async def _equip(item):
    assigned_ids = utils.get_assigned_user_ids()

    if _equip.message.author.id not in assigned_ids:
        await _equip.message.channel.send(":warning: Your id is not assigned")

    else:

        if item in statics.items:
            if item.endswith("_axe"):
                filename = f"data/users/{_equip.message.author.id}.ini"

                data = iniparser2.INI(convert_property=True)
                data.read_file(filename)

                if data["inventory"][item] < 1:
                    await _equip.message.channel.send(
                        f":x: {_equip.message.author.mention} You don't have this item `{item}`"
                    )
                    return

                data.set("axe", item, section="tools")
                data.write(filename)

                await _equip.message.channel.send(
                    f":white_check_mark: {_equip.message.author.mention} You have equipped item: **{item}**"
                )

            elif item.endswith("_pickaxe"):
                filename = f"data/users/{_equip.message.author.id}.ini"

                data = iniparser2.INI(convert_property=True)
                data.read_file(filename)

                if data["inventory"][item] < 1:
                    await _equip.message.channel.send(
                        f":x: {_equip.message.author.mention} You don't have this item `{item}`"
                    )
                    return

                data.set("pickaxe", item, section="tools")
                data.write(filename)

                await _equip.message.channel.send(
                    f":white_check_mark: {_equip.message.author.mention} You have equipped item: **{item}**"
                )

            elif item.endswith("_sword"):
                filename = f"data/users/{_equip.message.author.id}.ini"

                data = iniparser2.INI(convert_property=True)
                data.read_file(filename)

                if data["inventory"][item] < 1:
                    await _equip.message.channel.send(
                        f":x: {_equip.message.author.mention} You don't have this item `{item}`"
                    )
                    return

                data.set("sword", item, section="tools")
                data.write(filename)

                await _equip.message.channel.send(
                    f":white_check_mark: {_equip.message.author.mention} You have equipped item: **{item}**"
                )

            else:
                await _equip.message.channel.send(f":x: Item `{item}` is not equipable")

        else:
            await _equip.message.channel.send(f":x: Item `{item}` did not exists")
