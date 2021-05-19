import os
import discord
import cmdtools
import datetime
import iniparser2

from lib import utils


async def error_guild_info(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "guild_id":
            await error_guild_info.message.channel.send(":x: Guild id is required")
    else:
        raise error


async def _guild_info(guild_id):
    try:
        guild_id = int(guild_id)
    except Exception:
        await _guild_info.message.channel.send(":x: Guild id value is not an integer")
        return

    filename = f"data/guilds/{guild_id}.ini"

    if not os.path.isfile(filename):
        await _guild_info.message.channel.send(
            f":x: Guild id `{guild_id}` did not exists"
        )
        return

    guild = iniparser2.INI(convert_property=True)
    guild.read_file(filename)

    leader_user = await _guild_info.client.fetch_user(guild["info"]["leader"])

    created_at = datetime.datetime.strptime(
        guild["info"]["created"], "%Y-%m-%d %H:%M:%S.%f"
    )

    embed = discord.Embed(title=guild["info"]["name"], color=0xFF00FF)
    embed.description = f"Leader: **{leader_user.name}#{leader_user.discriminator}**"
    embed.description += (
        f"\nCreated At: **{created_at.strftime('%a %d %b %Y %X %p %z')}**"
    )
    embed.set_author(name=f"Level {guild['stats']['level']}")
    embed.description += (
        f"\nMembers Count: `{len(utils.get_guild_members_id(guild_id))}`"
    )
    embed.set_thumbnail(url=guild["info"]["logo"])

    try:
        await _guild_info.message.channel.send(embed=embed)
        return
    except Exception:
        pass

    embed.set_thumbnail(url=embed.Empty)
    await _guild_info.message.channel.send(embed=embed)
