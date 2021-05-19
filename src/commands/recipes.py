import discord

from lib import statics


async def _recipes(page=1):
    try:
        page = int(page) - 1
    except Exception:
        await _recipes.message.channel.send(":x: Use number to navigate between pages")

    else:
        pages = [[]]

        for item in statics.craft:
            if len(pages[len(pages) - 1]) == 10:
                pages.append([])

            if len(pages[len(pages) - 1]) < 10:
                pages[len(pages) - 1].append({item: statics.craft[item]})

        if (page + 1) > len(pages) or (page + 1) < 1:
            await _recipes.message.channel.send(f":x: Page {page + 1} did not exists")

        else:

            embed = discord.Embed(title="Crafting Recipes", color=0xFF00FF)
            embed.set_footer(
                text=f"Requested by {_recipes.message.author.display_name}"
            )

            for index, item in enumerate(pages[page]):
                recipes = []

                for item in item.keys():
                    for recipe in pages[page][index][item]["recipes"]:
                        recipes.append(
                            f"`x{pages[page][index][item]['recipes'][recipe]} {recipe}`"
                        )

                    embed.add_field(
                        name=item,
                        value=" + ".join(recipes)
                        + " = "
                        + f"x{pages[page][index][item]['result']} {item}",
                        inline=False,
                    )

            embed.set_author(name=f"Page {page + 1} of {len(pages)}")

            await _recipes.message.channel.send(embed=embed)
