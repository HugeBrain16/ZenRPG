import iniparser2
import discord

from lib import utils


async def _inventory(page=1):
    try:
        page = int(page) - 1
    except Exception:
        await _inventory.message.channel.send(
            ":warning: use number to navigate between pages"
        )
        return

    assigned_ids = utils.get_assigned_user_ids()

    if _inventory.message.author.id not in assigned_ids:
        await _inventory.message.channel.send(":warning: Your id is not assigned")

    else:

        pages = [[]]
        filename = f"data/users/{_inventory.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        for item in data["inventory"].keys():
            if len(pages[len(pages) - 1]) == 15:
                pages.append([])

            if len(pages[len(pages) - 1]) < 15:
                if data["inventory"][item] > 0:
                    pages[len(pages) - 1].append(f"{item}: {data['inventory'][item]}")

        if (page + 1) > len(pages) or (page + 1) < 1:
            await _inventory.message.channel.send(f":x: Page {page + 1} did not exists")

        else:
            if len(pages[0]) < 1:
                await _inventory.message.channel.send(
                    f":warning: You don't have any items"
                )

            else:
                embed = discord.Embed(title="Inventory", color=0xFF00FF)
                embed.set_author(name=_inventory.message.author.display_name)
                embed.description = "```\n" + "\n".join(pages[page]) + "\n```"
                embed.set_footer(text=f"Page {page + 1} of {len(pages)}")

                await _inventory.message.channel.send(embed=embed)
