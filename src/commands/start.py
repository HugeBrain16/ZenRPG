from lib import utils
from lib import statics
import iniparser2


async def _start():
    assigned_userids = utils.get_assigned_user_ids()

    if _start.message.author.id in assigned_userids:
        await _start.message.channel.send(":x: Your id has already assigned!")

    else:
        filename = f"data/users/{_start.message.author.id}.ini"

        open(filename, "w").close()

        data = iniparser2.INI(convert_property=True)

        data.set_section("stats")
        data["stats"]["balance"] = 500
        data["stats"]["level"] = 0
        data["stats"]["current_exp"] = 0.0
        data["stats"]["max_exp"] = 50.0

        data.set_section("status")
        data["status"]["health"] = 100.0
        data["status"]["max_health"] = 100.0

        data.set_section("inventory")
        for item in statics.items.keys():
            data["inventory"][item] = 0

        data.set_section("cooldown")
        for cooldown in statics.cooldowns:
            data["cooldown"][cooldown] = 0

        data.set_section("tools")
        for tool in statics.tools:
            data["tools"][tool] = True

        data.write(filename)

        await _start.message.channel.send(
            ":white_check_mark: Your id has successfully assigned!"
        )
