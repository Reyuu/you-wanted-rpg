import frame
import random
import os
from time import sleep


def p(string):
    print(string)


def choice(choicelist):
    for i in choicelist:
        p("%i. %s" % ((choicelist.index(i))+1, i))
    x = raw_input(">>>")
    return x


def wait(time):
    for i in range(0, time):
        p(".")
        sleep(time)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


"""def whose_turn(Player, Enemy):
    if (random.randint(1, 2)%2) is 0:
        return [Player, Enemy]
    else:
        return [Enemy, Player]"""


def check_if_death(clas):
    if clas.currentHP < 0 or clas.currentHP is 0:
        return True
    else:
        return False


def fight(Player, Enemy):
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
                if check_if_death(Player) is True:
                    fight_state = "player_dead"
            if hitchance_roll > Enemy_hitchance:
                p("%s missed!" % Enemy.name)
            #wait(3)

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
            if hitchance_roll > Player_hitchance:
                #miss
                p("You've missed!")
        if ch is 2:
            #flee roll
            flee_roll = random.randint(0, 100)
            if flee_roll < Player.DEX+10:
                fight_state = "fled"
                p("You've fled!")
            else:
                p("You've failed to flee!")
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

    def check_if_fight(state):
        if state is "fight":
            return True
        else:
            return False

    if who_first is 1:
        p("%s has attacked you!\nWhat do you want to do?" % Enemy.name)
    if who_first is 2:
        p("%s has attacked you!" % Enemy.name)
    while ((Player.currentHP > 0) or (Enemy.currentHP > 0) or (fight_state is "fight")):
        if who_first is 1:
            player_turn()
            if check_if_death(Enemy) is True:
                fight_state = "enemy_dead"
            if check_if_fight(fight_state) is False:
                break
            enemy_turn()
            if check_if_death(Player) is True:
                fight_state = "player_dead"
            if check_if_fight(fight_state) is False:
                break
        if who_first is 2:
            enemy_turn()
            if check_if_death(Player) is True:
                fight_state = "player_dead"
            if check_if_fight(fight_state) is False:
                break
            player_turn()
            if check_if_death(Enemy) is True:
                fight_state = "enemy_dead"
            if check_if_fight(fight_state) is False:
                break
    clear()
    if fight_state == "enemy_dead":
        p("You've defeated the foe! Good job!")
        Player.LVL_c.EXP += Enemy.EXP
    if fight_state == "player_dead":
        p("You are dead. Bad job!")
    if fight_state == "fled":
        p("You've fled. Average job!")
    return fight_state

Player = frame.PlayerBase([50, 10, 100000000], 10, 4, 2, 20, 10)
Enemy = frame.EnemyBase("Goblin", 500, 9, 5, 3, 20, 10, 4, 5, 3, 5)
fight(Player, Enemy)
if Player.LVL_c.check_if_level_advanced(Player.LVL_c.EXP):
    p("Your level has advanced! You are level %i and you have %i points!" % (Player.LVL_c.check_level(Player.LVL_c.EXP),
                                                                             Player.LVL_c.points))


