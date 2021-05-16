import iniparser2
import discord
import cmdtools

from lib import utils


async def error_player(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "mention":
            await error_player.message.channel.send(
                ":x: please mention a user to see their info"
            )


async def _player(mention):
    mention_id = int(
        mention.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
    )
    mention = await _player.client.fetch_user(mention_id)
    if not isinstance(mention, discord.User):
        await _player.message.channel.send(":x: mention is invalid")
        return

    assigned_ids = utils.get_assigned_user_ids()

    if mention.id not in assigned_ids:
        await _player.message.channel.send(
            ":warning: The mentioned user does not have their id assigned"
        )

    else:
        filename = f"data/users/{mention.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        embed = discord.Embed(title="Player Info", color=0xFF00FF)
        embed.set_author(name=f"{mention.display_name} Lv.{data['stats']['level']}")
        embed.set_footer(text=f"Requested by {_player.message.author.display_name}")
        embed.description = f"Showing information for user {mention.display_name}\n\nSTATS:```\nBalance: {data['stats']['balance']}\nCurrent EXP: {data['stats']['current_exp']}\nMax EXP: {data['stats']['max_exp']}```\n\nSTATUS:\n```Health: {data['status']['health']}```"

        await _player.message.channel.send(embed=embed)
