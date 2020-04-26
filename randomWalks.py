from objects import *

## motion
# RANDOM will render the actions based on raytaces (brainless)
# MOUSE  will render based on mouse (selects bot when hovered over the bot)
# STILL is used when agent controls the next move e.g (rotate, move forward)
window = (1400 ,800) # window dimensions

env = Environment(window, record=('RAYTRACE_8.mp4' ,'MP4V') ,motion = 'RANDOM')
env.addPlayer(Seeker((300, 50) ,'Seeker' ,viewAngle=20 ,radius = 5, color=(0 ,255 ,0)))
env.addPlayer(Hider((950, 50) ,'Hider' ,viewAngle=20 ,radius = 5, color=(255 ,0 ,0)))


############# square #############
# env.addObject(Object=Object([(700, 300), (700, 600)],1))
# env.addObject(Object=Object([(500, 300), (800, 300)],1))
# env.addObject(Object=Object([(800, 300), (800, 500)],1))
# env.addObject(Object=Object([(500, 500), (800, 500)],1))



################ Hide and seek playground ############
env.addObject(Object=Object([(200, 150), (400, 150)] ,1))
env.addObject(Object=Object([(400, 150), (400, 550)] ,1))
env.addObject(Object=Object([(400, 550), (200, 550)] ,1))
env.addObject(Object=Object([(600, 0), (600, 250)] ,1))
env.addObject(Object=Object([(600, 450), (600, 700)] ,1))
env.addObject(Object=Object([(1000, 150), (1300, 150)] ,1))
env.addObject(Object=Object([(1000, 550), (1300, 550)] ,1))
env.addObject(Object=Object([(800, 150), (800, 550)] ,1))
env.addObject(Object=Object([(800, 350), (1100, 350)] ,1))
#

################## maze ##################
# even = True
# y =100
# for x in range(y,1400,y):
#     if even:
#         env.addObject(Object=Object([(x, 0), (x, 800-y)], 1))
#         even = False
#     else:
#         env.addObject(Object=Object([(x, y), (x, 800)], 1))
#         even = True
####################End of maze section #########################

#
####################### Brainless interaction ############################
# renders each state based on returned ray traced arrays
env.runRender()
###############################################################
