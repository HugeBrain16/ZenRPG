import os
import iniparser2
import discord
import cmdtools


async def error_guild_members(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "guild_id":
            await error_guild_members.message.channel.send(":x: guild id is required")


async def _guild_members(guild_id, page=1):
    try:
        guild_id = int(guild_id)

    except Exception:
        await _guild_members.message.channel.send(
            ":x: Guild id value is not an integer"
        )
        return

    try:
        page = int(page) - 1

    except Exception:
        await _guild_members.message.channel.send(
            ":x: Use number to navigate between pages"
        )
        return

    filename = f"data/guilds/{guild_id}.ini"

    if os.path.isfile(filename):
        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        pages = [[]]

        for member in data["members"].keys():
            member = int(member)

            if len(pages[len(pages) - 1]) == 10:
                pages.append([])

            if len(pages[len(pages) - 1]) < 10:
                user = await _guild_members.client.fetch_user(member)
                if member != data["info"]["leader"]:
                    pages[len(pages) - 1].append(f"{user.name}#{user.discriminator}")

        if (page + 1) > len(pages) or (page + 1) < 1:
            await _guild_members.message.channel.send(
                f":x: Page {page + 1} did not exists"
            )
            return

        leader = await _guild_members.client.fetch_user(data["info"]["leader"])

        embed = discord.Embed(title="Members", color=0xFF00FF)
        embed.set_author(name=data["info"]["name"])
        embed.description = f"Leader: **{leader.name}#{leader.discriminator}**"

        if len(pages[0]) > 0:
            embed.description += "\n\n```\n"
            embed.description += "\n".join(pages[page])
            embed.description += "\n```"
            embed.set_footer(text=f"Page {page + 1} of {len(pages)}")

        embed.set_thumbnail(url=data["info"]["logo"])

        try:
            await _guild_members.message.channel.send(embed=embed)
            return
        except Exception:
            pass

        embed.set_thumbnail(url=embed.Empty)
        await _guild_members.message.channel.send(embed=embed)

    else:
        await _guild_members.message.channel.send(
            f":x: Guild id `{guild_id}` did not exists"
        )
