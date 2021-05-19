import os
import iniparser2
import cmdtools

from lib import utils


async def error_guild_join(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "guild_id":
            await error_guild_join.message.channel.send(":x: Guild id is required")


async def _guild_join(guild_id):
    try:
        guild_id = int(guild_id)

    except Exception:
        await _guild_join.message.channel.send(":x: guild id is not an integer value")
        return

    assigned_ids = utils.get_assigned_user_ids()

    if _guild_join.message.author.id not in assigned_ids:
        await _guild_join.message.channel.send(":warning: Your id is not assigned")

    else:
        in_guild = False
        guilds = utils.get_guilds()

        for gid in range(len(guilds)):
            members = utils.get_guild_members_id(gid)

            if _guild_join.message.author.id in members:
                in_guild = True

        if in_guild is True:
            await _guild_join.message.channel.send(":x: You are already in a guild")
            return

        filename = f"data/guilds/{guild_id}.ini"

        if not os.path.isfile(filename):
            await _guild_join.message.channel.send(
                f":x: Guild id {guild_id} did not exists"
            )
            return

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        data.set(_guild_join.message.author.id, True, section="members")
        data.write(filename)

        await _guild_join.message.channel.send(
            f":white_check_mark: You have joined guild: `{guilds[guild_id]['name']}`"
        )
