import discord
import cmdtools

from lib import utils


async def error_avatar(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "mention":
            await error_avatar.message.channel.send(":x: please mention a user")


async def _avatar(mention):
    mention_id = utils.mention_to_id(mention)
    mention = await _avatar.client.fetch_user(mention_id)
    if not isinstance(mention, discord.User):
        await _avatar.message.channel.send(":x: mention is invalid")
        return

    embed = discord.Embed(title="Avatar", color=0xFF00FF)
    embed.set_author(name=mention.display_name)
    embed.set_image(url=mention.avatar_url)
    embed.set_footer(text=f"Requested by {_avatar.message.author.display_name}")

    await _avatar.message.channel.send(embed=embed)
