import tkinter as tk
import math
import binascii

HEIGHT = 750 #px
WIDTH = 750 #px
RSTEP = 20 #px

STARTTXT = "Never gonna give you up; Never gonna let you down;"

arcs = 6

def vline(c,a,r0,r1,med):
    if not(med):
        ar = math.radians(a)
        x0 = WIDTH / 2 + r0 * math.cos(ar)
        x1 = WIDTH / 2 + r1 * math.cos(ar)
        y0 = HEIGHT / 2 + r0 * math.sin(ar)
        y1 = HEIGHT / 2 + r1 * math.sin(ar)
        c.create_line(x0, y0, x1, y1)
    else:
        ar0 = math.radians(a-ASTEP)
        ar1 = math.radians(a+ASTEP)
        x0 = WIDTH / 2 + r0 * math.cos(ar0)
        x1 = WIDTH / 2 + r1 * math.cos(ar0)
        y0 = HEIGHT / 2 + r0 * math.sin(ar0)
        y1 = HEIGHT / 2 + r1 * math.sin(ar0)
        x2 = WIDTH / 2 + r0 * math.cos(ar1)
        x3 = WIDTH / 2 + r1 * math.cos(ar1)
        y2 = HEIGHT / 2 + r0 * math.sin(ar1)
        y3 = HEIGHT / 2 + r1 * math.sin(ar1)
        c.create_line((x0 + x2)/2, (y0+y2)/2, (x1+x3)/2, (y1+y3)/2)

def hline(c,a0,a1,r,med):
    if not(med):
        ar0 = math.radians(a0)
        ar1 = math.radians(a1+ASTEP)
        x0 = WIDTH / 2 + r * math.cos(ar0)
        x1 = WIDTH / 2 + r * math.cos(ar1)
        y0 = HEIGHT / 2 + r * math.sin(ar0)
        y1 = HEIGHT / 2 + r * math.sin(ar1)
        c.create_line(x0, y0, (x0+x1)/2, (y0+y1)/2)
    else:
        ar0 = math.radians(a0-ASTEP)
        ar1 = math.radians(a1)
        x0 = WIDTH / 2 + r * math.cos(ar0)
        x1 = WIDTH / 2 + r * math.cos(ar1)
        y0 = HEIGHT / 2 + r * math.sin(ar0)
        y1 = HEIGHT / 2 + r * math.sin(ar1)
        c.create_line((x0+x1)/2,(y0+y1)/2, x1, y1)

def text2bin(txt):
    b = ' '.join(format(ord(x), 'b') for x in txt)
    return b.replace(' ','')

def addArc(*args):
    global arcs
    arcs += 1
    update()

def lessArc(*args):
    global arcs
    arcs -= 1
    if arcs < 3:
        arcs = 3
    else:
        update()

def update(*args):
    global c, ASTEP, ASTART

    ASTEP = 180/arcs #angle in degrees
    ASTART = 0 #int * ASTEP

    c.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white")
    
    val = text2bin(txt.get())

    a = ASTART
    d = 40
    outer = False

    while a*ASTEP < 360:
        hline(c,a*ASTEP,(a+1)*ASTEP,d, a%2 == 0)
        hline(c,a*ASTEP,(a+1)*ASTEP,d-1, a%2 == 0)
        hline(c,a*ASTEP,(a+1)*ASTEP,d-2, a%2 == 0)
        a += 1

    a = ASTART

    for ch in val:
        if (ch == '1') ^ a%2 == 0:
            if outer:
                hline(c,a*ASTEP,(a+1)*ASTEP,d+RSTEP, a%2 == 0)
            else:
                vline(c,a*ASTEP,d,d+RSTEP,a%2 == 0)
        a += 1
        if a*ASTEP > 360:
            a -= int(360/ASTEP)
            outer = not(outer)
            if not(outer):
                d += RSTEP

    a = ASTART

    if outer:
        d += RSTEP

    while a*ASTEP < 360:
        hline(c,a*ASTEP,(a+1)*ASTEP,d+RSTEP, a%2 == 0)
        hline(c,a*ASTEP,(a+1)*ASTEP,d+RSTEP+1, a%2 == 0)
        hline(c,a*ASTEP,(a+1)*ASTEP,d+RSTEP+2, a%2 == 0)
        a += 1

top = tk.Tk()

txt = tk.StringVar()
txt.set(STARTTXT)
txt.trace('w',update)

e = tk.Entry(top,width=100,textvariable=txt)
e.grid(row=0,column=0)

bl = tk.Button(top, text="-", command=lessArc)
bl.grid(row=0,column=1)

bp = tk.Button(top, text="+", command=addArc)
bp.grid(row=0,column=2)

c = tk.Canvas(top, height=HEIGHT, width=WIDTH)
c.grid(row=1,column=0,columnspan=3)

update()

top.mainloop()
