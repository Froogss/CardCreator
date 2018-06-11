import enums
class CardWriter:
    base_initial_vars = {"id": "String ID = \"{}\"", "name": "String NAME = \"{}\"", "description": "String DESCRIPTION = \"{}\"", "img_path": "String IMG_PATH = \"{}\"", "cost": "int COST = {}"}
    super_format = "super(\"{id}\", \"{name}\", \"{img_path}\", {cost}, \"{desc}\", {type}, {colour}, {rarity}, {target});"

    substitutions = {}

    def __init__(self, proto):
        self.proto = proto
        self.indent_level = 0
        self.file = open("{}{}".format(proto.id, ".java"), "w")

    def write_card(self):
        for _import in self.proto.base_imports:
            self.write_line("import {};".format(_import))

        self.write_line("\nimport basemod.abstracts.CustomCard;\n")

        self.write_line("public class {}\nextends CustomCard {{".format(self.proto.id))
        super_call = {"id": self.proto.id, "name": "NAME", "img_path": self.proto.img_path, "cost": self.proto.cost,
                      "desc": "DESCRIPTION", "type": self.proto.type, "colour": self.proto.colour,
                      "rarity": self.proto.rarity, "target": self.proto.target}

        for line in self.base_initial_vars.items():
            self.write_line("public static final {};".format(line[1]).format(getattr(self.proto, line[0])))

        self.write_line("public {}() {{".format(self.proto.id))
        self.write_line(self.super_format.format(**super_call))
        self.write_line("}\n")
        self.use_method()
        self.write_line("}\n")
        self.write_line("@Override")
        self.write_line("public AbstractCard makeCopy() {")
        self.write_line("return new {}();".format(self.proto.id))
        self.write_line("}\n")
        self.write_line("@Override")
        self.write_line("public void upgrade() {")
        self.write_line("if (!this.upgraded) {")
        self.write_line("upgradeName();")
        self.write_line("}")
        self.write_line("}")
        self.write_line("}")
        self.file.close()



    def write_line(self, line):
        if line == "}" or line == "}\n":
            self.indent_level -= 1
        new_line = "{}{}{}".format(("  " * self.indent_level), line, "\n")
        self.file.write(new_line)

        # Iterate through the characters in the line in reverse to see if the line ends with { not counting \n
        for i in range(1, len(line)):
            char = line[i*-1]

            if char not in ["\n", "{"]:
                break

            elif char == "{":
                self.indent_level += 1
                break

            else:
                break

    def format_use_var(self):
        effects = [x.effects["t"] for x in self.proto.effects]
        if enums.CardTarget.ENEMY in effects or enums.CardTarget.SELF_AND_ENEMY in effects:
            self.write_line("public void use(AbstractPlayer p, AbstractMonster m) {")

        else:
            self.write_line("public void use(AbstractPlayer p) {")

    def use_method(self):
        self.write_line("@Override")
        self.format_use_var()
        for eff in self.proto.effects:
            for order in eff.order:
                if order == "a":
                    self.write_line("AbstractDungeon.actionManager.addToBottom(new GainBlockAction(p, p, {}));".format(eff.effects["a"]))

                if order == "d":
                    self.write_line("AbstractDungeon.actionManager.addToBottom(new DamageAction(m, new DamageInfo(p, {}, this.damageTypeForTurn), AbstractGameAction.AttackEffect.SLASH_DIAGONAL);)".format(eff.effects["d"]))

                if order == "w":
                    self.write_line("AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(mo, p, new WeakPower(mo, {}, false), {}, true, AbstractGameAction.AttackEffect.NONE));".format(eff.effects["w"], eff.effects["w"]))

                if order == "v":
                    self.write_line("AbstractDungeon.actionManager.addToBottom(new ApplyPowerAction(mo, p, new VulnerablePower(mo, {}, false), {}, true, AbstractGameAction.AttackEffect.NONE));".format(eff.effects["v"], eff.effects["v"]))


