# 2020/2/10 Morris
# import package
from vpython import *

# parameter setting
k = 9E9                     # Coulomb constant
ec = 1.6E-19                # charge of a electron
radius = 1.2E-14            # radius of charge
arrow_length = 1E-14        # length of arrow
shaftwidth = 1E-15          # shaft width of arrow
dt = 0.01                   # update time interval
m = 1.6E-31                 # mass of charge
v0 = vec(radius, 0, 0)      # free charge initial velocity
p0 = vec(0, 10*radius, 0)   # free charge initial position

def main():
    '''main function'''
    # create scene and object
    scene = canvas(width=1000, height=600, range=2E-13, userspin=False,
                   userpan=False, userzoom = False)

    # adjust scene light direction to avoid interference
    scene.lights[0].direction = vec(0, 0.88, 0.88)
    scene.lights[1].direction = vec(0, -0.88, -0.88)

    # create a dipole at +-10*radius away from the origin and using class 'Charge'
    dipole = [charge(vec(-10*radius, 0, 0), -ec),
              charge(vec(10*radius, 0, 0), ec)]

    # show electric potential of dipole in the given region
    # show_potential(dipole, scene.range*1.8)

    # show field the dipole of dipole in the given region
    show_field(dipole, scene.range*1.8)

    # create a free charge that have a random velocity and position
    free_charge = charge(p0, 1E-42*ec)
    free_charge.v = v0
    while True:
        rate(1/dt)

        # update the position of the charge
        update(dipole, free_charge)

def charge(pos, coulomb):
    '''
        --> create one or multiple charge using vpython object 'sphere'
        --> red and blue represent negative and positive charge respectively
    '''
    return sphere(pos=pos, radius=radius, C=coulomb,
                  color = color.blue if coulomb > 0 else color.red,
                  make_trail=True)

def show_field(charges, range):
    '''
    create field in the given range and set the default interval that create a
    arrow be the radius of the charge.
   '''
    # create arrow representing eletric field in the given region using meshgrid
    for x, y in meshgrid(range, range):
        pos, E = vec(x, y, 0), vec(0, 0, 0)
        # using try and except syntax to prevent the error by divided 0
        try:
            # use superposition quality of electric field to calcuate the field
            for charge in charges:
                E += k*charge.C*(pos-charge.pos)/mag(pos-charge.pos)**3

            # normalize the value of eletric field to (0, 1) for mapping color
            color = vec(1, field_norm(mag(E)), 0)

            # create field by creating arrow
            arrow(pos=pos, axis=hat(E)*arrow_length, color=color,
                  shaftwidth=shaftwidth)
        except ZeroDivisionError:
            # cannot calculate the eletric field at the surface of the charge
            print('Electric field is infinity at the susrface of the charge')


def show_potential(charges, range):
    '''
    for a given position calculate electric potential and draw a
    meshgrid of quad representing potential magnitude
    '''
    # create quad object that representing eletric potnetial in the given region
    for x, y in meshgrid(range, range, 0.5*radius):
        pos, V = vec(x, y, 0), 0
        # using try and except syntax to prevent the error by divided 0
        try:
            # calculate the eletric potential using fromula v = k*q/r
            for charge in charges:
                V += k*charge.C/mag(pos-charge.pos)

            # given red color if potnetial is smaller than 0, and vice versa
            if V > 0: color = vec(0, 0, potential_norm(V))
            else: color = vec(potential_norm(V), 0, 0)

            # create field by creating quad of meshgrid and the color represnt potential
            create_quad(pos, color)

        except ZeroDivisionError:
            # cannot calculate the eletric field at the surface of the charge
            print('Electric field is infinity at the susrface of the charge')


def field_norm(value):
    '''
    normalize the value of eletric field between vmin and vmax to 0 and 1
    by taking log, so the normalize value can be used for mapping the colors
    '''
    a = 1E-17
    return 1 - log(a*value)


def potential_norm(value):
    '''
        normalize the value of eletric potential between vmin and vmax to 0 and 1
        by taking log, so the normalize value can be used for mapping the colors
    '''
    b = 3E-4
    # to prevent the area that potential equals to 0 that will arise domain error
    try:
        return log(b*abs(value))
    except ValueError:
        return 0

def create_quad(pos, color):
    '''
        --> create a meshgrid at the given position and the color at that position
        --> using quad object and the side length be the 0.1 times raidus of the charge
    '''
    quad(vs=[vertex(pos=(pos-vec(0.25*radius, 0.25*radius, 0)), color=color, opacity=0.6),
             vertex(pos=(pos-vec(0.25*radius, -0.25*radius, 0)), color=color, opacity=0.6),
             vertex(pos=(pos-vec(-0.25*radius, -0.25*radius, 0)), color=color, opacity=0.6),
             vertex(pos=(pos-vec(-0.25*radius, 0.25*radius, 0)), color=color, opacity=0.6)])


def meshgrid(xrange, yrange, step=radius):
    '''
    create a meshgrid a given xrange and yrange
    setting default step be the radius of the charge
    '''
    grid = []
    for x in frange(-xrange, xrange, step):
        for y in frange(-yrange, yrange, step):
            grid.append([x, y])
    return grid

def frange(start, stop, step=1):
    '''
    create a range that each stap can be a float number that can be in this program
    '''
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    elif n == 1:
        return([start])
    else:
        return([])

def update(source, obj):
    '''given a charge and position and update position due to influence of the source'''
    # first calculate electric field at a given position
    E = vec(0, 0, 0)
    try:
        # use superposition quality of electric field to calcuate the field
        for charge in source:
            E += k*charge.C*(obj.pos-charge.pos)/mag(obj.pos-charge.pos)**3
        a = obj.C*E/m
        obj.v += a*dt
        obj.pos += obj.v*dt
    except ZeroDivisionError:
        # stop moving when free charge hit dipole
        obj.v = 0

# execute main function
main()
