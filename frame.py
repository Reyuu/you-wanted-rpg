import random


def p(string):
    print(string)


def get():
    x = raw_input(">>>")
    return x


def choice(choicelist):
    for i in choicelist:
        p("%i. %s" % ((choicelist.index(i))+1, i))
    x = get()
    return x


def wait(timex):
    # 100 = 1s
    # 1000 = 10s
    # 10000 = 100s
    import time
    for i in range(0, timex):
        p(".")
        time.sleep(timex/timex)
    del time


def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    del os


class IncorrectPiece(Exception):
    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        return ("%s is not correct piece" % self.piece)


class ItemPiece(object):
    def __init__(self, name, stR, dex, inT, hp, ma, atk_p, atk_m, deF, val, piece, special_type=""):
        _piece = ["empty", "chest", "legs", "hands", "1hand", "2hand", "amulet", "head", "boots", "ring"]
        if piece not in _piece:
            raise IncorrectPiece(piece)
        self._par = {"name": name,
                     "str": stR,
                     "dex": dex,
                     "int": inT,
                     "hp": hp,
                     "ma": ma,
                     "atk_p": atk_p,
                     "atk_m": atk_m,
                     "def": deF,
                     "val": val,
                     "piece": piece,
                     "special_type": special_type}


class EQ:
    def __init__(self):
        self.EmptyPiece = ItemPiece("empty", 0, 0, 0, 0, 0, 0, 0, 0, 0, "empty")
        self._eq = {"chest": self.EmptyPiece,
                    "legs": self.EmptyPiece,
                    "hand": self.EmptyPiece,
                    "1hand": self.EmptyPiece,
                    "2hand": self.EmptyPiece,
                    "amulet": self.EmptyPiece,
                    "head": self.EmptyPiece,
                    "boots": self.EmptyPiece,
                    "ring": self.EmptyPiece}

    def equip(self, item):
        if item._par["piece"] is self._eq[item._par["piece"]]:
            self._eq.update({item._par["piece"]: item})

    def unequip(self, piece):
        self._eq.update({piece: self.EmptyPiece})

    def _gather_stats(self):
        self.stats = {"str": 0, "dex": 0, "int": 0, "hp": 0, "ma": 0, "atk_p": 0, "atk_m": 0, "def": 0}
        for j in self._eq:
            for i in ["str", "dex", "int", "hp", "ma", "atk_p", "atk_m", "def"]:
                self.stats[i] += self._eq[j]._par[i]
        return self.stats

class Level:
    def __init__(self, levels, xp_first, xp_last):
        from math import log, exp
        self._lvl = {}
        self.pretty_lvl_list_str = ""
        b = log(xp_last/xp_first)/(levels-1)
        a = xp_first/(exp(b) - 1.0)
        for i in range(0, levels+1):
            old_xp = int(a*exp(b*(i-1)))
            new_xp = int(a*exp(b*i))
            dictup = {str(i+2): [old_xp, new_xp, new_xp - old_xp]}
            self.pretty_lvl_list_str += str(dictup)+"\n"
            self._lvl.update(dictup)
        if "1" not in self._lvl.keys():
            dictup = {"1": [0, self._lvl["2"][0], self._lvl["2"][0]]}
            self.pretty_lvl_list_str = str(dictup)+"\n"+self.pretty_lvl_list_str
            self._lvl.update(dictup)
        del log, exp
        self.last_lvl = 1
        self.points = 0
        self.EXP = 0

    def check_level(self, exp):
        for i in self._lvl:
            if (self._lvl[i][0] < exp < self._lvl[i][1]):
                return int(i)
            else:
                pass

    def check_if_level_advanced(self, exp):
        if self.last_lvl is not self.check_level(exp):
            self.points += (self.check_level(exp) - self.last_lvl) * 5
            self.last_lvl = self.check_level(exp)
            return True
        else:
            return False

class SkillSystem:
    def __init__(self):
        """
        Skills:
        Physical Combat
        Magical Combat
        Elemental Magic
        Dark Magic
        Restoration Magic
        Defense Proficiency
        Exploration (loot/walking around)
        Speechcraft (merchats/story chars/npcs)
        Dodging
        Crafting
        """
        self.CombatP = 0.0
        self.CombatM = 0.0
        self.ElementalM = 0.0
        self.DarkM = 0.0
        self.RestorationM = 0.0
        self.Defense = 0.0
        self.Exploration = 0.0
        self.Speechcraft = 0.0
        self.Dodging = 0.0
        self.Crafting = 0.0
        self.StandardRatio = 0.01
        self.ExtremeRatio = 0.0001

    def add(self, skill, ratio):
        skill += ratio


class PlayerBase(object):
    def __init__(self, lvlargs, STR, DEX, INT, HP, MA):  # lvlargs type list
        self.pos_x = None
        self.pos_y = None
        self.EQ = EQ()
        self.skill = SkillSystem()
        self.gather = lambda stat: self.EQ._gather_stats()[stat]
        self.LVL_c = Level(lvlargs[0], lvlargs[1], lvlargs[2])  # LevelC
        self.base_STR = STR
        self.base_DEX = DEX
        self.base_INT = INT
        self.base_HP = HP
        self.base_MA = MA
        self.regenratio = 1
        self.STR = self.base_STR + self.gather("str")
        self.DEX = self.base_DEX + self.gather("dex")
        self.INT = self.base_INT + self.gather("int")
        self.HP = self.base_HP + self.gather("hp") + (self.base_STR / 2)
        self.currentHP = self.HP
        self.MA = self.base_MA + self.gather("ma") + (self.base_MA / 2)
        self.currentMA = self.MA
        self.ATK_P = self.gather("atk_p") + ((self.base_STR/100)*self.skill.CombatP) + self.STR
        self.ATK_M = self.gather("atk_m") + ((self.base_MA/100)*self.skill.CombatM) + self.INT
        self.DEF = self.gather("def") + ((self.skill.Defense))

    def update_stats(self):
        self.STR = self.base_STR + self.gather("str")
        self.DEX = self.base_DEX + self.gather("dex")
        self.INT = self.base_INT + self.gather("int")
        self.HP = self.base_HP + self.gather("hp")
        self.MA = self.base_MA + self.gather("ma")
        self.ATK_P = self.gather("atk_p") + ((self.base_STR/100)*self.skill.CombatP)
        self.ATK_M = self.gather("atk_m") + ((self.base_MA/100)*self.skill.CombatM)
        self.DEF = self.gather("def")


class EnemyBase:
    def __init__(self, name, EXP, STR, DEX, INT, HP, MA, ATK_P, ATK_M, DEF, bonushitchance):
        self.name = name
        self.EXP = EXP
        self.STR = STR
        self.DEX = DEX
        self.INT = INT
        self.HP = HP
        self.currentHP = self.HP
        self.MA = MA
        self.currentMA = self.MA
        self.ATK_P = ATK_P
        self.ATK_M = ATK_M
        self.DEF = DEF
        self.bonushitchance =  bonushitchance

    def after_fight(self):
        self.currentHP = self.HP
        self.currentMA = self.MA

class Fight:
    def check_if_death(self, clas):
        if clas.currentHP < 0 or clas.currentHP is 0:
            return True
        else:
            return False

    def check_if_fight(self, state):
        if state is "fight":
            return True
        else:
            return False

    def fight(self, Player, Enemy):
        Player_hitchance = int((Player.skill.CombatP + (Player.DEX) + (Player.STR/3) - (Enemy.DEX/4)))
        Enemy_hitchance = ((Enemy.DEX/2)+(Enemy.STR/2)+Enemy.bonushitchance - (Player.DEX/3))
        fight_state = "fight"
        who_first = random.randint(1, 2)

        def enemy_turn():
                #enemy turn
                #TODO dodge roll
                hitchance_roll = random.randint(0, 100)
                print("Enemy: %i : %i" % (hitchance_roll, Enemy_hitchance))
                if hitchance_roll < Enemy_hitchance:
                    #hit
                    atk_roll = random.randint(Enemy.ATK_P, int(Enemy.ATK_P+(Enemy.ATK_P/100)*1.4))
                    Player.currentHP -= atk_roll
                    p("You've been hit for %i, %iHP left" % (atk_roll, Player.currentHP))
                    if self.check_if_death(Player) is True:
                        fight_state = "player_dead"
                    else:
                        fight_state = "fight"
                if hitchance_roll > Enemy_hitchance:
                    p("%s missed!" % Enemy.name)
                    fight_state = "fight"
                #wait(3)
                return fight_state

        def player_turn():
            ch = choice(["attack", "try to flee", "manually change game state"])
            try:
                ch = int(ch)
            except:
                p("This wasn't a integer!")
            if ch is 1:
                #atk_p roll
                hitchance_roll = random.randint(0, 100)
                print("You: %i : %i" % (hitchance_roll, Player_hitchance))
                if hitchance_roll < Player_hitchance:
                    #hit
                    print("ATK roll: %i - %i" % (Player.ATK_P, int(Player.ATK_P+(Player.ATK_P/100)*1.4)))
                    atk_roll = random.randint(Player.ATK_P, int(Player.ATK_P+(Player.ATK_P/100)*1.4))
                    Enemy.currentHP -= atk_roll
                    p("You've hit %s for %i, %iHP left" % (Enemy.name, atk_roll, Enemy.currentHP))
                    fight_state = "fight"
                if hitchance_roll > Player_hitchance:
                    #miss
                    p("You've missed!")
                    fight_state = "fight"
            if ch is 2:
                #flee roll
                flee_roll = random.randint(0, 100)
                if flee_roll < Player.DEX+10:
                    fight_state = "fled"
                    p("You've fled!")
                else:
                    p("You've failed to flee!")
                    fight_state = "fight"
            if ch is 3:
                ch = choice(["player dead", "enemy dead", "fled"])
                try:
                    ch = int(ch)
                except:
                    print("That wasn't integer")
                if ch is 1:
                    fight_state = "player_dead"
                if ch is 2:
                    fight_state = "enemy_dead"
                if ch is 3:
                    fight_state = "fled"
            elif ch not in (1, 2, 3):
                p("Wrong command, you lose a turn! Be careful next time!")
            return fight_state



        if who_first is 1:
            p("%s has attacked you!\nWhat do you want to do?" % Enemy.name)
        if who_first is 2:
            p("%s has attacked you!" % Enemy.name)
        while ((Player.currentHP > 0) or (Enemy.currentHP > 0) or (fight_state is "fight") or (fight_state is not "fled")):
            if who_first is 1:
                fight_state = player_turn()
                if self.check_if_death(Enemy) is True:
                    fight_state = "enemy_dead"
                if self.check_if_fight(fight_state) is False:
                    break
                if fight_state is "fled":
                    break
                fight_state = enemy_turn()
                if self.check_if_death(Player) is True:
                    fight_state = "player_dead"
                if self.check_if_fight(fight_state) is False:
                    break
            if who_first is 2:
                fight_state = enemy_turn()
                if self.check_if_death(Player) is True:
                    fight_state = "player_dead"
                if self.check_if_fight(fight_state) is False:
                    break
                fight_state = player_turn()
                if self.check_if_death(Enemy) is True:
                    fight_state = "enemy_dead"
                if self.check_if_fight(fight_state) is False:
                    break
                if fight_state is "fled":
                    break
        clear()
        if fight_state == "enemy_dead":
            p("You've defeated the foe! Good job!")
            Enemy.after_fight()
            Player.LVL_c.EXP += Enemy.EXP
            wait(3)
        if fight_state == "player_dead":
            p("You are dead. Bad job!")
            wait(3)
        if fight_state == "fled":
            p("You've fled. Average job!")
            wait(3)
        return fight_state

"""
class Room(object):  #empty
    def __init__(self, drop=False, monster=False, lore=False, list_lines=['There is nothing in this room', 'Plain nothing']):
        self.drop = drop
        self.monster = monster
        self.lore = lore
        self.list_lines = "\n".join(list_lines)

    def __str__(self):
        return self.list_lines

class Monster(Room):
    def __init__(self, monster_cls, monster=True):
        self.monster_cls = monster_cls
        self.monster = True"""



#TODO Test chamber
#TODO Walking around
#TODO God-fukcking-damn fight
#TODO Random dungeon generator
#TODO SkillSystem
#TODO Crafting
