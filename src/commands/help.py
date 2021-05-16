from lib import utils


async def _help():
    cmds = utils.get_commands()

    await _help.message.channel.send(
        "Available commands:\n```" + "\n".join(cmds) + "```"
    )
