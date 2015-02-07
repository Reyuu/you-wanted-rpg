#!/usr/bin/env python
# -*- coding: utf-8 -*
'''Generate a perfect maze, that is a maze with
    * all included points connected (no isolated passages) and
    * no loops (only one path between any two points).
The size and branching factor of the maze can be adjusted.

Coding by d.factorial [at] gmail.com.
Class refactorization rey444xd3 [at] gmail.com
'''
import random


class Maze(object):
    def __init__(self, xwide, yhigh):
        self.xwide = xwide
        self.yhigh = yhigh


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
            #if this would make a diagonal connecition, forbid it
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
        return self.field

        #print the maze
    def print_maze(self):
        for y in range(self.yhigh):
            s = ""
            for x in range(self.xwide):
                s += self.field[y][x]
            print(s)



#20:21:15<@Marcin> obiekt player, metoda move(x, z), player przekazany print_maze
#20:17:41<@Marcin> używasz arraya z dwoma elementami zamiast obiektu z wartościami x  oraz z

