from  math import *
import numpy as np
import cv2
import random
import time


class Object:
    '''
    Object class creates walls by joing all possible point x and y.
    e.g

    Object([(x1,y1),(x2,y2),(x3,y3)], 1)
    this will create triangle with point x1,y1  , x2,y2  and  x3,y3

    and passing this object to environment using addObject method.
    env.addObject(Object=wall)
    '''

    def __init__(self, points, thickness, color = (255,255,255)):
        self.points = list(points)
        self.color = color
        self.thickness = thickness
        self.walls = []
        self.construct_walls()

    def construct_walls(self):
        temp_list = self.points.copy()
        for point  in self.points[:-1]:
            temp_list.pop(temp_list.index(point))
            for other_point in temp_list:
                self.walls.append([point,other_point])


class Hider:

    '''
    Hider is bot class that has characteristic of hider. Its speed is reduced to zero when caught by Seeker and rays are disabled.
    In brainless mode it take 90 degree of turn (left/right based on ray array data) when sees Seeker.
    takes arguments as follows:
    point       = start point
    name        = name of bot
    viewAngle   = vision angle
    speed       = rate of change of cordinates (x and y will change based on vector length that is speed)
    color       = color of bot
    freezeTime  = time bot is freezed when game.env starts (units is not sec, adjust manually as
    unit depends on time taken by each loop/render frame)
    '''



    def __init__(self, point, name ,viewAngle=45, speed=7,radius=5, color=(255,255,255),freezeTime=200):
        self.ishider = True
        self.x = point[0]
        self.y = point[1]
        self.viewAngle = viewAngle
        self.rayEndPoints = {}
        self.r = radius
        self.speed = speed
        self.vector = (self.x + random.randint(-10,10), self.y +random.randint(-10,10))
        self.color=color
        self.name = name
        self.freezeTime = freezeTime
        self.sensitivity = 50



class Seeker:

        '''
        Seeker is bot class that has characteristic of Seeker.
        takes arguments as follows:
        point       = start point
        name        = name of bot
        viewAngle   = vision angle
        speed       = rate of change of cordinates (x and y will change based on vector length that is speed)
        color       = color of bot
        freezeTime  = time bot is freezed when game.env starts (units is not sec, adjust manually as
        unit depends on time taken by each loop/renderf rame)
        '''

        def __init__(self, point,name, viewAngle=10, radius=5, color=(255, 255, 255),freezeTime=200):
            self.ishider = False
            self.x = point[0]
            self.y = point[1]
            self.viewAngle = viewAngle
            self.rayEndPoints = {}
            self.r = radius
            self.speed = 7
            self.vector = (self.x + random.randint(-10, 10), self.y + random.randint(-10, 10))
            self.color = color
            self.otherSpotted = {}
            self.name = name
            self.sensitivity = 50
            self.freezeTime = freezeTime






class Environment:

    '''
    Environment class which takes two keyword arg that are window size, record file name and motion type
    '''


    def __init__(self, window, record=None,motion=None):
        self.window = window
        self.points = [[0,0],[0,window[1]],[window[0],0],[window[0],window[1]]]
        self.bg_color = (0,0,0)
        self.frame = np.array( [[self.bg_color]*window[0]]*window[1], dtype=np.uint8)
        self.blank = np.array( [[self.bg_color]*window[0]]*window[1], dtype=np.uint8)
        self.walls = [[[0,0],[window[0],0],'wall'],
                      [[window[0],0],[window[0],window[1]],'wall'],
                       [[window[0],window[1]],[0,window[1]],'wall'],
                        [[0,window[1]],[0,0],'wall']]
        self.players = {}
        self.selected_Player = None
        self.thickness = 1

        if record:
            self.record = cv2.VideoWriter(record[0], cv2.VideoWriter_fourcc(*record[1]),  20.0, self.window)
        else:
            self.record = None
        if motion:
            if motion == 'MOUSE' or motion == 'STILL' or motion == 'RANDOM':
                self.motion = motion
            else:
                self.motion = 'STILL'



    def runRender(self):
        cv2.imshow("RayTracing", self.frame)
        # time.sleep(3)
        while True:
            self.temp_frame = self.frame.copy()
            for _, player_ in self.players.items():
                    # print (player_.color)
                    self.scanEnv(player_)
                    self.drawRay(player_)
                    self.drawSource(player_)


            if self.selected_Player:
                cv2.putText(self.temp_frame, "Selected - {}".format(self.selected_Player), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2,
                            cv2.LINE_AA, False)
            if self.record:

                self.record.write(self.temp_frame)
            cv2.imshow("RayTracing", self.temp_frame)
            self.moveSource()
            if cv2.waitKey(80) == ord('q'):
                self.record.release()
                break


    def feed(self,actions):
        player_data = {}
        self.temp_frame = self.frame.copy()
        for player_ in actions:
                player = self.players[player_]
                self.rotateplayer(player, actions[player_]['rotate'])
                if actions[player_]['forward']:
                    self.moveforward(player)
                self.scanEnv(player)
                self.drawRay(player)
                self.drawSource(player)
                reward = 0
                for x in range(-30,30,10):
                    if x in player.rayEndPoints:
                        if  0 < player.rayEndPoints[x][0] < 50:
                            reward -= 10
                        if 0 > player.rayEndPoints[x][0] and player.ishider:
                            reward -= 200
                        if 0 > player.rayEndPoints[x][0] and not player.ishider:
                            reward += 200
                        if 150 <  player.rayEndPoints[x][0] :
                            reward += 10
                    else:
                        player.rayEndPoints[x] = 0
                        reward  -= 200


                player_data[player_] = {}
                player_data[player_]['position'] = (player.x,player.y)
                player_data[player_]['vector'] = player.vector
                player_data[player_]['rayEnds'] = player.rayEndPoints
                player_data[player_]['reward'] = reward
                player_data[player_]['isHider'] = player.ishider
        return player_data, self.temp_frame


    # def action(self,actions):
    #     for player in actions:

    def moveSource(self):

            if self.motion == 'MOUSE':
                cv2.setMouseCallback("RayTracing", self.mouselocate,self.players)
            elif self.motion == 'RANDOM':
                for _, player_ in  self.players.items():
                    if player_.rayEndPoints:
                        self.update(self.window,player_)
            else:
                pass

    def locate(self,x,y,event,player):

        x_ = player.x
        y_ = player.y
        r  = player.r
        v = player.vector
        if  x_ - r - 100 < x < x_+ r+100 and y_- r -100 < y < y_ +r+100:
            distance = self.get_distance((x, y), (x_, y_))
            selected = player.r + 100 > distance > player.r+10
            # if selected and cv2.waitKey(40) == ord('w'):
            if selected :
                self.selected_Player = player.name
                # print (player.name)
                player.x = int((x_+x)/2)
                player.y = int((y_+y)/2)
                player.vector = (x, y)
        else:
            self.selected_Player = None

    def construct_walls(self, player):
        walls = []
        for player_, _ in self.players.items():
            if player.name != player_:
                x = _.x
                y = _.y
                size = 7

                walls.append( [ (x-size, y), (x+size, y), player_] ) #lt,lb
                walls.append( [ (x, y-size), (x, y+size), player_] ) #rt,rb


        return walls


    def mouselocate(self,event, x, y, flags, players):

        if self.selected_Player:
            self.locate(x, y, event, players[self.selected_Player])
        else:
            for _,player in players.items():
                    self.locate(x, y, event, player)
                    if self.selected_Player:
                        break

    def drawSource(self,player):

        cv2.circle(self.temp_frame, (player.x, player.y), player.r, (255,255,255),-1)

    def drawRay(self,player):

        for ray, values in player.rayEndPoints.items():
            if values and player.color!=(255,255,255):

                cv2.line(self.temp_frame, (player.x,player.y), tuple(values[1]), player.color, 1)

    def addPlayer(self,player):

        try:
            self.players[player.name] = player
        except:
            raise

    def addObject(self,Object):

        try:
            for wall in Object.walls:
                self.walls.append(wall+['wall'])
                cv2.line(self.frame, wall[0], wall[1], Object.color, 1)
        except:
            raise


    def get_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]
        div = det(xdiff, ydiff)
        if div == 0:
            return None
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return [round(x,2), round(y,2)]

    def get_distance(self,p1,p2):

        return  ceil( (((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2))**(1/2))

    def getDirection(self,visionData):
        pass

    def rotateplayer(self,player,angle):
        if angle!=0:
            angle = int((angle/abs(angle))*(((abs(angle))//10)+1)*10)#+int(angle/abs(angle))*10
        # print (angle)
        angle_ =   self.get_Context_angle(angle,player)
        xvector =  player.x + 100*sin(radians(angle_))
        yvector =  player.y + 100*cos(radians(angle_))
        player.vector = (ceil(xvector) , ceil(yvector))

    def moveforward(self,player):

            angle_ =   self.get_Context_angle(0,player)
            player.x =  ceil(player.x + player.speed*sin(radians(angle_)))
            player.y =  ceil(player.y + player.speed*cos(radians(angle_)))
            xvector =  player.x + 100*sin(radians(angle_))
            yvector =  player.y + 100*cos(radians(angle_))
            player.vector = (ceil(xvector) , ceil(yvector))



    def update(self,window,player):
        visionData = player.rayEndPoints
        # choices = [a for a in range(-60, 60, 20)]
        # if visionData[0][0] < 10:
        #     self.rotateplayer(player, 180)
        #     self.moveforward(player)
        #     return
        # for x in range(-5,6):
        #     if 0<= visionData[x][0] <200:
        #         # Need more improvement - random rotation for now
        #         self.rotateplayer(player, random.choice(choices))
        #         # -----------------------------------------------
        #         self.moveforward(player)
        #         return
        #     elif visionData[x][0]<0:
        #         self.rotateplayer(player, random.choice([-90,90]))
        #         self.moveforward(player)
        #         return
        #
        # self.moveforward(player)
        # if 0 > player.x or window[0] < player.x:
        #     player.x = int(window[0]/2)
        #     player.y = int(window[1]/2)
        #
        # if 0 > player.y or window[1] < player.y:
        #     player.x = int(window[0] / 2)
        #     player.y = int(window[1] / 2)

        collide = False
        rotate, dA = self.decideRotation(visionData)
        self.rotateplayer(player, rotate)
        for a_, d_ in visionData.items():
            if d_[0] < 60:
                collide = True

        if not collide:
            self.moveforward(player)
        else:

            if rotate == 0:
                rotate = dA
            self.rotateplayer(player,dA)


    def decideRotation(self,visionData):

        s = 150
        total = 0
        dA = 0
        max = 0
        total_l = 0
        total_r = 0
        for a_, d_  in visionData.items():
            # s_weight
            if d_[0] < s:
                    total+=d_[0] #*(1+1-1/(abs(a_)+1))
                    max+= s #*(1-1/(abs(a_)+1))


            else:
                total+=s*(1-1/(abs(a_)+1))
            if a_ < 0:
                total_l += d_[0] #* (1 +1- 1 / (abs(a_) + 1))
            if a_ > 0:
                total_r += d_[0] #* (1 +1- 1 / (abs(a_) + 1))

        if total <= max/2:
            if total_l > total_r:
                angle = -90
            else:
                angle = +90

        else:
            avg = total/len(visionData.keys())
            angle = 0
            diff =  -s
            dA = 0

            for a_, d_ in visionData.items():
                if abs(d_[0]) - avg >= diff :
                    dA = angle
                    angle = a_
                    diff = d_[0] - avg

        return angle ,dA









    def get_Context_angle(self,angle,player):

        dx = player.x - player.vector[0]
        dy = player.y - player.vector[1]
        return  -90 - (angle + int(np.rad2deg(np.arctan2(dy,dx))))


    def scanEnv(self, player):


        player.rayEndPoints = {}

        for type in [self.walls,self.construct_walls(player)]:
            for wall in type:
                for angle_ in range(-1*player.viewAngle,player.viewAngle+1):

                    angle = self.get_Context_angle(angle_,player)
                    angle = radians(angle)
                    x1 = player.x + 0.01*sin(angle)
                    y1 = player.y + 0.01*cos(angle)
                    x0 = player.x
                    y0 = player.y
                    ray =([x0,y0],[x1,y1])
                    intercept = self.get_intersection(wall[:2], ray)
                    x_ = [wall[0][0],wall[1][0]]
                    y_ = [wall[0][1],wall[1][1]]
                    if intercept:
                            if x1 <= intercept[0] < x0 and x1 <= intercept[1]  < y0 :
                                intercept = [ x0, y0]
                            if (min([x0, intercept[0]]) <= x1 <= max([x0, intercept[0]]) and min(
                                    [y0, intercept[1]]) <= y1 <= max([y0, intercept[1]])):
                                if min(x_) <= intercept[0] <= max(x_) and min(y_) <= intercept[1] <= max(y_):

                                    intercept = [int(round(intercept[0], 0)), int(round(intercept[1], 0))]
                                    distance =self.get_distance([player.x, player.y], intercept)
                                    if angle_ not in player.rayEndPoints:
                                        player.rayEndPoints[angle_]= [distance,intercept]
                                    else:
                                        if  player.rayEndPoints[angle_][0] > distance+1:
                                            player.rayEndPoints[angle_] = [distance, intercept]
                                            if wall[2] != 'wall' and (self.players[wall[2]].ishider and not player.ishider):
                                                self.players[wall[2]].color = (255, 255, 255)
                                                self.players[wall[2]].speed = 0
                                                player.rayEndPoints[angle_] = [-30, intercept]
                                            elif wall[2] != 'wall' and ( not self.players[wall[2]].ishider and player.ishider):
                                                player.rayEndPoints[angle_] = [-30, intercept]



