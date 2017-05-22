#!/usr/bin/env python3
# the above line is so that the script can run standalone. I think it's automatically going: python 'file' instead of making you do it manually

import sys
import turtle
import random
#how are you supposed to know what to import....idk

CELL_SIZE = 10 #measured in pixels, takes forever to render with anything under 10, completely freezes on 1, most of the time can't even do anything after that without freezing

class LifeBoard:
    """Encapsulates a Life board

    Attributes:
    xsize, ysize : horizontal and vertical size of the board
    state : set containing (x,y) coordinates for live cells.

    Methods:
    display(update_board) -- Display the state of the board on-screen.
    erase() -- clear the entire board
    makeRandom() -- fill the board randomly
    set(x,y) -- set the given cell to Live; doesn't refresh the screen
    toggle(x,y) -- change the given cell from live to dead, or vice
                   versa, and refresh the screen display

    """
    # documentation block. 
    def __init__(self, x, y):
        """create new LifeBoard instance.
        scr -- curses screen object to use for display
        char -- character to use for live cells
        """
        self.state = set()
        self.x, self.y = x,y

    def is_legal(self,x,y):
        return (0 <= x < self.x) and (0 <= y < self.y)

    def set(self,x,y):
        if self.is_legal(x,y):
            key = (x,y)
            self.state.add(key)

    def makeRandom(self):
        self.erase()
        for i in range(0,self.x):
            for j in range(0,self.y):
                if random.random() > 0.5:
                    self.set(i,j)

    def toggle(self,x,y):
        if self.is_legal(x,y):
            key = (x,y)
            if key in self.state:
                self.state.remove(key)
            else: 
                self.state.add(key)

    def erase(self):
        self.state.clear()

    def step(self):
        d = set()
        for i in range(self.x):
            xrange = range(max(0, i-1), min(self.x, i+2))
            for j in range(self.y):
                s = 0
                live = ((i,j) in self.state)
                #this loop confuses me. for the highest number in j to the lowest number in y to j+2, then loop through each x, then check the keys for each value
                #i get that it's going through the neighbors of each cell. it's just written in such a different way to me. the loop seems to be going through all the combinations of 0-2 of (currentx, currenty) (ie x,y+1; x+1, y+1; x, y+2; etc)
                for yp in range(max(0,j-1),min(self.y,j+2)): 
                    for xp in xrange:
                        if (xp,yp) in self.state:
                            s += 1 #has a neighbor

                s -= live 
                if (s == 3): # here is where it checks neighbor counts and maybe adds the cell, after it replaces the collection
                    d.add((i,j))
                elif s == 2 and live:
                    d.add((i,j))
                elif live:
                    pass

        self.state = d

    def draw(self,x,y):
        turtle.penup()
        key = (x,y)
        if key in self.state:
            turtle.setpos(x*CELL_SIZE, y*CELL_SIZE)
            turtle.color('black')
            turtle.pendown()
            turtle.setheading(0)
            turtle.begin_fill()
            for i in range(4): #took me a few seconds to realize that this is drawing each edge and then rotating 90 degrees to draw the next edge until it's a square, seems very inefficient
                turtle.forward(CELL_SIZE-1)
                turtle.left(90)
            turtle.end_fill()

    def display(self):
        turtle.clear()
        for i in range(self.x):
            for j in range(self.y):
                self.draw(i,j)
        turtle.update()

def display_help_window():
    from turtle import TK
    root = TK.Tk()
    frame = TK.Frame()
    canvas = TK.Canvas(root, width=400, height=200, bg="white")
    canvas.pack()
    help_screen = turtle.TurtleScreen(canvas)
    help_t = turtle.RawTurtle(help_screen)
    help_t.penup()
    help_t.hideturtle()
    help_t.speed('fastest')

    width, height = help_screen.screensize()
    line_height = 20
    y = height // 2 - 30 # / == double division, // == division, truncate to int
    for s in ("Click on cells to make them alive or dead.",
              "Keyboard commands:",
              " E)rase the board",
              " R)andom fill",
              " S)tep once or",
              " C)ontinuously -- use 'S' to resume stepping",
              "+ -> increase pixel size and rerandomize",
              "- -> decrease pixel size and rerandomize",
              " Q)uit"):
        help_t.setpos(-(width/2),y)
        help_t.write(s,font=('sans-serif',14,'normal'))
        y -= line_height

def main():
    display_help_window()

    scr = turtle.Screen()
    turtle.colormode('standard')
    xsize, ysize = scr.screensize()
    turtle.setworldcoordinates(0,0,xsize,ysize)

    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.tracer(0,0)
    turtle.penup()

    board = LifeBoard(xsize // CELL_SIZE, 1+ ysize // CELL_SIZE)

    def toggle(x,y):
        cellx = x // CELL_SIZE
        celly = y // CELL_SIZE
        if board.is_legal(cellx, celly):
            board.toggle(cellx, celly)
            board.display()

    turtle.onscreenclick(turtle.listen)
    turtle.onscreenclick(toggle)

    board.makeRandom()
    board.display()

    def erase():
        board.erase()
        board.display()
    turtle.onkey(erase,'e')

    def makeRandom():
        board.makeRandom()
        board.display()
    turtle.onkey(makeRandom, 'r')

    turtle.onkey(sys.exit, 'q')

    continuous = False
    def step_once():
        nonlocal continuous #continuous variable but a new one not the same scope
        continuous = False
        perform_step()

    def step_continuous():
        nonlocal continuous
        continuous = True
        perform_step()

    def perform_step():
        board.step()
        board.display()
        if continuous:
            turtle.ontimer(perform_step, 1)

    turtle.onkey(step_once, 's')
    turtle.onkey(step_continuous, 'c')

    def up_size():
        global CELL_SIZE
        CELL_SIZE += 1
        makeRandom()

    def down_size():
        global CELL_SIZE
        CELL_SIZE -= 1
        makeRandom()

    turtle.onkey(up_size, '+')
    turtle.onkey(down_size, '-')

    turtle.listen()
    turtle.mainloop()

if __name__ == '__main__':
    main()


