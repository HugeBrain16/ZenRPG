import os
import iniparser2


def get_commands():
    result = []

    for file in os.listdir("commands"):
        if os.path.isfile("commands/" + file):
            if file.endswith(".py"):
                if file not in ["__init__.py", "__main__.py"]:
                    result.append(file.split(".py")[0])

    return result


def get_assigned_user_ids():
    result = []

    for file in os.listdir("data/users"):
        if os.path.isfile("data/users/" + file):
            if file.endswith(".ini"):
                result.append(int(file.split(".ini")[0]))

    return result


def mention_to_id(mention):
    return int(
        mention.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
    )


def get_fields():
    result = []

    for file in os.listdir("data/fields"):
        if os.path.isfile("data/fields/" + file):
            if file.endswith(".ini"):
                result.append(int(file.split(".ini")[0]))

    return result


def get_guilds():
    guilds_file = []

    for guild in os.listdir("data/guilds"):
        if os.path.isfile("data/guilds/" + guild):
            if guild.endswith(".ini"):
                guilds_file.append("data/guilds/" + guild)

    guilds = []

    for guild in guilds_file:
        data = iniparser2.INI(convert_property=True)
        data.read_file(guild)

        guilds.append(
            {
                "id": int(os.path.basename(guild).split(".ini")[0]),
                "name": data["info"]["name"],
                "leader": data["info"]["leader"],
                "members": len(data["members"].keys()),
            }
        )

    return guilds


def get_guilds_data():
    guilds_file = []

    for guild in os.listdir("data/guilds"):
        if os.path.isfile("data/guilds/" + guild):
            if guild.endswith(".ini"):
                guilds_file.append("data/guilds/" + guild)

    guilds = []

    for guild in guilds_file:
        data = iniparser2.INI(convert_property=True)
        data.read_file(guild)

        guilds.append(data)

    return guilds


def get_guilds_name():
    guilds = get_guilds()
    names = []

    for guild in guilds:
        names.append(guild["name"])

    return names


def get_guild_members_id(guild_id):
    members = []
    filename = f"data/guilds/{guild_id}.ini"

    if os.path.isfile(filename):
        guild = iniparser2.INI(convert_property=True)
        guild.read_file(filename)

        for member in guild["members"].keys():
            members.append(int(member))

        return members


def get_guilds_id():
    ids = []

    for gid in os.listdir("data/guilds"):
        if gid.endswith(".ini"):
            ids.append(int(gid.split(".ini")[0]))

    return ids


def new_guild_id():
    ids = get_guilds_id()

    if len(ids) > 0:
        return ids[len(ids) - 1] + 1

    else:
        return 0


def fsec(x):
    if (x / 60) < 1:
        if x == 1:
            return f"1 second"

        else:
            return f"{x} seconds"

    elif (x / 60) >= 1 and (x / 3600) < 1:
        if int(x / 60) == 1:
            return f"1 minute"

        else:
            return f"{int(x/60)} minutes"

    elif (x / 3600) >= 1 and (x / 86400) < 1:
        if int(x / 3600) == 1:
            return f"1 hour"

        else:
            return f"{int(x / 3600)} hours"

    elif (x / 86400) >= 1 and (x / 2628002.88) < 1:
        if int(x / 86400) == 1:
            return f"1 day"

        else:
            return f"{int(x/86400)} days"

    elif (x / 2628002.88) >= 1:
        if int(x / 2628002.88) == 1:
            return f"1 month"

        else:
            return f"{int(x/2628002.88)} months"
