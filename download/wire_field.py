'''
    2020/2/19 --Morris --Magnetic Field of A Wire

    --> create scene, wire and arrow represent the direction of current
    --> calculate magnetic field using Biot-Savart law
    --> normalize magnetic field
    --> create arrow with different color represent magnitude(using cylindrcal
        distribution)
'''

# import package
from vpython import *

# paremeter setting
mu = 4*pi*1E-7              # permeability of free space
arrow_length = .5           # arrow length of field
dt = 0.01                   # animation frame interval
I = 10                      # current

def main():
    '''main function that execute at the end'''
    # let wire be global variable so that other function has access to it
    global wire

    # create scene
    scene = canvas(width=1000, height=600, userzoom=False, userspan=False,
                   range=5, align='left')
    # control scene camera location
    scene.camera.pos = vec(0, 6, 7)
    scene.camera.axis=vec(0, -2, -2)
    # create wire
    wire = cylinder(pos=vec(0, -250, 0), axis=vec(0, 500, 0), radius=.3,
                    opacity=.2, I=I)
    # create arrow represent current
    current = arrow(pos=vec(0, -6, 0), axis=vec(0, 1, 0),
                    color=color.green)
    # plot calculate value of magnetide field and theretical
    plot()
    # create magnetic field
    magnetic_field()
        # let the current flow
    while True:
        rate(1/dt)
        if current.pos.y <= 6:
            current.pos += vec(0, .05, 0)
        else:
            current.pos = vec(0, -6, 0)


def magnetic_field():
    '''
    create arrow represent the direction of magnetic field,
    and use color toe represent magnitude of field
    '''
    # use cylindrical coordinate to distribute arrow around wire
    # for z in frange(-3, 4, 3):
    z = 0
    for r in frange(1, 5, .5):
        for theta in frange(0, -2*pi, -pi/8):
            # transform coordinate
            pos = vec(r*cos(theta), z, r*sin(theta))
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
    B, n = vec(0, 0, 0), 3000
    start = wire.pos.y
    stop = wire.pos.y + wire.axis.y
    step = mag(wire.axis)/n
    # preform intergral
    for y in frange(start, stop, step):
        source = vec(0, y, 0)
        dl = vec(0, step, 0)
        try:
            B += mu*wire.I/4/pi*cross(dl, (pos-source))/(mag(pos-source))**3
        except ZeroDivisionError:
            print('zero division error')
    return B


def mag_field_color(B):
    a = 1/mag(biot_savart(vec(6, 0, 0)))
    # a = 1/2E-6
    return vec(0, 0, log(a*mag(B)))


def plot():
    # plot graph
    g1 = graph(title='magnetic field from the distance to wire(theory vs. calculated)',
               width=500, height=300, align='right', xtitle='distance',
               ytitle='magnetic field')
    # plot therotical value of magnetide field
    theory  = gcurve(graph=g1, color=color.red)
    # magnetide field that using intergral to aquired
    B = gcurve(graph=g1, color=color.blue)

    for x in frange(1, 5, 0.1):
        B.plot(pos=(x, mag(biot_savart(vec(x, 0, 0)))))
        theory.plot(pos=(x, mu*wire.I/2/pi/x))



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

