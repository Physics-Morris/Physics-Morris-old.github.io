# import package
from vpython import *
from frange import *

# paremeter setting
mu = 4*pi*1E-7              # permeability of free space
arrow_length = .3           # arrow length of field
dt = 0.01                   # animation frame interval
I = 50                      # current
G = 6.6E-11                 # gravitational constant
M = 6E24                    # mass of earth

# create scene
scene = canvas(width=1000, height=600, range=10, align='left')

# control scene camera location
#scene.camera.pos = vec(0, 2, 8)
#scene.camera.axis=vec(0, -.2, -1)

# create circular ring
loop = ring(pos=vec(0, 0, 0), radius=1.5, axis=vec(0, 1, 0),
            opacity=.5, I=I)

# create arrow represent current
current = arrow(pos=vec(1.5, 0, 0), axis=vec(0, 0, -.4),
                color=color.red)

# create list store info of particle
particles = []
for numbers in range(50):
    # create random particle with random speed, mass and charge shoot toward earth
    x = 10*random() if random() > 0.5 else -10*random()
    y = 10*random() if random() > 0.5 else -10*random()
    z = 10*random() if random() > 0.5 else -10*random()
    if x > 0: vx = -15*random()
    else: vx = 15*random()
    if y > 0: vy = -15*random()
    else: vy = 15*random()
    if z > 0: vz = -15*random()
    else: vz = 15*random()
    r, g, b = random(), random(), random()
    particles.append(sphere(pos=vec(x, y, z), v=vec(vx, vy, vz), color=vec(r, g, b),
                            M=random()/10, Q=random()*1E6, radius=.1, make_trail=True, retain=50))

# create closed field line near lopp from inside the loop
for R in frange(0.6, 0.4, -0.2):
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


t = 0
while True:
    rate(1/dt)

    # let the current flow
    current.pos = vec(1.5*cos(t), 0, 1.5*sin(t))
    current.axis = vec(-.4*sin(t), 0, .4*cos(t))

    for particle in particles:
        if mag(particle.pos) < 1.5: particle.visible = False
        # prefrom intergral using biot-savart law which divided wire into n segment
        B, n = vec(0, 0, 0), 500
        r = loop.radius

        # preform intergral to calculate B field
        for theta in frange(0, 2*pi, 2*pi/n):
            source = vec(r*cos(theta), 0, r*sin(theta))
            dl = (2*pi*r/n)*vec(-r*sin(theta), 0, r*cos(theta))
            try:
                B += mu*loop.I/4/pi*cross(dl, (particle.pos-source))/(mag(particle.pos-source))**3
            except ZeroDivisionError:
                print('zero division error')

        # gravity
        # Fg = -G*M*particle.M*particle.pos/mag(particle.pos)**3
        Fg = vec(0, 0, 0)

        a = (particle.Q*cross(particle.v, B) + Fg)/particle.M
        particle.v += a*dt
        particle.pos += particle.v*dt
    t += dt



