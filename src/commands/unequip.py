import iniparser2
import cmdtools

from lib import utils
from lib import statics


async def error_unequip(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "tool":
            await error_unequip.message.channel.send(":x: Tool name is required")


async def _unequip(tool):
    assigned_ids = utils.get_assigned_user_ids()

    if _unequip.message.author.id not in assigned_ids:
        await _unequip.message.channel.send(":warning: Your id is not assigned")

    else:
        if tool in statics.tools:
            filename = f"data/users/{_unequip.message.author.id}.ini"

            data = iniparser2.INI(convert_property=True)
            data.read_file(filename)

            if data["tools"][tool] is True:
                await _unequip.message.channel.send(
                    f":x: {_unequip.message.author.mention}, You are not equipping this tool: `{tool}`"
                )
                return

            data["tools"][tool] = True
            data.write(filename)

            await _unequip.message.channel.send(
                f":white_check_mark: {_unequip.message.author.mention}, You have unequipped tool **{tool}**"
            )
        else:
            await _unequip.message.channel.send(f":x: Tool `{tool}` did not exists")
