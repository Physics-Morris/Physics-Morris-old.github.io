from vpython import *

l, theta, m, g, out = 20, pi/4, 1.2, 9.8, 0.05

scene = canvas(width=1000, height=600, align='left')
scene.range = 35
celling = box(pos=vec(0, 0, 0), size=vec(30, 1, 30), color=color.blue)
cyn = cylinder(pos=vec(l*sin(theta), -l*cos(theta), 0), axis=vec(0, -5, 0), radius=3, color=color.red,
               theta=pi/4, omg=0)
line = curve(cyn.pos, celling.pos)
f1 = graph(title='<b>Angle</b>', xtitle='<b>time</b>', ytitle='<b>Angule</b>', align='right',
           width=300, height=300)
f2 = graph(title='<b>Mass</b>', xtitle='<b>time</b>', ytitle='<b>Mass(kg)</b>', align='right',
           width=300, height=300)
w = gdots(graph=f1)
w2 = gdots(graph=f2)

sands = []

def sand_flow():
    sand = sphere(pos=cyn.pos+vec(0, -5, 0), radius=0.2,
                  color=vec(random(), random(), random()), v=vec(0, -1, 0))
    sands.append(sand)

dt = 0.1
t = 0
while True:
    rate(1/dt)
    if m >= 0.2:
        sand_flow()
        m = m - out*dt
    I = m*l**2
    alpha = -m*g*l*sin(cyn.theta)/I
    cyn.omg += alpha*dt
    cyn.theta += cyn.omg*dt
    cyn.pos = vec(l*sin(cyn.theta), -l*cos(cyn.theta), 0)
    line.visible = False
    line = curve(cyn.pos, celling.pos)
    for sand in sands:
        sand.pos += sand.v*dt
    w.plot(pos=(t, cyn.theta))
    w2.plot(pos=(t, m))
    t += dt

