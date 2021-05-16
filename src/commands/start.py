from re import S
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
        data.set("balance", 500, section="stats")
        data.set("level", 0, section="stats")
        data.set("current_exp", 0.0, section="stats")
        data.set("max_exp", 50.0, section="stats")

        data.set_section("status")
        data.set("health", 100.0, section="status")

        data.set_section("inventory")
        for item in statics.items.keys():
            data.set(item, 0, section="inventory")

        data.set_section("cooldown")
        for cooldown in statics.cooldowns:
            data.set(cooldown, 0, section="cooldown")

        data.write(filename)

        await _start.message.channel.send(
            ":white_check_mark: Your id has successfully assigned!"
        )
