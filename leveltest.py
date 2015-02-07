#!/usr/bin/env python
'''Generate a perfect maze, that is a maze with
    * all included points connected (no isolated passages) and
    * no loops (only one path between any two points).
The size and branching factor of the maze can be adjusted.

Coding by d.factorial [at] gmail.com.
'''
import random

#the dimensions of the maze

xwide, yhigh = 40, 20

#the grid of the maze
#each cell of the maze is one of the following:
    # '#' is wall
    # '.' is empty space
    # ',' is exposed but undetermined
    # '?' is unexposed and undetermined
field = []

for y in range(yhigh):
    row = []
    for x in range(xwide):
        row.append('?')
    field.append(row)

#list of coordinates of exposed but undetermined cells.
frontier = []

def carve(y, x):
    '''Make the cell at y,x a space.
    
    Update the fronteer and field accordingly.
    Note: this does not remove the current cell from frontier, it only adds new cells.
    '''
    extra = []
    field[y][x] = '.'
    if x > 0:
        if field[y][x-1] == '?':
            field[y][x-1] = ','
            extra.append((y,x-1))
    if x < xwide - 1:
        if field[y][x+1] == '?':
            field[y][x+1] = ','
            extra.append((y,x+1))
    if y > 0:
        if field[y-1][x] == '?':
            field[y-1][x] = ','
            extra.append((y-1,x))
    if y < yhigh - 1:
        if field[y+1][x] == '?':
            field[y+1][x] = ','
            extra.append((y+1,x))
    random.shuffle(extra)
    frontier.extend(extra)

def harden(y, x):
    '''Make the cell at y,x a wall.
    '''
    field[y][x] = '#'



def check(y, x, nodiagonals = True):
    '''Test the cell at y,x: can this cell become a space?
    
    True indicates it should become a space,
    False indicates it should become a wall.
    '''
    
    edgestate = 0
    if x > 0:
        if field[y][x-1] == '.':
            edgestate += 1
    if x < xwide-1:
        if field[y][x+1] == '.':
            edgestate += 2
    if y > 0:
        if field[y-1][x] == '.':
            edgestate += 4
    if y < yhigh-1:
        if field[y+1][x] == '.':
            edgestate += 8
    
    if nodiagonals:
        #if this would make a diagonal connecition, forbid it
            #the following steps make the test a bit more complicated and are not necessary,
            #but without them the mazes don't look as good
        if edgestate == 1:
            if x < xwide-1:
                if y > 0:
                    if field[y-1][x+1] == '.':
                        return False
                if y < yhigh-1:
                    if field[y+1][x+1] == '.':
                        return False
            return True
        elif edgestate == 2:
            if x > 0:
                if y > 0:
                    if field[y-1][x-1] == '.':
                        return False
                if y < yhigh-1:
                    if field[y+1][x-1] == '.':
                        return False
            return True
        elif edgestate == 4:
            if y < yhigh-1:
                if x > 0:
                    if field[y+1][x-1] == '.':
                        return False
                if x < xwide-1:
                    if field[y+1][x+1] == '.':
                        return False
            return True
        elif edgestate == 8:
            if y > 0:
                if x > 0:
                    if field[y-1][x-1] == '.':
                        return False
                if x < xwide-1:
                    if field[y-1][x+1] == '.':
                        return False
            return True
        return False
    else:
        #diagonal walls are permitted
        if  [1,2,4,8].count(edgestate):
            return True
        return False
    

#choose a original point at random and carve it out.
xchoice = random.randint(0, xwide-1)
ychoice = random.randint(0, yhigh-1)
carve(ychoice,xchoice)

#parameter branchrate:
    #zero is unbiased, positive will make branches more frequent, negative will cause long passages
    #this controls the position in the list chosen: positive makes the start of the list more likely,
    #negative makes the end of the list more likely

    #large negative values make the original point obvious

    #try values between -10, 10
branchrate = 5

from math import e

while(len(frontier)):
    #select a random edge
    pos = random.random()
    pos = pos**(e**-branchrate)
    choice = frontier[int(pos*len(frontier))]
    if check(*choice):
        carve(*choice)
    else:
        harden(*choice)
    frontier.remove(choice)
    
#set unexposed cells to be walls
for y in range(yhigh):
    for x in range(xwide):
        if field[y][x] == '?':
            field[y][x] = '#'

#print the maze
for y in range(yhigh):
    s = ""
    for x in range(xwide):
        s += field[y][x]
    print(s)