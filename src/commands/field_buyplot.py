import iniparser2

from lib import utils


async def _field_buyplot():
    assigned_ids = utils.get_assigned_user_ids()

    if _field_buyplot.message.author.id not in assigned_ids:
        await _field_buyplot.message.channel.send(":warning: Your id is not assigned")

    else:
        fields = utils.get_fields()

        if _field_buyplot.message.author.id not in fields:
            await _field_buyplot.message.channel.send(f":x: You don't have a field")

        else:

            filename = f"data/fields/{_field_buyplot.message.author.id}.ini"
            user_filename = f"data/users/{_field_buyplot.message.author.id}.ini"

            data = iniparser2.INI(convert_property=True)
            user_data = iniparser2.INI(convert_property=True)
            data.read_file(filename)
            user_data.read_file(user_filename)

            if len(data.sections()) == 10:
                await _field_buyplot.message.channel.send(
                    ":x: You cannot buy more plots"
                )

            else:
                price = 1000 * len(data.sections())

                if user_data["stats"]["balance"] >= price:
                    await _field_buyplot.message.channel.send(
                        f":white_check_mark: You bought a new field plot with id `{len(data.sections())}`"
                    )
                    data.set_section(f"plot{len(data.sections())}")
                    data[f"plot{len(data.sections()) - 1}"]["plant"] = True
                    data[f"plot{len(data.sections()) - 1}"]["progress"] = 0

                    user_data["stats"]["balance"] -= price

                    data.write(filename)
                    user_data.write(user_filename)
