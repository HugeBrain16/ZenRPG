import iniparser2

from lib import utils


async def _guild_leave():
    assigned_ids = utils.get_assigned_user_ids()

    if _guild_leave.message.author.id not in assigned_ids:
        await _guild_leave.message.channel.send(":warning: Your id is not assigned")

    else:
        in_guild = False
        is_leader = False
        guild_id = -1

        for gid in utils.get_guilds_id():
            members = utils.get_guild_members_id(gid)

            guild = iniparser2.INI(convert_property=True)
            guild.read_file(f"data/guilds/{gid}.ini")

            if _guild_leave.message.author.id in members:
                in_guild = True
                guild_id = gid

            if _guild_leave.message.author.id == guild["info"]["leader"]:
                in_guild = False
                is_leader = True
                guild_id = gid

        if is_leader:
            await _guild_leave.message.channel.send(
                ":x: You can't leave if you are a leader of a guild, you can delete your guild"
            )
            return

        elif in_guild:
            filename = f"data/guilds/{guild_id}.ini"

            data = iniparser2.INI(convert_property=True)
            data.read_file(filename)

            data.remove_property(str(_guild_leave.message.author.id), section="members")
            data.write(filename)

            await _guild_leave.message.channel.send(
                f":white_check_mark: You left the guild: **{data['info']['name']}**"
            )

        else:
            await _guild_leave.message.channel.send(":x: You are not in a guild")
