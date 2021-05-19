import os

import iniparser2
from lib import utils


async def _guild_delete():
    assigned_ids = utils.get_assigned_user_ids()

    if _guild_delete.message.author.id not in assigned_ids:
        await _guild_delete.message.channel.send(":warning: Your id is not assigned")

    else:
        for gid in utils.get_guilds_id():
            guild = iniparser2.INI(convert_property=True)
            guild.read_file(f"data/guilds/{gid}.ini")

            if guild["info"]["leader"] == _guild_delete.message.author.id:
                os.remove(f"data/guilds/{gid}.ini")

                await _guild_delete.message.channel.send(
                    ":white_check_mark: Guild deleted"
                )
                return

        await _guild_delete.message.channel.send(":x: You don't own a guild")
