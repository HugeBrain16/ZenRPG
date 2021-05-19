import iniparser2
import cmdtools

from lib import utils
from lib import statics


async def error_field_plant(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "item":
            await error_field_plant.message.channel.send(":x: seed name is required")
        elif error.param == "plot":
            await error_field_plant.message.channel.send(":x: plot number is required")

    else:
        raise error


async def _field_plant(seed, plot):
    try:
        plot = int(plot)
    except Exception:
        await _field_plant.message.channel.send(":x: use number to select a plot")

    else:

        assigned_ids = utils.get_assigned_user_ids()

        if _field_plant.message.author.id not in assigned_ids:
            await _field_plant.message.channel.send(":warning: Your id is not assigned")

        else:

            fields = utils.get_fields()

            if _field_plant.message.author.id not in fields:
                await _field_plant.message.channel.send(f":x: You don't have a field")

            else:

                if seed not in statics.items:
                    await _field_plant.message.channel.send(
                        f":x: Item `{seed}` did not exists"
                    )
                    return

                if not seed.endswith("_seed"):
                    await _field_plant.message.channel.send(
                        f":x: You cannot plant this item: `{seed}`"
                    )
                    return

                filename = f"data/fields/{_field_plant.message.author.id}.ini"
                seedfor = seed.split("_seed")[0]

                data = iniparser2.INI(convert_property=True)
                data.read_file(filename)

                if "plot" + str(plot) not in data.sections():
                    await _field_plant.message.channel.send(
                        f":x: Plot id `{plot}` did not exists"
                    )

                else:
                    _plot = "plot" + str(plot)

                    if (
                        data[_plot]["progress"] > 0
                        or data[_plot]["plant"] in statics.items
                    ):
                        await _field_plant.message.channel.send(
                            f":x: Plot id `{plot}` is not empty"
                        )

                    else:
                        data[_plot]["progress"] = statics.farm[seedfor]
                        data[_plot]["plant"] = seedfor

                        data.write(filename)

                        await _field_plant.message.channel.send(
                            f":white_check_mark: {_field_plant.message.author.mention}, You have planted `{seed}`, takes {utils.fsec(statics.farm[seedfor])} to mature."
                        )
