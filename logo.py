from turtle import left, forward, color, mainloop, pensize, colormode, penup, pendown, hideturtle, begin_fill, end_fill
colormode(255)
pensize(2)
from random import randint
from math import sin, radians

def nUholnik(n, a):
    begin_fill()
    for i in range(n):
        forward(a)
        left(360/n)
    end_fill()

def centered_nUholnik(n, a):
    x = 1/sin(radians(180/n))
    penup()
    left(90)
    forward(-x*a/2)
    left(-90)
    pendown()
    rotated_nUholnik(n, a)
    penup()
    left(90)
    forward(x*a/2)
    left(-90)
    pendown()

def rotated_nUholnik(n, a):
    left(180/n)
    nUholnik(n, a)
    left(-180/n)

def random_color():
    color(randint(0, 255),randint(0, 255),randint(0, 255))

for i in range(30, 2, -1):
    if i%2==1 :
        color('red3')
    else:
        color('black')
    centered_nUholnik(i, 1000/i)

hideturtle()
mainloop()