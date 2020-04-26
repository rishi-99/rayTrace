
from objects import *

window = (1400 ,800) # window dimensions

env = Environment(window, record=('RAYTRACE_8.mp4' ,'MP4V') ,motion = 'RANDOM')
env.addPlayer(Seeker((300, 50) ,'Seeker' ,viewAngle=20 ,radius = 5, color=(0 ,255 ,0)))
env.addPlayer(Hider((850, 50) ,'Hider' ,viewAngle=20 ,radius = 5, color=(255 ,0 ,0)))


wall = Object([(int(window[0] / 2), 0), (int(window[0] / 2), int(window[1] / 2))], 1)
env.addObject(Object=wall)
for x in range(1000):

    controls = {}
    controls['Seeker'] = {'forward': True, 'rotate': 60}
    controls['Hider'] = {'forward': True, 'rotate': 60}
    state = env.feed(controls)
    print(state)
    cv2.imshow("RayTracing", state[1])
    if cv2.waitKey(80) == ord('q'):
        break
