import discord

from lib import utils
from lib import statics


async def _help(page=1):
    try:
        page = int(page) - 1
    except Exception:
        await _help.message.channel.send(
            ":warning: use number to navigate between pages"
        )

    else:
        cmds = utils.get_commands()

        pages = [[]]

        for cmd in cmds:
            if len(pages[len(pages) - 1]) == 10:
                pages.append([])

            if len(pages[len(pages) - 1]) < 10:
                try:
                    pages[len(pages) - 1].append(f"{cmd}\t{statics.help[cmd]}")
                except KeyError:
                    pages[len(pages) - 1].append(cmd)

        if (page + 1) > len(pages) or (page + 1) < 1:
            await _help.message.channel.send(f":x: Page {page + 1} did not exists")

        else:
            embed = discord.Embed(color=0xFF00FF)
            embed.description = (
                f"Available commands [page {page + 1} of {len(pages)}]:\n```\n"
                + "\n".join(pages[page])
                + "\n```"
            )
            embed.set_footer(text=f"Requested by {_help.message.author.display_name}")

            await _help.message.channel.send(embed=embed)
