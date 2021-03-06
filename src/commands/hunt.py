import random
import iniparser2
import discord

from lib import statics
from lib import utils


async def _hunt():
    assigned_ids = utils.get_assigned_user_ids()

    if _hunt.message.author.id not in assigned_ids:
        await _hunt.message.channel.send(":warning: Your id is not assigned")

    else:
        filename = f"data/users/{_hunt.message.author.id}.ini"

        data = iniparser2.INI(convert_property=True)
        data.read_file(filename)

        if data["cooldown"]["hunt"] > 0:
            await _hunt.message.channel.send(
                f":warning: Command is still cooling down for {utils.fsec(data['cooldown']['hunt'])}"
            )

        else:
            rng = random.randint(0, len(statics.hunt) - 1)
            rng_break = random.randint(1, 3)
            keys = [key for key in statics.hunt.keys()]
            item = keys[rng]
            item_data = statics.hunt[item]

            if len(item_data) > 0 and data["tools"]["sword"] in item_data:
                if (
                    data["status"]["health"] - item_data[data["tools"]["sword"]]
                ) <= 0.0:
                    data["status"]["health"] = data["status"]["max_health"]
                    data["stats"]["current_exp"] = 0.0

                    if data["stats"]["level"] > 0:
                        data["stats"]["max_exp"] /= 2
                        data["stats"]["level"] -= 1

                    data["cooldown"]["hunt"] = 60

                    for tool in statics.tools:
                        if tool in statics.items:
                            data.set(
                                tool, data["inventory"]["tool"] - 1, section="inventory"
                            )
                            data.set(tool, True, section="tools")

                    await _hunt.message.channel.send(
                        f":skull: You got killed by: `{item}`, you lost a level, EXP and your equipped tools"
                    )
                else:
                    data["cooldown"]["hunt"] = 60
                    data["inventory"][item] += 1
                    data["status"]["health"] -= item_data[data["tools"]["sword"]]
                    data["stats"]["current_exp"] = 5.0

                    if rng_break == 2:
                        data["inventory"][data["tools"]["sword"]] -= 1
                        await _hunt.message.channel.send(
                            f":warning: Your `{data['tools']['sword']}` is broken"
                        )

                    embed = discord.Embed(title="hunt", color=0xFF00FF)
                    embed.description = f"You killed a(n) `{item}` and You lost {item_data[data['tools']['sword']]} Health Points"
                    embed.set_author(name=_hunt.message.author.display_name)

                    await _hunt.message.channel.send(embed=embed)

                    data["tools"]["sword"] = True

            elif len(item_data) == 0:
                data["cooldown"]["hunt"] = 60
                data["inventory"][item] += 1
                data["stats"]["current_exp"] = 5.0

                embed = discord.Embed(title="hunt", color=0xFF00FF)
                embed.description = f"You killed a(n) `{item}`"
                embed.set_author(name=_hunt.message.author.display_name)

                await _hunt.message.channel.send(embed=embed)

            else:
                data.set("hunt", 60, section="cooldown")
                await _hunt.message.channel.send("You found nothing")

            data.write(filename)
