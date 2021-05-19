hunt = {
    "boar": {"wooden_sword": 5.0, "stone_sword": 3.0, "iron_sword": 1.5},
    "bird": {},
    "squirrel": {},
    "rabbit": {},
}
mine = {
    "stone": {"wooden_pickaxe": 1, "stone_axe": 2, "iron_axe": 3},
    "coal": {"wooden_pickaxe": 1, "stone_pickaxe": 2, "iron_pickaxe": 3},
    "iron": {"stone_pickaxe": 1, "iron_pickaxe": 2},
}
chop = {"wooden_axe": 2, "stone_axe": 3, "iron_axe": 4}
cooldowns = ["hunt", "chop", "fish", "mine", "forage"]
tools = ["axe", "pickaxe", "sword"]
items = {
    "squirrel": {"price": 13, "purchasable": False, "sellable": True},
    "rabbit": {"price": 20, "purchasable": False, "sellable": True},
    "boar": {"price": 30, "purchasable": False, "sellable": True},
    "bird": {"price": 10, "purchasable": False, "sellable": True},
    "iron": {"price": 40, "purchasable": True, "sellable": True},
    "coal": {"price": 25, "purchasable": True, "sellable": True},
    "wood": {"price": 10, "purchasable": True, "sellable": True},
    "stone": {"price": 15, "purchasable": True, "sellable": True},
    "leather": {"price": 30, "purchasable": False, "sellable": True},
    "fish": {"price": 18, "purchasable": False, "sellable": True},
    "fishing_rod": {"price": 200, "purchasable": True, "sellable": False},
    "stick": {"price": 5, "purchasable": False, "sellable": True},
    "wooden_axe": {"price": 30, "purchasable": True, "sellable": True},
    "wooden_pickaxe": {"price": 45, "purchasable": True, "sellable": True},
    "stone_axe": {"price": 60, "purchasable": True, "sellable": True},
    "stone_pickaxe": {"price": 70, "purchasable": True, "sellable": True},
    "iron_axe": {"price": 100, "purchasable": True, "sellable": True},
    "iron_pickaxe": {"price": 120, "purchasable": True, "sellable": True},
    "wooden_sword": {"price": 40, "purchasable": True, "sellable": True},
    "stone_sword": {"price": 80, "purchasable": True, "sellable": True},
    "iron_sword": {"price": 100, "purchasable": True, "sellable": True},
    "cotton": {"price": 12, "purchasable": False, "sellable": True},
    "string": {"price": 20, "purchasable": False, "sellable": True},
    "berry": {"price": 8, "purchasable": True, "sellable": True},
    "mushroom": {"price": 9, "purchasable": True, "sellable": True},
    "health_potion": {"price": 100, "purchasable": True, "sellable": False},
    "potato_seed": {"price": 20, "purchasable": True, "sellable": True},
    "carrot_seed": {"price": 18, "purchasable": True, "sellable": True},
    "potato": {"price": 65, "purchasable": True, "sellable": True},
    "carrot": {"price": 50, "purchasable": True, "sellable": True},
}
consumable = {"berry": 10.0, "mushroom": 8.5, "health_potion": 50.0}
forage = ["berry", "cotton", "mushroom", "potato_seed", "carrot_seed"]
farm = {"potato": 60 * 5, "carrot": 60 * 3}
help = {
    "help": "Show this menu",
    "inventory": "view your inventory",
    "chop": "chop woods from the forest",
    "hunt": "hunt creatures from the forest",
    "balance": "view your balance",
    "start": "start your journey!",
    "player": "display player/user info",
    "ping": "pong",
    "sell": "sell your items",
    "about": "about this bot",
    "guild_list": "Display list of created guilds",
    "guild_create": "Create a new guild",
}
craft = {
    "stick": {"recipes": {"wood": 1}, "result": 3},
    "string": {"recipes": {"cotton": 5}, "result": 3},
    "health_potion": {"recipes": {"berry": 3, "herb_leaf": 5}, "result": 1},
    "fishing_rod": {"recipes": {"stick": 10, "string": 5}, "result": 1},
    "leather": {"recipes": {"boar": 1}, "result": 2},
    "wooden_axe": {"recipes": {"wood": 3, "stick": 2}, "result": 1},
    "wooden_pickaxe": {"recipes": {"wood": 3, "stick": 2}, "result": 1},
    "stone_axe": {"recipes": {"stone": 3, "stick": 2}, "result": 1},
    "stone_pickaxe": {"recipes": {"stone": 3, "stick": 2}, "result": 1},
    "iron_axe": {"recipes": {"iron": 3, "stick": 2}, "result": 1},
    "iron_pickaxe": {"recipes": {"iron": 3, "stick": 2}, "result": 1},
    "iron_sword": {"recipes": {"iron": 2, "stick": 1}, "result": 1},
    "wooden_sword": {"recipes": {"wood": 2, "stick": 1}, "result": 1},
}
