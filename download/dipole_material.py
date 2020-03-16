# 2020/2/10 Morris
# import package
from vpython import *

# use a custome function that can create a range which interval can be float number
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


# parameter setting
k = 9E9                     # Coulomb constant
ec = 1.6E-19                # charge of a electron
radius = 1.2E-14            # radius of charge
arrow_length = 5E-14        # length of arrow
shaftwidth = 5E-15          # shaft width of arrow
dt = 0.01                   # update time interval
m = 1.6E-31                 # mass of charge

# create scene and object
scene = canvas(width=1000, height=600, range=2E-12, userspin=False)

# adjust scene light direction to avoid interference of the scene
scene.lights[0].direction = vec(0, 0.88, 0.88)
scene.lights[1].direction = vec(0, -0.88, -0.88)

# create a dipole at +-10*radius away from the origin and using class 'Charge'
dipoles = []
for x in frange(-200*radius, 200*radius, 40*radius):
    for y in frange(-170*radius, 170*radius, 40*radius):
        axis_x = random() if random() > 0.5 else -random()
        axis_y = random() if random() > 0.5 else -random()
        dis = (axis_x**2 + axis_y**2)**0.5
        axis_x, axis_y = axis_x/dis*20*radius, axis_y/dis*20*radius
        axis = vec(axis_x, axis_y, 0)
        dipole_1 = sphere(pos=vec(x, y, 0), radius=5*radius, C=-ec,
                          make_trail=True, color=vec(1, 0, 0))
        dipole_2 = sphere(pos=dipole_1.pos+axis, radius=5*radius, C=ec,
                          make_trail=True, color=vec(0, 0, 1))
        arrow(pos=dipole_2.pos, axis=(dipole_1.pos-dipole_2.pos)*0.8, color=vec(0, 1, 0))
        dipoles.append([dipole_1, dipole_2])


p0 = vec(-250*radius, 0, 0)
# free charge initial velocity
vx = 100*random()*radius
v0 = vec(vx, 0, 0)
# random charge sign
sign = 1 if random() > 0.5 else -1
color = vec(1, 0, 0) if sign < 0 else vec(0, 0, 1)
free_charge = sphere(pos=p0, radius=5*radius, C=1E-42*ec*sign,
                     make_trail=True, color=color, v=v0)



while True:
    rate(1/dt)
    if mag(free_charge.pos) > 3E-12:
        # clear object in scene
        for obj in scene.objects:
            obj.visible = False
            del obj

        # create a dipole at +-10*radius away from the origin and using class 'Charge'
        dipoles = []
        for x in frange(-200*radius, 200*radius, 40*radius):
            for y in frange(-170*radius, 170*radius, 40*radius):
                axis_x = random() if random() > 0.5 else -random()
                axis_y = random() if random() > 0.5 else -random()
                dis = (axis_x**2 + axis_y**2)**0.5
                axis_x, axis_y = axis_x/dis*20*radius, axis_y/dis*20*radius
                axis = vec(axis_x, axis_y, 0)
                dipole_1 = sphere(pos=vec(x, y, 0), radius=5*radius, C=-ec,
                                  make_trail=True, color=vec(1, 0, 0))
                dipole_2 = sphere(pos=dipole_1.pos+axis, radius=5*radius, C=ec,
                                  make_trail=True, color=vec(0, 0, 1))
                arrow(pos=dipole_2.pos, axis=(dipole_1.pos-dipole_2.pos)*0.8, color=vec(0, 1, 0))
                dipoles.append([dipole_1, dipole_2])


        free_charge.clear_trail()
        # create a free charge that have a random velocity and position
        # free charge initial position
        p0 = vec(-250*radius, 0, 0)
        # free charge initial velocity
        vx = 100*random()*radius
        v0 = vec(vx, 0, 0)
        # random charge sign
        sign = 1 if random() > 0.5 else -1
        # determing the color of free charge
        color = vec(1, 0, 0) if sign < 0 else vec(0, 0, 1)
        free_charge = sphere(pos=p0, radius=5*radius, C=1E-42*ec*sign,
                             make_trail=True, color=color, v=v0)

    # update the position of the charge
    pos = free_charge.pos
    try:
        E = vec(0, 0, 0)
        # use superposition quality of electric field to calcuate the field
        for dipole in dipoles:
            for charge in dipole:
                E += k*charge.C*(pos-charge.pos)/mag(pos-charge.pos)**3
    except ZeroDivisionError:
        # cannot calculate the eletric field at the surface of the charge
        print('Electric field is infinity at the susrface of the charge')
    a = free_charge.C*E/m
    free_charge.v += a*dt
    free_charge.pos += free_charge.v*dt


