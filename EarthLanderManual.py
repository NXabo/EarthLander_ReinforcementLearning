# -*- coding: utf-8 -*-
"""
@author: LJ
"""
from tkinter import *
import math
import numpy as np

#Variables du jeu
altitude = 8100
speed = 268
throttle = 0
fuel = 1000
gameState = 0
actualPixelPos = 70
userInput = 0
reset = 0
alt_poss = [[0,800],[800,2000],[2000,3000],[3000,4000],[4000,5000],[5000,999999]]
speed_poss = [[-999999,0],[0,40],[40,70],[70,200],[200,999999]]

#environement (s'éxécute 10X par seconde)
def environment():
    global altitude
    global speed
    global throttle
    global fuel
    global gameState
    global state
    global alt_poss
    global speed_poss

    ############ EL parameters
    state = 0
    trans_matrix = np.loadtxt("trans_matrix.txt")
    ############

    ############ Gestion de l'état
    for i in range(len(alt_poss)):
        if alt_poss[i][0] <= altitude and alt_poss[i][1] > altitude:
            state = i
            break
    for i in range(len(speed_poss)):
        if speed_poss[i][0] <= speed and speed_poss[i][1] > speed:
            state = state * len(speed_poss) + i
            break
    ############

    throttle = agent_QL(trans_matrix,state)
    if fuel <= 0:
        fuel = 0
        throttle = 0
        
    a = 9.8-throttle
    altitude -= speed*0.1 - a*0.01/2
    speed += a*0.1
    fuel -= throttle*0.1
    
    if altitude <= 0:
        if speed <= 40:
            altitude = 0
            throttle = 0
            speed = 0
            gameState = 2
        else:
            altitude = 0
            throttle = 0
            speed = 0
            gameState = 1
            
#agent qui éxecute l'entrée utilisateur
def agentManual():
    return userInput


def agent_QL(trans_matrix,state):
    return np.argmax(trans_matrix,axis=1)[state]

# gestion de l'interface graphique (il n'est pas indispensable de comprendre le code ci-dessous pour réussir le TP)
def onTimer():
    global altitude
    global speed
    global throttle
    global fuel
    global gameState
    global reset
    global userInput
    global state
    if reset == 1:
        altitude = 10000
        speed = 0
        throttle = 0
        fuel = 1000
        gameState = 0
        userInput = 0
        reset = 0
        state = 0
    if gameState == 0:
        environment()
        moveRocket()
        updateData()
    root.after(100,onTimer)
    
def moveRocket():
    global actualPixelPos
    newPos = round(400 - altitude * 330  /10000)
    offset = newPos - actualPixelPos
    c.move(p0,0,offset)
    if throttle == 0:
        c.itemconfig(p0,fill="#000",outline="#000")
    else:
        c.itemconfig(p0,fill="#ff0",outline="#ff0")
    c.move(p1,0,offset)
    c.move(p2,0,offset)
    c.move(p3,0,offset)
    c.move(o1,0,offset)
    actualPixelPos = newPos
    if gameState == 1:
        c.itemconfig(pexplo,state="normal") 
    elif gameState == 2:
        c.itemconfig(l1,fill="#fff")
        c.itemconfig(pfla,fill="#fff",outline="#fff")
    else:
        c.itemconfig(pexplo,state="hidden")
        c.itemconfig(l1,fill="#000")
        c.itemconfig(pfla,fill="#000",outline="#000")
        
def updateData():
    c.itemconfig(t1, text="Altitude: {0:.2f}".format(altitude))
    c.itemconfig(t2, text="Speed: {0:.2f}".format(speed))
    c.itemconfig(t3, text="Fuel: {0:.2f}".format(fuel))
    c.itemconfig(t4, text="Throttle: {0:d}".format(throttle))
    c.itemconfig(t5, text="State: {0:d}".format(state))
    
def onKeyPressed(e):
    global userInput
    global reset
    c = e.char
    if c == 'a' or c == '0':
        userInput = 0
    elif c == 'z':
        userInput = 1
    elif c == 'e' or c == '1':
        userInput = 2
    elif c == 'r':
        userInput = 3
    elif c == 't' or c == '2':
        userInput = 4
    elif c == 'y':
        userInput = 5
    elif c == 'u' or c == '3':
        userInput = 6
    elif c == 'i':
        userInput = 7
    elif c == 'o' or c == '4':
        userInput = 8
    elif c == 'p':
        userInput = 9
    elif c == 'q' or c == '5':
        userInput = 10
    elif c == 's':
        userInput = 11
    elif c == 'd' or c == '6':
        userInput = 12
    elif c == 'f':
        userInput = 13
    elif c == 'g' or c == '7':
        userInput = 14
    elif c == 'h':
        userInput = 15
    elif c == 'j' or c == '8':
        userInput = 16
    elif c == 'k':
        userInput = 17
    elif c == 'l' or c == '9':
        userInput = 18
    elif c == 'm':
        userInput = 19
    elif c == 'w':
        reset = 1
        
root = Tk()
root.title("Earth Lander")
root.geometry("640x480")

c = Canvas(bg ="#000")

p0 = c.create_polygon([158,50,152,70,160,80,168,70,162,50],fill="#ff0",outline ="#ff0",width=2.0)
p1 = c.create_polygon([150,50,150,70,140,70],fill="#f00",outline="#f00",width=2.0)
p2 = c.create_polygon([170,50,170,70,180,70],fill="#f00",outline="#f00",width=2.0)
p3 = c.create_polygon([160,10,175,30,170,50,150,50,145,30],fill="#fff",outline="#f00",width=2.0)
o1 = c.create_oval(150,25,170,35,fill="#0ff",outline="#f00",width=2.0)
                   
l1 = c.create_line(100,400,100,350,fill="#000",width=2.0)
pfla = c.create_polygon([100,375,75,362,100,350],fill="#000",outline="#000",width=2.0) 
                        
pexplo = c.create_polygon([110,320,140,350,140,300,160,355,190,320,180,360,220,375, 180,380,200,420,170,385,160,450,150,385,120,430,125,380,90,375,130,360],fill="#ff0",outline="#ff0",width=2.0)
c.itemconfig(pexplo,state="hidden")                          
                          
c.create_polygon([640,400,480,250,320,400],fill="#a55",outline="#a55",width=2.0)
c.create_line(0,400,640,400,fill="#0f0",width=3.0)
                   
t1 = c.create_text(320, 30, anchor=W, font="arial",text="Altitude: 10000",fill ="#fff")
t2 = c.create_text(320, 60, anchor=W, font="arial",text="Speed: 0",fill ="#fff")
t3 = c.create_text(320, 90, anchor=W, font="arial",text="Fuel: 1000",fill ="#fff")
t4 = c.create_text(320, 120, anchor=W, font="arial",text="Throttle: 0",fill ="#fff")
t5 = c.create_text(320, 150, anchor=W, font="arial",text="State: 0",fill ="#fff")

c.pack(fill=BOTH, expand=1)

root.bind_all("<Key>",onKeyPressed)
root.focus_force()
root.after(100,onTimer)
root.mainloop()