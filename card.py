from CardWriter import CardWriter
import enums
import string
import time
import json
import sys

class Effect:
    def __init__(self, input):
        self.effects = input[0]
        self.order = input[1]


class CardPrototype:
    base_imports = ["com.megacrit.cardcrawl.actions.GameActionManager",
                    "com.megacrit.cardcrawl.cards.AbstractCard",
                    "com.megacrit.cardcrawl.cards.AbstractCard.CardColour",
                    "com.megacrit.cardcrawl.cards.AbstractCard.CardRarity",
                    "com.megacrit.cardcrawl.cards.AbstractCard.CardTarget",
                    "com.megacrit.cardcrawl.cards.AbstractCard.CardType",
                    "com.megacrit.cardcrawl.characters.AbstractPlayer",
                    "com.megacrit.cardcrawl.dungeons.AbstractDungeon",
                    "com.megacrit.cardcrawl.monsters.AbstractMonster",
                    "com.megacrit.cardcrawl.core.CardCrawlGame",
                    "com.megacrit.cardcrawl.actions.common.ApplyPowerAction",
                    "com.megacrit.cardcrawl.powers.VulnerablePower",
                    "com.megacrit.cardcrawl.powers.WeakPower"]

    def __init__(self):
        self.effects = []
        self.has_target = False

    def check_string(self, _string):
        clean_str = " ".join(_string.split())
        for letter in clean_str:
            if letter not in string.ascii_letters and letter != " ":
                return False

        return True

    def set_type(self, card_type):
        conversion = {"attack": enums.CardType.ATTACK, "skill": enums.CardType.SKILL, "power": enums.CardType.POWER,
                      "status": enums.CardType.STATUS, "curse": enums.CardType.CURSE}

        if card_type not in conversion:
            raise TypeError("Invalid card type, please only use attack, skill, power, status, curse")

        else:
            self.type = conversion[card_type]

    def set_rarity(self, card_rarity):
        conversion = {"basic": enums.CardRarity.BASIC, "special": enums.CardRarity.SPECIAL,
                      "common": enums.CardRarity.COMMON, "uncommon": enums.CardRarity.UNCOMMON,
                      "rare": enums.CardRarity.RARE, "curse": enums.CardRarity.CURSE}

        if card_rarity not in conversion:
            raise ValueError("Invalid card rarity, please use only basic, special, common, uncommon, rare or curse")

        else:
            self.rarity = conversion[card_rarity]

    def set_colour(self, card_colour):
        conversion = {"red": enums.CardColour.RED, "green": enums.CardColour.GREEN, "blue": enums.CardColour.BLUE,
                      "curse": enums.CardColour.CURSE, "colourless": enums.CardColour.COLOURLESS}
        if card_colour not in conversion:
            raise ValueError("Invalid card colour entered, please use only red, green, blue, curse or colourless")

        else:
            self.colour = conversion[card_colour]

    def set_description(self, desc):
        if not self.check_string(desc):
            return "Card must only contain characters from the english alphabet and spaces"

        self.description = desc

    def set_name(self, name):
        if not self.check_string(name):
            return "Card must only contain characters from the english alphabet and spaces"

        self.name = name
        self.id = "{}{}".format(self.name, str(int(time.time())))

    def set_cost(self, cost):
        if type(cost) != int:
            raise TypeError("Cost must be int, not {}".format(type(cost)))

        elif cost > 999:
            raise ValueError("Energy costs cannot be more than 999")
        elif cost < 0:
            raise ValueError("Energy costs cannot be less than 0")

        else:
            self.cost = cost

    def set_target(self):
        # The first item in this list that is also set as a target in effects should be used as the target for the card
        hierarchy = ["self_and_enemy", "enemy", "all", "all_enemy", "self", "none"]
        conversion = {"self_and_enemy": enums.CardTarget.SELF_AND_ENEMY, "enemy": enums.CardTarget.ENEMY,
                      "all": enums.CardTarget.ALL, "all_enemy": enums.CardTarget.ALL_ENEMY,
                      "self": enums.CardTarget.SELF, "none": enums.CardTarget.NONE}
        card_targets = [x.effects["t"] for x in self.effects]
        for target in hierarchy:
            if target in card_targets:
                self.target = conversion[target]
                break

    def add_effect(self, effects):
        target = effects[0]["t"]
        if target in [enums.CardTarget.ENEMY, enums.CardTarget.SELF_AND_ENEMY] and self.has_target:
            raise ValueError("A card not use both enemy and self_and_enemy as a target")

        elif target in [x.target for x in self.effects]:
            raise ValueError("A card may only use each target type once")

        elif target == enums.CardTarget.ENEMY:
            self.has_target = True

        self.effects.append(Effect(effects))

    def import_json(self, input_json):
        try:
            for key in ["name", "cost", "colour", "rarity", "target", "description", "img_path", "effects"]:
                if key not in input_json:
                    raise KeyError("Required key {} not found in input".format(key))
            self.set_name(input_json["name"])
            self.set_cost(input_json["cost"])
            self.set_colour(input_json["colour"])
            self.set_rarity(input_json["rarity"])
            self.set_type(input_json["type"])
            self.set_description(input_json["description"])
            self.img_path = input_json["img_path"]
            effects = input_json["effects"]
            for i in effects:
                self.add_effect(i)

            self.set_target()
        except ValueError as e:
            print(e.message)
        self.finalize_card()

    def finalize_card(self):
        cw = CardWriter(self)
        cw.write_card()

card = CardPrototype()
with open(sys.argv[1], "rb") as file:
    input_json = json.loads(file.read())
    card.import_json(input_json)
