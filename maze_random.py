#!/usr/bin/env python
# -*- coding: utf-8 -*
'''Generate a perfect maze, that is a maze with
    * all included points connected (no isolated passages) and
    * no loops (only one path between any two points).
The size and branching factor of the maze can be adjusted.

Coding by d.factorial [at] gmail.com.
Class refactorization and code change rey444xd3 [at] gmail.com
'''
from frame import *

class Enemies(object):
    def __init__(self, mazelvl):
        self.instances = [
            [EnemyBase("Crab", 4, 3, 2, 0, 5, 5, 4, 0, 3, 5), EnemyBase("Bat", 8, 5, 4, 0, 7, 0, 3, 0, 1, 3),
             EnemyBase("Fox", 6, 4, 6, 0, 10, 0, 5, 0, 2, 10), EnemyBase("Wolf", 15, 8, 4, 0, 13, 0, 7, 0, 5, 7),
            EnemyBase("Kobold", 6, 4, 7, 2, 10, 0, 7, 0, 2, 10)],
            [],
            [],
            [],
            [],
            []
        ]
        self.monsters = []
        if mazelvl in range(0, 11):
            for i in self.instances[0]:
                self.monsters.append(i)
        if mazelvl in range(5, 16):
            for i in self.instances[1]:
                self.monsters.append(i)
        if mazelvl in range(10, 21):
            for i in self.instances[2]:
                self.monsters.append(i)
        if mazelvl in range(15, 26):
            for i in self.instances[3]:
                self.monsters.append(i)
        if mazelvl in range(25, 31):
            for i in self.instances[4]:
                self.monsters.append(i)
        if mazelvl is 31:
            #final boss
            self.monsters = []
            self.monsters.append(self.instances[5][0])

class Room(object):
    def __init__(self, symbol, type="empty", *args):
        self.symbol = symbol
        self.type = type
        self.args = args

        if self.type == "wall":
            self.collision = True
            self.fight = False

        if self.type == "enemy":
            self.collision = False
            self.fight = True
            try:
                self.enemy_cls = self.args[0]
            except IndexError:
                self.enemy_cls = None

        if self.type == "empty":
            self.collision = False
            self.fight= False


        #else:
        #    self.collision = True
        #    self.enemy = False


class Maze(object):
    def __init__(self, xwide, yhigh, player_cls):
        self.xwide = xwide
        self.yhigh = yhigh
        self.Player = player_cls
        self.lvl = 1

        #the grid of the maze
        #each cell of the maze is one of the following:
            # '#' is wall
            # '.' is empty space
            # ',' is exposed but undetermined
            # '?' is unexposed and undetermined
        self.field = []

        for y in range(self.yhigh):
            row = []
            for x in range(self.xwide):
                row.append('?')
            self.field.append(row)

        #list of coordinates of exposed but undetermined cells.
        self.frontier = []
        self.create()
        for y in range(self.yhigh):
            for x in range(self.xwide): # #.E
                if self.field[y][x] is "#":
                    self.field[y][x] = Room("#", "wall")
                if self.field[y][x] is ".":
                    self.field[y][x] = Room(".", "empty")
                if self.field[y][x] is "E":
                    monster = random.choice(Enemies(self.lvl).monsters)
                    self.field[y][x] = Room("E", "enemy", monster)

    def carve(self, y, x):
        '''Make the cell at y,x a space.

        Update the frontier and field accordingly.
        Note: this does not remove the current cell from frontier, it only adds new cells.
        '''
        self.extra = []
        self.field[y][x] = '.'
        if x > 0:
            if self.field[y][x-1] == '?':
                self.field[y][x-1] = ','
                self.extra.append((y,x-1))
        if x < self.xwide - 1:
            if self.field[y][x+1] == '?':
                self.field[y][x+1] = ','
                self.extra.append((y,x+1))
        if y > 0:
            if self.field[y-1][x] == '?':
                self.field[y-1][x] = ','
                self.extra.append((y-1,x))
        if y < self.yhigh - 1:
            if self.field[y+1][x] == '?':
                self.field[y+1][x] = ','
                self.extra.append((y+1,x))
        random.shuffle(self.extra)
        self.frontier.extend(self.extra)

    def harden(self, y, x):
        '''Make the cell at y,x a wall.
        '''
        self.field[y][x] = '#'



    def check(self, y, x, nodiagonals = True):
        '''Test the cell at y,x: can this cell become a space?

        True indicates it should become a space,
        False indicates it should become a wall.
        '''

        edgestate = 0
        if x > 0:
            if self.field[y][x-1] == '.':
                edgestate += 1
        if x < self.xwide-1:
            if self.field[y][x+1] == '.':
                edgestate += 2
        if y > 0:
            if self.field[y-1][x] == '.':
                edgestate += 4
        if y < self.yhigh-1:
            if self.field[y+1][x] == '.':
                edgestate += 8

        if nodiagonals:
            #if this would make a diagonal connection, forbid it
                #the following steps make the test a bit more complicated and are not necessary,
                #but without them the mazes don't look as good
            if edgestate == 1:
                if x < self.xwide-1:
                    if y > 0:
                        if self.field[y-1][x+1] == '.':
                            return False
                    if y < self.yhigh-1:
                        if self.field[y+1][x+1] == '.':
                            return False
                return True
            elif edgestate == 2:
                if x > 0:
                    if y > 0:
                        if self.field[y-1][x-1] == '.':
                            return False
                    if y < self.yhigh-1:
                        if self.field[y+1][x-1] == '.':
                            return False
                return True
            elif edgestate == 4:
                if y < self.yhigh-1:
                    if x > 0:
                        if self.field[y+1][x-1] == '.':
                            return False
                    if x < self.xwide-1:
                        if self.field[y+1][x+1] == '.':
                            return False
                return True
            elif edgestate == 8:
                if y > 0:
                    if x > 0:
                        if self.field[y-1][x-1] == '.':
                            return False
                    if x < self.xwide-1:
                        if self.field[y-1][x+1] == '.':
                            return False
                return True
            return False
        else:
            #diagonal walls are permitted
            if  [1,2,4,8].count(edgestate):
                return True
            return False

    def create(self, branchrate=5):
        #choose a original point at random and carve it out.
        xchoice = random.randint(0, self.xwide-1)
        ychoice = random.randint(0, self.yhigh-1)
        self.carve(ychoice,xchoice)

        #parameter branchrate:
            #zero is unbiased, positive will make branches more frequent, negative will cause long passages
            #this controls the position in the list chosen: positive makes the start of the list more likely,
            #negative makes the end of the list more likely

            #large negative values make the original point obvious

            #try values between -10, 10

        from math import e

        while(len(self.frontier)):
            #select a random edge
            pos = random.random()
            pos = pos**(e**-branchrate)
            choice = self.frontier[int(pos*len(self.frontier))]
            if self.check(*choice):
                self.carve(*choice)
            else:
                self.harden(*choice)
            self.frontier.remove(choice)

        #set unexposed cells to be walls
        for y in range(self.yhigh):
            for x in range(self.xwide):
                if self.field[y][x] == '?':
                    self.field[y][x] = '#'
        #random enemies
        monsters = abs(random.randint(5, 30))
        print "Number of monsters: %i" % monsters
        counter = 0
        for y in range(self.yhigh):
            for x in range(self.xwide):
                z = random.randint(0, 20)
                if z is 1:
                    if self.field[y][x] is ("#" or "E"):
                        pass
                    else:
                        self.field[y][x] = "E"
                        counter += 1
                if counter is monsters:
                    break
            if counter is monsters:
                break
        return self.field
        #print the maze
    def print_maze(self):
        for y in range(self.yhigh):
            s = ""
            for x in range(self.xwide):
                s += self.field[y][x].symbol
            print(s)

    def start_player_at_maze(self, px, py):
        collisions = []
        z = ""
        self.Player.pos_x = px
        self.Player.pos_y = py
        for y in range(self.yhigh):
            s = ""
            if y is py:
                for x in range(self.xwide):
                    if x is px:
                        #s = list(s)
                        if self.field[y][x].collision is True:
                            collisions.append((py, px))
                            px = random.randrange(0, self.xwide)
                            py = random.randrange(0, self.yhigh)
                            s += self.field[y][x].symbol
                        else:
                            s += "@"
                            self.Player.pos_x = x
                            self.Player.pos_y = y
                    else:
                        s += self.field[y][x].symbol
                z += s

            else:
                for x in range(self.xwide):
                    s += self.field[y][x].symbol
                z += s
            print(s)
        if "@" not in z:
            px = random.randrange(0, self.xwide)
            py = random.randrange(0, self.yhigh)
            clear()
            self.start_player_at_maze(px, py)
        print "Player position: %i, %i" % (px, py)
        print("%i/%i HP" % (self.Player.currentHP, self.Player.HP))
        if len(collisions) is not 0: print("Bouncing collisions at %s" % collisions); return collisions

    def print_player_at_maze(self, px, py):
        collisions = []
        z = ""
        for y in range(self.yhigh):
            s = ""
            if y is py:
                for x in range(self.xwide):
                    if x is px:
                        s += "@"
                        self.Player.pos_x = x
                        self.Player.pos_y = y
                    else:
                        s += self.field[y][x].symbol
                z += s

            else:
                for x in range(self.xwide):
                    s += self.field[y][x].symbol
                z += s
            print(s)
        #if "@" not in z:
        #    clear()
        #    self.print_player_at_maze(px, py)
        print("Player position: %i, %i" % (px, py))
        print("%i/%i HP" % (self.Player.currentHP, self.Player.HP))
        if len(collisions) is not 0: print("Bouncing collisions at %s" % collisions); return collisions

    def move(self, px, py):
        clear()
        printed = False
        #IndexError countermeasure
        try:
            collision = self.field[py][px].collision
            enemy_ = self.field[py][px].fight
        except IndexError:
            collision = True
            enemy_ = False
        #exceeding the playfield
        if px < 0:
            px = 0
        if px > self.xwide:
            px = self.xwide
        if py < 0:
            py = 0
        if py > self.yhigh:
            py = self.yhigh
        #fight tests
        if enemy_ is True:
            #print self.field[py][px].enemy_cls
            outcome = Fight().fight(self.Player, self.field[py][px].enemy_cls)
            if outcome is "enemy_dead":
                self.field[py][px] = Room(".")
            if outcome is "player_dead":
                p("So sorry, you have to leave the maze")
                import os
                os._exit(1)
            if outcome is "fled":
                self.Player.pos_x = self.Player.pos_x
                self.Player.pos_y = self.Player.pos_y
                self.print_player_at_maze(self.Player.pos_x, self.Player.pos_y)
                printed = True

        if enemy_ is False:
            pass
        #collisions tests
        if printed is False:
            if collision is True:
                self.Player.pos_x = self.Player.pos_x
                self.Player.pos_y = self.Player.pos_y
                self.print_player_at_maze(self.Player.pos_x, self.Player.pos_y)
            if collision is False:
                self.Player.pos_x = px
                self.Player.pos_y = py
                self.print_player_at_maze(self.Player.pos_x, self.Player.pos_y)
                self.Player.currentHP += self.Player.regenratio
                if self.Player.currentHP >= self.Player.HP:
                    self.Player.currentHP = self.Player.HP
                self.Player.currentMA += self.Player.regenratio
                if self.Player.currentMA >= self.Player.MA:
                    self.Player.currentMA = self.Player.MA
#TODO Monsters generator --fast
#20:21:15<@Marcin> obiekt player, metoda move(x, z), player przekazany print_maze
#20:17:41<@Marcin> używasz arraya z dwoma elementami zamiast obiektu z wartościami x  oraz z

