import discord

from lib import statics


async def _items():
    embed = discord.Embed(title="Items", color=0xFF00FF)
    embed.description = "List of all items..."
    for item in sorted(statics.items):
        embed.add_field(
            name=item.replace("_", " ").capitalize(),
            value=f"**ID**: `{item}`\n**Price**: {statics.items[item]['price']}\n**Purchasable**: {statics.items[item]['purchasable']}\n**Sellable**: {statics.items[item]['sellable']}",
            inline=True,
        )
    embed.set_footer(text=f"Requested by {_items.message.author.display_name}")

    await _items.message.channel.send(embed=embed)
