# import package
from vpython import *
from frange import *

# paremeter setting
mu = 4*pi*1E-7              # permeability of free space
arrow_length = .3           # arrow length of field
dt = 0.01                   # animation frame interval
I = 10                      # current

# create scene
scene = canvas(width=1000, height=600, range=3, align='left')

# create circular ring
for y in frange(-.6, .6, .3):
    r = 1.5 - abs(y)
    ring(pos=vec(0, y, 0), radius=r, axis=vec(0, 1, 0),
                opacity=.5, I=I)

# create closed field line near lopp from inside the loop
for R in frange(.8, .4, -0.2):
    for phi in frange(0, -2*pi, -pi/4):
        # transform coordinate
        pos = vec(R*cos(phi), -0.01, R*sin(phi))
        # use while loop to create closed loop of magnetic field
        while True:
            temp = pos
            for times in range(10):
                # prefrom intergral using biot-savart law which divided wire into n segment
                B, n = vec(0, 0, 0), 500
                # do the intergral for different radius
                for y in frange(-.6, .6, .3):
                    r = 1.5 - abs(y)
                    # preform intergral
                    for theta in frange(0, 2*pi, 2*pi/n):
                        source = vec(r*cos(theta), y, r*sin(theta))
                        dl = (2*pi*r/n)*vec(-r*sin(theta), 0, r*cos(theta))
                        try:
                            B += mu*I/4/pi*cross(dl, (pos-source))/(mag(pos-source))**3
                        except ZeroDivisionError:
                            print('zero division error')

                # using 1/100 times of arrow length as the increment
                pos += hat(B)*arrow_length/10

            # create smae length of arrow
            arrow(pos=pos, axis=hat(B), length=arrow_length,
                  color=vec(log(1E7*mag(B)), 0, 1))
            # a do-while loop that stop magnetic field loop over one lap
            if temp.y*pos.y <= 0 and temp.y > 0:
                break

