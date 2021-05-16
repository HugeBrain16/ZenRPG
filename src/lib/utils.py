import os
import time


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
