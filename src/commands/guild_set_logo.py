import os
import iniparser2
import cmdtools

from lib import utils


async def error_guild_set_logo(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "url":
            await error_guild_set_logo.message.channel.send(":x: Logo url is required")


async def _guild_set_logo(url):
    for gid in utils.get_guilds_id():
        filename = f"data/guilds/{gid}.ini"

        if os.path.isfile(filename):
            data = iniparser2.INI(convert_property=True)
            data.read_file(filename)

            if _guild_set_logo.message.author.id == data["info"]["leader"]
                data["info"]["logo"] = url
                data.write(filename)

                await _guild_set_logo.message.channel.send(
                    f":white_check_mark: Logo has been updated for guild: **{data['info']['name']}**"
                )
                return

    await _guild_set_logo.message.channel.send(f":x: You don't own a guild")
