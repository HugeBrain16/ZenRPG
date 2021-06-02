import iniparser2
import cmdtools
import datetime

from lib import utils


async def error_guild_create(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "name":
            await error_guild_create.message.channel.send(":x: Guild name is required")

    else:
        raise error


async def _guild_create(name):
    assigned_ids = utils.get_assigned_user_ids()

    if _guild_create.message.author.id not in assigned_ids:
        await _guild_create.message.channel.send(":warning: Your id is not assigned")

    else:
        if len(name) < 3:
            await _guild_create.message.channel.send(
                ":x: Guild name is too short, min 3 characters"
            )

        else:
            for gid in utils.get_guilds_id():
                members = utils.get_guild_members_id(gid)

                if _guild_create.message.author.id in members:
                    await _guild_create.message.channel.send(
                        f":x: {_guild_create.message.author.mention}, You are already in a guild"
                    )
                    return

            names = utils.get_guilds_name()

            if name in names:
                await _guild_create.message.channel.send(
                    f":x: A guild with the name `{name}` already exists"
                )

            else:
                gid = utils.new_guild_id()
                filename = f"data/guilds/{gid}.ini"
                user_filename = f"data/users/{_guild_create.message.author.id}.ini"

                user_data = iniparser2.INI(convert_property=True)
                user_data.read_file(user_filename)

                if user_data["stats"]["balance"] < 10_000:
                    await _guild_create.message.channel.send(
                        ":x: You don't have enough coins to create a new guild, coins required 10,000"
                    )
                    return

                if user_data["stats"]["level"] < 5:
                    await _guild_create.message.channel.send(
                        ":x: You must be at least level 5 to create a new guild"
                    )
                    return

                open(filename, "w").close()

                data = iniparser2.INI(convert_property=True)
                data.set_section("info")
                data["info"]["name"] = name
                data["info"]["leader"] = _guild_create.message.author.id
                data["info"]["created"] = datetime.datetime.utcnow()
                data["info"]["logo"] = "no logo"

                data.set_section("stats")
                data["stats"]["level"] = 0
                data["stats"]["current_exp"] = 0.0
                data["stats"]["max_exp"] = 100.0

                data.set_section("members")
                data.set(_guild_create.message.author.id, True, section="members")

                user_data.set(
                    "balance", user_data["stats"]["balance"] - 10_000, section="stats"
                )

                data.write(filename)
                user_data.write(user_filename)

                await _guild_create.message.channel.send(
                    f":white_check_mark: Guild has successfully created with id `{gid}`"
                )
