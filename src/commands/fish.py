import iniparser2
import random
import discord

from lib import utils


async def _fish():
    assigned_ids = utils.get_assigned_user_ids()

    if _fish.message.author.id not in assigned_ids:
        await _fish.message.channel.send(":warning: Your id is not assigned")

    else:
        filename = f"data/users/{_fish.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["fish"] > 0:
            await _fish.message.channel.send(
                f":x: Command is still cooling down for {utils.fsec(data['cooldown']['fish'])} minutes"
            )
            return

        if data["inventory"]["fishing_rod"] < 1:
            await _fish.message.channel.send(":x: You don't have a fishing rod")
            return

        else:
            rng = random.randint(1, 3)
            rng_fish = random.randint(1, 3)

            if rng == 2:
                data.set(
                    "fishing_rod",
                    data["inventory"]["fishing_rod"] - 1,
                    section="inventory",
                )
                await _fish.message.channel.send(
                    f":warning: {_fish.message.author.mention}, Your fishing rod is broken"
                )

            if rng_fish == 2:
                data.set("fish", 60, section="cooldown")
                data.set("fish", data["inventory"]["fish"] + 1, section="inventory")
                data.set(
                    "current_exp", data["stats"]["current_exp"] + 2.0, section="stats"
                )

                await _fish.message.channel.send(
                    f"{_fish.message.author.mention}, You have caught a `fish`"
                )

            else:
                data.set("fish", 60, section="cooldown")
                await _fish.message.channel.send(f":x: you didn't catch anything")

        data.write(filename)
