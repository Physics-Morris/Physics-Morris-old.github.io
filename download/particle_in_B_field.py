'''
    2020/2/19 --Morris --Magnetic Field of A Wire

    --> create scene, circular ring and arrow represent the direction of current
    --> calculate magnetic field using Biot-Savart law
    --> normalize magnetic field
    --> create arrow with different color represent magnitude(using cylindrcal
        distribution)
    --> create a particle with positive or negative charge, and update its position
        in magnetic field
'''

# import package
from vpython import *

# paremeter setting
mu = 4*pi*1E-7              # permeability of free space
arrow_length = .1           # arrow length of field
dt = 0.01                   # animation frame interval
I = 10                      # current
C = 1E6                     # particle charge
v0 = vec(0, -1.5, 0)        # particle initial velocity
pos = vec(0, 1, 1)          # particle initial position
m = 1                       # particle mass

def main():
    '''main function that execute at the end'''
    # let loop be global variable
    global loop
    # create scene
    scene = canvas(width=1000, height=600, userzoom=False, userspan=False,
                   range=3, align='left')
    # control scene camera location
    scene.camera.pos = vec(0, 1, 3)
    scene.camera.axis=vec(0, -.5, -1)
    # create circular ring
    loop = ring(pos=vec(0, 0, 0), radius=1.5, axis=vec(0, 1, 0),
                opacity=.5, I=I, thickness=.05)
    # create arrow represent current
    current = arrow(pos=vec(1.5, 0, 0), axis=vec(0, 0, .2),
                    color=color.red)
    # create particle
    particle = sphere(pos=pos, radius=.05, v=v0, C=C, color=vec(0, 1, 0),
                      make_trail=True)
    # create a arrow that represent force excert on particle
    force = arrow(pos=particle.pos, color=vec(1, 0, 0), shaftwidth=.03,
                  axis=cross(particle.v, biot_savart(particle.pos))/10)
    # create a arrow that represent velocity of particle
    velocity = arrow(pos=particle.pos, color=vec(0, 0, 1), shaftwidth=.03,
                     axis=particle.v/3)
    # plot calculate value of magnetide field and theretical
    plot()
    # create magnetic field
    magnetic_field()
    # let the current flow
    t = 0
    while True:
        rate(1/dt)
        update(particle, force, velocity)
        current.pos = vec(1.5*cos(t), 0, 1.5*sin(t))
        current.axis = vec(-.2*sin(t), 0, .2*cos(t))
        if mag(particle.pos) > 3 or t > 5:
            t = 0
            particle.pos = frandom()
            particle.v = 1.5*frandom()
            particle.clear_trail()
        t += dt


def magnetic_field():
    '''
    create arrow represent the direction of magnetic field,
    and use color toe represent magnitude of field
    '''
    # use cylindrical coordinate to distribute arrow around wire
    for y in frange(-1, .5, .5):
        for r in frange(0, 2, .2):
            for theta in frange(0, -2*pi, -pi/16):
                if abs(r - loop.radius) > .1:
                    # transform coordinate
                    pos = vec(r*cos(theta), y, r*sin(theta))
                    B = biot_savart(pos)
                    # create smae length of arrow
                    arrow(pos=pos, axis=hat(B), length=arrow_length,
                          color=mag_field_color(B))

def biot_savart(pos):
    '''
    calculate magnetic field using 'wire' as the source,
    and reutrn the magnetude and direction of the field
    '''
    # do the intergral that divided wire into n segment
    B, n = vec(0, 0, 0), 1000
    r = loop.radius
    # preform intergral
    for theta in frange(0, 2*pi, 2*pi/n):
        source = vec(r*cos(theta), 0, r*sin(theta))
        dl = (2*pi*r/n)*vec(-r*sin(theta), 0, r*cos(theta))
        try:
            B += mu*loop.I/4/pi*cross(dl, (pos-source))/(mag(pos-source))**3
        except ZeroDivisionError:
            print('zero division error')
    return B


def mag_field_color(B):
    # a = 1/mag(biot_savart(vec(2, 0, 0)))
    a = 1/2E-6
    return vec(1-log(a*mag(B)), 0, 1)


def plot():
    # plot graph
    g1 = graph(title='magnetic field from the distance to center',
               width=500, height=300, align='right', xtitle='distance',
               ytitle='magnetic field')
    # magnetide field that using intergral to aquired
    B = gdots(graph=g1, color=color.blue)

    for r in frange(0, 5, .01):
        if abs(r - loop.radius) > 0.1:
            B.plot(pos=(r, mag(biot_savart(vec(r, 0, 0)))))


def update(obj, force, velocity):
    '''
    update particle position and velocity due to magnetic field
    '''
    # lorentz force
    a = obj.C*cross(obj.v, biot_savart(obj.pos))/m
    obj.v += a*dt
    obj.pos += obj.v*dt
    # update arrow position and direction
    force.pos = obj.pos
    force.axis = m*a/10
    force.shaftwidth = .05
    velocity.pos = obj.pos
    velocity.axis = obj.v/3
    velocity.shaftwidth = .05


def frandom():
    '''
    return a random vector that each element is between +- 1
    '''
    x = random() if random() > 0.5 else -random()
    y = random() if random() > 0.5 else -random()
    z = random() if random() > 0.5 else -random()
    return vec(x, y, z)

def frange(start, stop, step=1):
    '''
    create a range that each stap can be a float number
    that can be in this program
    '''
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    elif n == 1:
        return([start])
    else:
        return([])


main()

