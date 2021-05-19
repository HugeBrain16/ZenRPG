import iniparser2
import cmdtools

from lib import utils
from lib import statics


async def error_field_harvest(error):
    if isinstance(error, cmdtools.MissingRequiredArgument):
        if error.param == "plot":
            await error_field_harvest.message.channel.send(
                ":x: Plot number is required"
            )

    else:
        raise error


async def _field_harvest(plot):
    try:
        plot = int(plot)
    except Exception:
        await _field_harvest.message.channel.send(":x: use number to select a plot")

    else:

        assigned_ids = utils.get_assigned_user_ids()

        if _field_harvest.message.author.id not in assigned_ids:
            await _field_harvest.message.channel.send(
                ":warning: Your id is not assigned"
            )

        else:

            fields = utils.get_fields()

            if _field_harvest.message.author.id not in fields:
                await _field_harvest.message.channel.send(f":x: You don't have a field")

            else:

                filename = f"data/fields/{_field_harvest.message.author.id}.ini"
                user_filename = f"data/users/{_field_harvest.message.author.id}.ini"

                data = iniparser2.INI(convert_property=True)
                user_data = iniparser2.INI(convert_property=True)
                data.read_file(filename)
                user_data.read_file(user_filename)

                if "plot" + str(plot) not in data.sections():
                    await _field_harvest.message.channel.send(
                        f":x: Plot id `{plot}` did not exists"
                    )

                else:

                    _plot = "plot" + str(plot)

                    if data[_plot]["plant"] in statics.items:

                        if data[_plot]["progress"] == 0:
                            user_data.set(
                                data[_plot]["plant"],
                                user_data["inventory"][data[_plot]["plant"]] + 1,
                                section="inventory",
                            )
                            user_data.set(
                                "current_exp",
                                user_data["stats"]["current_exp"] + 10.0,
                                section="stats",
                            )
                            await _field_harvest.message.channel.send(
                                f":white_check_mark: {_field_harvest.message.author.mention}, You've harvested item `{data[_plot]['plant']}` from plot id `{plot}`"
                            )
                            data.set("plant", True, section=_plot)

                            data.write(filename)
                            user_data.write(user_filename)

                        else:
                            await _field_harvest.message.channel.send(
                                f":warning: crop on plot id `{plot}` is not yet mature, will mature in {utils.fsec(data[_plot]['progress'])}"
                            )
                    else:
                        await _field_harvest.message.channel.send(
                            f":x: Plot id {plot} is empty"
                        )
