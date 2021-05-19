import iniparser2
import discord
import cmdtools

from lib import utils
from lib import statics


async def error_profile(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "mention":
            await error_profile.message.channel.send(
                ":x: please mention a user to see their info"
            )


async def _profile(mention):
    mention_id = utils.mention_to_id(mention)
    mention = await _profile.client.fetch_user(mention_id)
    if not isinstance(mention, discord.User):
        await _profile.message.channel.send(":x: mention is invalid")
        return

    assigned_ids = utils.get_assigned_user_ids()

    if mention.id not in assigned_ids:
        await _profile.message.channel.send(
            ":warning: The mentioned user does not have their id assigned"
        )

    else:
        filename = f"data/users/{mention.id}.ini"
        guild = None
        own_guild = None
        guilds = utils.get_guilds()

        for gid in range(len(guilds)):
            members = utils.get_guild_members_id(gid)

            if mention.id in members:
                guild = utils.get_guilds()[gid]

            if mention.id == int(guilds[gid]["leader"]):
                guild = None
                own_guild = guilds[gid]

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        embed = discord.Embed(title="Player Info", color=0xFF00FF)
        embed.set_author(name=mention.display_name)
        embed.set_footer(text=f"Requested by {_profile.message.author.display_name}")

        if guild is not None:
            embed.description = f"Guild: `{guild['name']}``\n\n"
        elif own_guild is not None:
            embed.description = f"[Leader] Guild: `{own_guild['name']}`\n\n"
        else:
            embed.description = ""

        stats_value = f"**Level**: {data['stats']['level']} ({int((data['stats']['current_exp']/data['stats']['max_exp']) * 100.0)}%)\n**EXP**: {data['stats']['current_exp']}/{data['stats']['max_exp']}\n**Balance**: {data['stats']['balance']} coin(s)"
        status_value = (
            f"**Health**: {data['status']['health']}/{data['status']['max_health']}"
        )
        equipment_value = ""
        for tool in statics.tools:
            if data["tools"][tool] in statics.items:
                equipment_value += f"**{tool.capitalize()}**: `{data['tools'][tool]}`\n"
            else:
                equipment_value += f"**{tool.capitalize()}**: `none`\n"

        embed.add_field(name="Stats", value=stats_value, inline=False)
        embed.add_field(name="Status", value=status_value, inline=False)
        embed.add_field(name="Equipment", value=equipment_value, inline=False)

        embed.set_thumbnail(url=mention.avatar_url)

        await _profile.message.channel.send(embed=embed)
