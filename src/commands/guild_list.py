import discord

from lib import utils


async def _guild_list(page=1):
    try:
        page = int(page) - 1
    except Exception:
        await _guild_list.message.channel.send(
            ":warning: use number to navigate between pages"
        )
        return

    guilds = utils.get_guilds()

    pages = [[]]

    for guild in guilds:
        if len(pages[len(pages) - 1]) == 10:
            pages.append([])

        if len(pages[len(pages) - 1]) < 10:
            fuser = await _guild_list.client.fetch_user(guild["leader"])
            pages[len(pages) - 1].append(
                f"{guild['id']}). {guild['name']} [leader {fuser.name}#{fuser.discriminator}] [members {guild['members']}]"
            )

    if (page + 1) > len(pages) or (page + 1) < 1:
        await _guild_list.message.channel.send(f":x: Page {page + 1} did not exists")
        return

    if len(pages[0]) < 1:
        await _guild_list.message.channel.send(f":x: No guilds were created")
        return

    embed = discord.Embed(title="List of Guilds", color=0xFF00FF)
    embed.description = "```\n" + "\n".join(pages[page]) + "\n```"
    embed.set_author(name=f"Page {page + 1} of {len(pages)}")

    await _guild_list.message.channel.send(embed=embed)
