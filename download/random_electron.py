# 2020/2/16 front page animation
from vpython import *

# parameter
k = 9E9
ec = 1.6E-19
radius = 1.2E-14
dt = 0.001
m = 1.6E-31

def main():
    '''main function'''
    # create scene
    scene = canvas(width=1000, height=600, range=5E-13,
                   usepan=False, userzoom=False)

    proton = charge(vec(0, 0, 0), ec)
    proton.radius = 3*radius

    # create electron
    electrons = []
    for i in range(60):
        x = random() if random() > 0.5 else -random()
        y = random() if random() > 0.5 else -random()
        z = random() if random() > 0.5 else -random()
        dis = (x**2+y**2+z**2)**0.5
        x, y, z = x/dis, y/dis, z/dis
        dx, dy, dz = random()*100, random()*100, random()*100
        electron = charge(vec(x*radius*dx, y*radius*dy, z*radius*dz), -1E-41*ec)
        vx = random() if random() > 0.5 else -random()
        vy = random() if random() > 0.5 else -random()
        vz = random() if random() > 0.5 else -random()
        r, g, b = random(), random(), random()
        electron.v = 1E-13*vec(vx, vy, vz)
        electron.color = vec(r, g, b)
        electron.trail_color = vec(r, g, b)
        electrons.append(electron)
    while True:
        rate(1/dt)
        update(proton, electrons)

def charge(pos, coulomb):
    '''
    --> create one or multiple charge using vpython object 'sphere'
    --> red and blue represent negative and positive charge respectively
    '''
    return sphere(pos=pos, radius=radius, C=coulomb,
                  color = color.blue if coulomb > 0 else color.red,
                  make_trail=True, type=points, retain=100)

def update(source, electrons):
    '''
    given a charge and position and update position
    due to influence of the source
    '''
    for electron in electrons:
        # first calculate electric field at a given position
        E = vec(0, 0, 0)
        try:
            # use superposition quality of electric field to calcuate the field
            E = k*source.C*(electron.pos-source.pos)/mag(electron.pos-source.pos)**3
            a = electron.C*E/m
            electron.v += a*dt
            electron.pos += electron.v*dt
        except ZeroDivisionError:
            # stop moving when free charge hit dipole
            electron.v = 0

main()
