import iniparser2
import cmdtools

from lib import utils
from lib import statics


async def error_use(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_use.message.channel.send(":x: item name is required")

    else:
        raise error


async def _use(item):
    assigned_ids = utils.get_assigned_user_ids()

    if _use.message.author.id not in assigned_ids:
        await _use.message.channel.send(":warning: Your id is not assigned")

    else:

        filename = f"data/users/{_use.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if item not in statics.items:
            await _use.message.channel.send(f":x: Item did not exists, `{item}`")
            return

        if item not in statics.consumable:
            await _use.message.channel.send(f":x: You cannot use this item, `{item}`")

        else:
            if data["inventory"][item] > 0:
                if data["status"]["health"] == data["status"]["max_health"]:
                    await _use.message.channel.send(
                        ":warning: Your Health is maxed out"
                    )
                    return

                if (data["status"]["health"] + statics.consumable[item]) > data[
                    "status"
                ]["max_health"]:
                    data.set("health", data["status"]["max_health"], section="status")

                else:
                    data.set(
                        "health",
                        data["status"]["health"] + statics.consumable[item],
                        section="status",
                    )

                data.set(item, data["inventory"][item] - 1, section="inventory")

                data.write(filename)

                await _use.message.channel.send(
                    f":white_check_mark: {_use.message.author.mention}, You used the item `{item}`, health restored **{statics.consumable[item]} HP**"
                )
            else:
                await _use.message.channel.send(
                    f":x: You don't have that item, `{item}`"
                )
