'''
    2020/2/19 --Morris --Magnetic Field of A Wire

    --> create scene, circular ring and arrow represent the direction of current
    --> calculate magnetic field using Biot-Savart law
    --> normalize magnetic field
    --> create arrow with different color represent magnitude(using cylindrcal
        distribution)
'''

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

# control scene camera location
scene.camera.pos = vec(0, 1, 7)
scene.camera.axis=vec(0, -.2, -1)

# create circular ring
loop = ring(pos=vec(0, 0, 0), radius=1.5, axis=vec(0, 1, 0),
            opacity=.5, I=I)

# create arrow represent current
current = arrow(pos=vec(1.5, 0, 0), axis=vec(0, 0, -.4),
                color=color.red)

# create closed field line near lopp from inside the loop
for R in frange(1, 0.6, -0.2):
    for phi in frange(0, -2*pi, -pi/4):
        # transform coordinate
        pos = vec(R*cos(phi), -0.01, R*sin(phi))
        # use while loop to create closed loop of magnetic field
        while True:
            temp = pos
            for times in range(10):
                # prefrom intergral using biot-savart law which divided wire into n segment
                B, n = vec(0, 0, 0), 500
                r = loop.radius

                # preform intergral
                for theta in frange(0, 2*pi, 2*pi/n):
                    source = vec(r*cos(theta), 0, r*sin(theta))
                    dl = (2*pi*r/n)*vec(-r*sin(theta), 0, r*cos(theta))
                    try:
                        B += mu*loop.I/4/pi*cross(dl, (pos-source))/(mag(pos-source))**3
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

# let the current flow
t = 0
while True:
    rate(1/dt)
    current.pos = vec(1.5*cos(t), 0, 1.5*sin(t))
    current.axis = vec(-.4*sin(t), 0, .4*cos(t))
    t += dt


