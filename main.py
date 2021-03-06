from frame import *
from maze_random import Maze
from os import _exit


Player = PlayerBase([50, 10, 100000000], 10, 4, 2, 20, 10)
Maze_c = Maze(20, 20, Player)
clear()
Maze_c.start_player_at_maze(3, 3)

while 1:
    x = get()
    if x == "w":
        Maze_c.move(Player.pos_x, Player.pos_y-1)
    if x == "s":
        Maze_c.move(Player.pos_x, Player.pos_y+1)
    if x == "a":
        Maze_c.move(Player.pos_x-1, Player.pos_y)
    if x == "d":
        Maze_c.move(Player.pos_x+1, Player.pos_y)
    if x == "c":
        for i in (Player.LVL_c.EXP, Player.LVL_c.check_if_level_advanced()):
            p(i)
    if "e.." in x:
        y = x.split("e..")[1]
        if "self." in y:
            y = y.replace("self.", "Player.")
        exec(y)
    if "p.." in x:
        y = x.split("p..")[1]
        if "self." in y:
            y = y.replace("self.", "Player.")
        exec("y = %s" % (y))
        p(y)
    if x == "eval..":
        p("eval mode engaged")
        while 1:
            x = get()
            if "exit..eval" in x:
                p("eval mode disengaged")
                break
            else:
                exec(x)

    if x == "q":
        credits()
        _exit(1)
    if x == "qq":
        _exit(1)

#Fight test
#Enemy = EnemyBase("Goblin", 500, 9, 5, 3, 20, 10, 4, 5, 3, 5)
#Fight().fight(Player, Enemy)
#if Player.LVL_c.check_if_level_advanced(Player.LVL_c.EXP):
#    p("Your level has advanced! You are level %i and you have %i points!" % (Player.LVL_c.check_level(Player.LVL_c.EXP),
#                                                                             Player.LVL_c.points))
