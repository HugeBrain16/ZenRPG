from re import I
import iniparser2

from lib import utils


async def _field_buy():
    assigned_ids = utils.get_assigned_user_ids()

    if _field_buy.message.author.id not in assigned_ids:
        await _field_buy.message.channel.send(":warning: Your id is not assigned")

    else:

        fields = utils.get_fields()

        if _field_buy.message.author.id in fields:
            await _field_buy.message.channel.send(f":x: You already have a field")

        else:

            filename = f"data/fields/{_field_buy.message.author.id}.ini"
            user_filename = f"data/users/{_field_buy.message.author.id}.ini"

            user_data = iniparser2.INI(convert_property=True)
            user_data.read_file(user_filename)

            if user_data["stats"]["balance"] >= 1000:
                open(filename, "w").close()

                data = iniparser2.INI(convert_property=True)
                data.read_file(filename)

                # free plot woo
                data.set_section("plot0")
                data["plot0"]["plant"] = True
                data["plot0"]["progress"] = 0

                user_data.set(
                    "balance", user_data["stats"]["balance"] - 1000, section="stats"
                )

                data.write(filename)
                user_data.write(user_filename)

                await _field_buy.message.channel.send(
                    ":white_check_mark: You bought a field"
                )

            else:
                await _field_buy.message.channel.send(
                    ":x: You need 1000 coins to buy a new field"
                )
