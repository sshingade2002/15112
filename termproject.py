import math, copy, random
from cmu_112_graphics import *
import tkinter as tk
class Arrow(object):
    weight = 22.68 # grams
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.v0 = 0
        self.IBO = 105.68 # m/s
        self.addWeight = 1.296 # g
        self.drawWeight = 31751 # g 
        self.dy = 0
        self.dx = 0
        
    
    def findInitialSpeed(self, power):
        # v = IBO + (L - 30) * 10 - W / 3 + min (0, -(A - 5D)/3)
        # assume that additional weigth on string (W) and draw weight (D) are constant values
        # power is propotional to the draw length 
        # assume that peak draw is a constant 70 lbs
        #power will be from 10- 100 and maxL is 2
        maxL = 50
        L = power/100*maxL
        self.v0 = self.IBO + (L - 30) * 10 - self.addWeight / 3 + min (0, -(Arrow.weight - 5*self.drawWeight)/3)
        return self.v0
        
    
class Target(object):
    sizeOfRings = 10 # pixels
    sizeOfInnerRing = 5 # pixels
    def __init__(self, rings):
        self.x = 0
        self.y = 0
        self.rings = rings
    
    def generateRandomLocation(self, xRange, yRange):
        x = random.randint(xRange[0], xRange[1])
        y = random.randint(yRange[0], yRange[1])
        self.x = x
        self.y = y
        return





def playGame():
    margin = 25
    height = 700+2*margin
    width = 700+2*margin
    runApp(width=width, height=height, title='Game') 

def appStarted(app):
    app.margin = 25
    app.startPostion = (app.margin,app.height-app.margin)
    app.arrow = Arrow(app.startPostion[0], app.startPostion[1], math.pi/4)

    app.target1 = Target(3)
    app.xRange = (app.width-app.margin-30-(app.width-app.margin*2)//2,app.width-app.margin-30)
    upperlimit = app.height-app.margin-30*app.target1.rings
    lowerlimit = app.margin + 30*app.target1.rings
    app.yRange = (lowerlimit,upperlimit)
    app.target1.generateRandomLocation(app.xRange, app.yRange)

    app.arrowPresent = False
    app.shoot = False
    ###################
    app.timerDelay = 100
    ####################
    app.timer = 40*1000
    
    app.trajectoryCirlces = []
    
    app.ypos = 0
    app.level = 1
    app.score = 0
    app.babyAI = False
    app.babyAILevel = 0

    app.waitingForKeyPress = True
    app.popupMode = False
    app.startLevelPopup = False
    app.endLevelPopup = False
    app.shootTimer = 0
    
    app.playerAngle = math.pi/4
    app.incrementAngle = math.pi/32
    app.power = 50
    app.wind = 0
    app.windAngle = 0
    app.angleQuadrant = 0
    app.targetIncrement = 10
    app.powerInc = 5

    app.babyAIpopup = True
    app.aiTrajectory = []
    app.aiarrow = Arrow(app.startPostion[0], app.startPostion[1], 0)
    app.aiTurn = False
    app.targetLocations = set()
    app.lenLast = 0
    app.airounds =  0
    app.timeTime = 0
    app.aiLaunch = False
    app.aiyposition = 0
    app.aiTimer = 0 
    app.aiScore = 0
    app.aiEndPopup = False
    

def findOptimalStationary(app, targetx, targety):
        arrow = app.aiarrow
        
        upperRangeLim = int((math.pi/2)/(app.incrementAngle))
        for angleF in range(1, upperRangeLim):
            angle = app.incrementAngle*angleF
            for power in range(10, 100):            # powerInc
                time = 0 
                x,y = app.startPostion
                arrow.angle = angle
                arrow.findInitialSpeed(power)
                
                a=9.81
                velocity = arrow.v0
                vx=velocity * math.cos(angle)
                vy=velocity * math.sin(angle)
                dx = 0
                while -1 < dx < app.width-app.margin:
                    time += app.timerDelay
                    t = time/1000
                    dx = x+vx*t
                    # print('dx', dx, 'targetx', targetx)
                    if targetx-10 <= dx <= targetx+10:
                        break

                if targetx-10 <= dx <= targetx+10:
                    dy = y-(vy*t - (a/2)*t*t)
                    if targety-10 <= dy <= targety+10:
                        app.timeTime = time 
                        return (power, angle)

        return None

def findOpMoving(app):
    target = app.target1
    xcst = target.x
    upperlimit = app.height-app.margin-30*target.rings*2
    lowerlimit = app.margin + 30*target.rings*2
    app.aiyposition = random.randint(lowerlimit, upperlimit)
    opower, oangel = findOptimalStationary(app,xcst, app.aiyposition)
    app.ypos = 1
    app.aiarrow.angle = oangel
    app.aiarrow.findInitialSpeed(opower)
    print(app.timeTime)
    



def timerFired(app):
    if not app.waitingForKeyPress:
        if app.babyAI:
            if app.airounds > 0:
                updateTargetPosition(app)
                
                    
            if app.timer//1000 >= 60:
                # playerscore = app.score
                print(app.aiTimer, app.airounds)
                if app.aiTimer == 1:
                    app.aiTimer = -1 
                    app.airounds += 1
                    if app.airounds == 2:
                        app.aiEndPopup = True
                if not app.aiTurn:
                    app.ypos = 1
                    app.arrowPresent = True
                    app.aiarrow.v0 = 0
                    app.aiarrow.x, app.aiarrow.y = app.startPostion
                    app.aiTrajectory = []
                    # app.score += playerscore
                else:
                    app.arrowPresent = False
                    app.trajectoryCirlces = []
                    app.arrow.x, app.arrow.y = app.startPostion
                    app.shoot = False
                    app.arrow.v0 = 0
                app.aiTimer += 1

                app.target1.generateRandomLocation(app.xRange, app.yRange)
                app.shootTimer = 0
                app.arrow.v0 = 0
                app.timer = 40*1000
                app.aiTurn = not app.aiTurn
                # app.score = 0
                app.targetLocations = set()
            app.timer += app.timerDelay

            if app.aiTurn:
                
                if app.aiarrow.v0 == 0 and app.babyAILevel == 1 and app.airounds > 0 :
                    findOpMoving(app)
                    # print(app.timeTime)
                else:
                    if app.aiarrow.v0 == 0 and app.babyAILevel == 1:
                        aiPandA(app, 10, 2)
                    elif app.aiarrow.v0 == 0 and app.babyAILevel == 2:
                        aiPandA(app, 10, 1)

                if app.airounds > 0:
                    if app.aiLaunch:
                        levelOneai(app)

                        # app.aiLaunch = False
                else:
                    levelOneai(app)
            else:
                levelOne(app)
        else:
            if app.level == 2 or app.level == 3:
                updateTargetPosition(app)
            if app.arrowPresent:
                if app.timer//1000 >= 60:
                    app.arrowPresent = False
                    app.endLevelPopup = True
                    app.arrow.v0 = 0
                app.timer += app.timerDelay
                if app.level == 1:
                    levelOne(app)
                elif app.level == 2:
                    levelTwo(app)
                elif app.level == 3:
                    levelThree(app)


def levelOneai(app):
    if app.airounds > 0:
        if app.aiLaunch:
            app.shootTimer += app.timerDelay
            app.aiTrajectory.append((app.aiarrow.x, app.aiarrow.y))
            updateAIArrowPostion(app)
            checkAIIfHit(app)
    elif app.ypos == 1 and app.aiTurn:
        app.shootTimer += app.timerDelay
        app.aiTrajectory.append((app.aiarrow.x, app.aiarrow.y))
        updateAIArrowPostion(app)
        checkAIIfHit(app)

def updateAIArrowPostion(app): 
    a=9.81
    velocity = app.aiarrow.v0
    angle = app.aiarrow.angle
    
    vx=velocity * math.cos(angle)
    vy=velocity * math.sin(angle)
    t=app.shootTimer/1000
    x = app.startPostion[0]
    y = app.startPostion[1]

    dx = x+vx*t
    dy = y-(vy*t - (a/2)*t*t)

    # print('update', velocity, angle, dx, dy)

    app.aiarrow.dy = vy
    app.aiarrow.dx = vx
    
    app.aiarrow.x = dx
    app.aiarrow.y = dy

    
    if dy > y or dy < 0:
        # app.ypos = 0
        # app.aiTurn = False
        app.level = 1
        # app.ypos = 1
        # app.timer = 55*1000

        # app.score = 0
        app.aiarrow.v0 = 0
        app.aiarrow.x, app.aiarrow.y = app.startPostion
        app.aiTrajectory = []
        app.shootTimer = 0
        app.aiLaunch = False
        # print(app.aiTrajectory)
    

def checkAIIfHit(app):
    target = app.target1
    # print(target.x-10, app.arrow.x, target.x+10)
    score = False
    if len(app.aiTrajectory) > 2 and app.aiTrajectory[-1][0] <= target.x <= app.aiarrow.x:
        if target.y-target.rings*5 <= app.aiarrow.y <= target.y+target.rings*5:
            app.aiScore += 20
            app.ypos = 0
            score = True
        elif target.y-target.rings*20 <= app.aiarrow.y <= target.y+target.rings*20:
            app.aiScore += 10
            app.ypos = 0
            score = True
        elif target.y - target.rings*30 <= app.aiarrow.y <= target.y + target.rings*30:
            app.aiScore += 5
            app.ypos = 0
            score = True

    elif app.aiarrow.x >= app.width-app.margin:
        app.ypos = 0 
        # app.aiTurn = False
        # print(app.aiTrajectory)
    
    if score:
        target.generateRandomLocation(app.xRange, app.yRange)
    if app.ypos == 0:
        app.aiTrajectory = []
        app.aiarrow.x, app.aiarrow.y = app.startPostion
        app.shootTimer = 0
        app.aiarrow.v0 = 0
        app.aiLaunch = False
        

def levelOne(app):
    if app.ypos == 1 and app.shoot:
        app.shootTimer += app.timerDelay
        app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
        updateArrowPostion(app)
        checkIfHit(app)
    

def levelTwo(app):
    if app.ypos == 1 and app.shoot:
        app.shootTimer += app.timerDelay
        app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
        updateArrowPostion(app)
        # updateTargetPosition(app)
        checkIfHit(app)

def levelThree(app):
    if app.ypos == 1 and app.shoot:
        app.shootTimer += app.timerDelay
        app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
        updateArrowPostionWithWind(app)
        # updateTargetPosition(app)
        checkIfHit(app)

# only changes y 
def updateTargetPosition(app):
    target = app.target1
    dyDown = target.y+target.rings*30+app.targetIncrement
    dyUp = target.y-target.rings*30+app.targetIncrement
    if dyDown >= app.height - app.margin or dyUp <= app.margin:
        app.targetIncrement = -app.targetIncrement
    else:
        target.y += app.targetIncrement
    
    if app.aiTurn and app.aiyposition != 0:
        targety = target.y
        speed = app.targetIncrement 
        targetTime = 0
        count = 0 
        while not (app.aiyposition-10 <= targety <= app.aiyposition+10) and count <= 100:
            # print(app.aiyposition-10, targety, app.aiyposition+10)
            
            dyDown = targety+target.rings*30+speed
            dyUp = targety-target.rings*30+speed
            if dyDown >= app.height - app.margin or dyUp <= app.margin:
                speed = -speed
            else:
                targety += speed
            targetTime += app.timerDelay
            count += 1
        # print('outside')
        if count >= 100:
            print('stuck')
        if app.timeTime-app.timerDelay*2 <= targetTime <= app.timeTime+app.timerDelay*2:
            app.aiLaunch = True
            print('targetTime', targetTime)


def checkIfHit(app):
    target = app.target1
    score = False
    # print(target.x-10, app.arrow.x, target.x+10)
    if len(app.trajectoryCirlces) > 2 and app.trajectoryCirlces[-1][0] <= target.x <= app.arrow.x:
        # print('inside')
        
        # print(target.y-target.rings*5, app.arrow.y, target.y+target.rings*5)
        if target.y-target.rings*5 <= app.arrow.y <= target.y+target.rings*5:
            app.score += 20
            app.ypos = 0
            score = True
        elif target.y-target.rings*20 <= app.arrow.y <= target.y+target.rings*20:
            app.score += 10
            app.ypos = 0
            score = True
        elif target.y - target.rings*30 <= app.arrow.y <= target.y + target.rings*30:
            app.score += 5
            app.ypos = 0
            score = True

    elif app.arrow.x >= app.width-app.margin:
        app.ypos = 0 
    
    if score:
        target.generateRandomLocation(app.xRange, app.yRange)
    if app.ypos == 0:
        app.trajectoryCirlces = []
        app.arrow.x, app.arrow.y = app.startPostion
        app.shootTimer = 0
        app.shoot = False
        app.arrow.v0 = 0
        # app.aiTurn = False
        

def updateArrowPostionWithWind(app): 
    a=9.81
    velocity = app.arrow.v0
    angle = app.arrow.angle
    wind = app.wind
    windAngle = app.windAngle
    windQuadrant = app.angleQuadrant
    wx = wy = 0

    if windQuadrant == 1 or windQuadrant == 2:
        wy = wind*math.sin(windAngle)
    else:
        wy = -wind*math.sin(windAngle)

    if windQuadrant == 1 or windQuadrant == 4:
        wx = wind*math.cos(windAngle)
    else:
        wx = -wind*math.cos(windAngle)
    
    
    vx = velocity * math.cos(angle)
    vxw = velocity * math.cos(angle) + wx
    vy = velocity * math.sin(angle) + wy
    t = app.shootTimer/1000
    x = app.startPostion[0]
    y = app.startPostion[1]

    dxw = x+vxw*t
    dx = x+vx*t
    dy = y-(vy*t - (a/2)*t**2)
    # print('dxw', dxw, 'dx', dx)
    app.arrow.dy = vy
    app.arrow.dx = vxw
    
    app.arrow.x = dxw
    app.arrow.y = dy

    if dy > y or dy < 0:
        app.ypos = 0

def updateArrowPostion(app): 
    a=9.81
    velocity = app.arrow.v0
    angle = app.arrow.angle
    vx=velocity * math.cos(angle)
    vy=velocity * math.sin(angle)
    t=app.shootTimer/1000
    x = app.startPostion[0]
    y = app.startPostion[1]

    dx = x+vx*t
    dy = y-(vy*t - (a/2)*t*t)

    app.arrow.dy = vy
    app.arrow.dx = vx
    
    app.arrow.x = dx
    app.arrow.y = dy

    if dy > y or dy < 0:
        app.ypos = 0
        # app.aiTurn = False

def mousePressed(app, event):
    if app.popupMode:
        x0 = 200
        y0 = 200
        x1 = app.width-x0
        y1 = app.height - 2*y0

        margin = 5
        x0new = x0+margin
        y0new = y0+margin
        x1new = x0new+(x1-x0)/2-margin
        y1new = y0new+(y1-y0)-margin*2

        x0new1 = x1new+margin
        y0new1 = y0+margin
        x1new1 = x0new1+(x1-x0)/2-margin*2
        y1new1 = y0new1+(y1-y0)-margin*2

        if x0new <= event.x <= x1new and y0new <= event.y <= y1new:
            app.babyAI = False
            app.popupMode = False
            app.startLevelPopup = True
        elif x0new1 <= event.x <= x1new1 and y0new1 <= event.y <= y1new1:
            app.babyAI = True
            app.popupMode = False
            app.babyAIpopup = True
            app.aiTurn = True
            
def aiPandA(app, powerRange, angleRange):
    if findOptimalStationary(app, app.target1.x, app.target1.y) != None:
        aipower, aiangle = findOptimalStationary(app, app.target1.x, app.target1.y)
        
        # print('ai', aipower, aiangle)
        
        aipower = random.randint(aipower-powerRange, aipower+powerRange)
        aiangle = random.uniform(max(aiangle-app.incrementAngle*angleRange,0),
                            min(math.pi/2, aiangle+app.incrementAngle*angleRange))
                            
        app.ypos = 1
        app.aiarrow.angle = aiangle
        app.aiarrow.findInitialSpeed(aipower)
        # print('ai', aipower, aiangle)
    else:
        print('NONE')

def keyPressed(app, event):
    # print('key pressed')
    if app.waitingForKeyPress:
        app.waitingForKeyPress = False
        app.popupMode = True
        app.babyAIpopup = False

    if app.startLevelPopup:
        if (event.key == 'Up' or 
            event.key == 'Down' or
            event.key == 'Right' or 
            event.key == 'Left'):
            app.startLevelPopup = False
            app.arrowPresent = True
            app.babyAIpopup = False

    elif not app.popupMode and not app.startLevelPopup:
        if event.key == 'r':
            appStarted(app)
        if event.key == 'o':
            app.popupMode = not app.popupMode
            if app.popupMode:
                app.startLevelPopup = False
                app.endLevelPopup = False

        if app.babyAI and app.aiTurn:
            aipower = 0
            aiangle = 0
            if event.key == '1':
                app.babyAILevel = 1
                app.babyAIpopup = False

            if event.key == '2':
                app.babyAILevel = 2
                app.babyAIpopup = False
                
            if event.key == '3':
                app.babyAILevel = 3

        if app.arrow.v0 == 0 and not app.aiTurn:
            
            if event.key == 's':
                # print('ai shooot')
                app.shoot = True
                app.arrowPresent = True
                app.ypos = 1
                app.arrow.findInitialSpeed(app.power)
                app.arrow.x = app.startPostion[0]
                app.arrow.y = app.startPostion[1]
            if event.key == 'Up' :
                updateArrowAngle(app, 'Up')
            if event.key == 'Down':
                updateArrowAngle(app, 'Down')
            if event.key == 'Right':
                if app.power < 100:
                    app.power += app.powerInc
            if event.key == 'Left':
                if app.power > 10:
                    app.power -= app.powerInc
            if event.key == 'a':
                app.babyAI = True
            else:
                if event.key == '1':
                    print("1")
                    app.level = 1
                    app.ypos = 1
                    app.timer = 40*1000
                    app.score = 0 
                    app.power = 50
                    app.playerAngle = math.pi/4
                    app.arrowPresent = True
                    app.endLevelPopup = False
                if event.key == '2':
                    app.level = 2
                    app.ypos = 1
                    app.timer = 40*1000
                    app.score = 0
                    app.power = 50
                    app.playerAngle = math.pi/4
                    app.arrowPresent = True
                    app.endLevelPopup = False
                if event.key == '3':
                    app.arrowPresent = True
                    app.endLevelPopup = False
                    app.ypos = 1
                    app.timer = 40*1000
                    app.score = 0
                    app.power = 50
                    app.playerAngle = math.pi/4
                    app.wind = random.randint(0, 30)
                    app.windAngle = random.uniform(0, math.pi/2)
                    app.angleQuadrant = random.randint(1, 4)
                    print(app.windAngle, app.angleQuadrant, app.wind)
                    app.level = 3
        

def updateArrowAngle(app, direction):
    if direction == 'Down':
        if app.playerAngle-app.incrementAngle < 0-app.incrementAngle:
            return
        else:
            app.playerAngle -= app.incrementAngle
    elif direction == 'Up':
        if app.playerAngle+app.incrementAngle > math.pi/2+app.incrementAngle:
            return
        else:
            app.playerAngle += app.incrementAngle
    
    app.arrow.angle = app.playerAngle

def drawTarget1(app, canvas):
    x0 = app.target1.x-30
    y0 =  app.target1.y-app.target1.rings*30
    x1 =  app.target1.x+30
    y1 =  app.target1.y+app.target1.rings*30
    canvas.create_oval(x0, y0, x1, y1, fill='blue')

    x0 = app.target1.x-20
    y0 =  app.target1.y-app.target1.rings*20
    x1 =  app.target1.x+20
    y1 =  app.target1.y+app.target1.rings*20
    canvas.create_oval(x0, y0, x1, y1, fill='green')

    x0 = app.target1.x-5
    y0 =  app.target1.y-app.target1.rings*5
    x1 =  app.target1.x+5
    y1 =  app.target1.y+app.target1.rings*5
    canvas.create_oval(x0, y0, x1, y1, fill='red')


def drawTrajectory(app, canvas):
    for x,y in app.trajectoryCirlces:
        canvas.create_oval(x-2, y-2, x+2, y+2, fill = 'black')

def drawaiTrajectory(app, canvas):
    for x,y in app.aiTrajectory:
        canvas.create_oval(x-2, y-2, x+2, y+2, fill = 'yellow')

def drawAIScore(app, canvas):
    x0 = app.margin
    y0 = app.margin
    canvas.create_text(x0, y0, text=f"AI = {app.aiScore}", anchor = 'w')

def drawAngle(app, canvas):
    angle = app.playerAngle
    arrowL = 30
    x0 = app.startPostion[0]
    y0 = app.startPostion[1]
    x1 = arrowL*math.cos(angle)+x0
    y1 = y0-arrowL*math.sin(angle)
    canvas.create_line(x0,y0,x1,y1)

def drawScore(app, canvas):
    x0 = app.margin
    y0 = app.margin
    canvas.create_text(x0, y0, text=f"Score = {app.score}", anchor = 'w')

def drawPower(app, canvas):
    x0 = app.width - app.margin
    y0 = app.height - app.margin
    canvas.create_text(x0, y0, text=f"Power = {app.power}", anchor = 'e')

def drawWind(app, canvas):
    x0 = app.width - app.margin
    y0 = app.margin*2
    canvas.create_text(x0, y0, text=f"Wind: {app.wind} m/s", anchor = 'e')
    angle = app.windAngle
    if app.angleQuadrant == 2:
        angle = math.pi - angle
    elif app.angleQuadrant == 3:
        angle += math.pi
    elif app.angleQuadrant == 4:
        angle = math.pi * 2 - angle
    
    arrowL = 30
    x0 = app.width-app.margin*3
    y0 = app.margin*4
    x1 = arrowL*math.cos(angle)+x0
    y1 = y0-arrowL*math.sin(angle)
    canvas.create_line(x0,y0,x1,y1, arrow=tk.LAST)


def drawTimer(app, canvas):
    x0 = app.width - app.margin
    y0 = app.margin
    drawString = ''
    if app.timer//1000 < 10:
        drawString = '0:0'+str(app.timer//1000)
    elif app.timer//1000 < 60:
        drawString = '0:'+str(app.timer//1000)
    else:
        drawString = '1:00'

    canvas.create_text(x0, y0, text="Timer "+drawString, anchor = 'e')

def drawRounds(app, canvas):
    x0 = app.margin
    y0 = app.margin*2
    canvas.create_text(x0, y0, text=f"Round {app.airounds}", anchor = 'w')

def redrawAll1(app, canvas):
    x0 = app.startPostion[0]-10
    y0 = app.startPostion[1]-10
    x1 = app.startPostion[0]+10
    y1 = app.startPostion[1]+10
    canvas.create_oval(x0, y0, x1, y1, fill='green')

    drawTarget1(app, canvas)
    # drawTarget2(app, canvas)
    drawAngle(app, canvas)
    drawScore(app, canvas)
    drawPower(app, canvas)
    drawTimer(app, canvas)
    if app.level == 3:
        drawWind(app, canvas)
    if app.arrowPresent: 
        # drawArrow(app, canvas)
        drawTrajectory(app, canvas)

def redrawAll2(app, canvas):

    x0 = app.startPostion[0]-10
    y0 = app.startPostion[1]-10
    x1 = app.startPostion[0]+10
    y1 = app.startPostion[1]+10
    canvas.create_oval(x0, y0, x1, y1, fill='green')

    drawTarget1(app, canvas)
    drawAIScore(app, canvas)
    drawTimer(app, canvas)
    # drawRounds(app, canvas)
    if app.aiTrajectory != []:
        drawaiTrajectory(app, canvas)

def drawSpashScreen(app, canvas):
    x0 = 0
    y0 = 0
    x1 = app.width
    y1 = app.height
    canvas.create_rectangle(x0,y0,x1,y1, fill = 'pink')
    welcomeText = '''Welcome to Sh00t S0ur Sh0t!\n
                    This is a bow and arrow game in which you will attempt to\n
                    hit the target to gain points. There are two modes: solo play\n
                    and computer play. Solo play involves simply playing through the\n
                    three levels each round one minute long. Computer play involves\n
                    playing against the computer for three rounds.\n
                    When playing, click 'o' to choose between solo and computer\n
                    Click any key to start!
                    '''
    canvas.create_text(x1//2, y1//2, text = welcomeText)

def drawPopupMode(app, canvas):
    x0 = 200
    y0 = 200
    x1 = app.width-x0
    y1 = app.height - 2*y0

    canvas.create_rectangle(x0,y0,x1,y1, fill = 'gray')

    margin = 5
    x0new = x0+margin
    y0new = y0+margin
    x1new = x0new+(x1-x0)/2-margin
    y1new = y0new+(y1-y0)-margin*2
    canvas.create_rectangle(x0new, y0new, x1new, y1new, fill = 'blue')
    canvas.create_text(x0new+(x1new-x0new)/2, y0new+(y1new-y0new)/2, text = 'Solo Mode')

    x0new1 = x1new+margin
    y0new1 = y0+margin
    x1new1 = x0new1+(x1-x0)/2-margin*2
    y1new1 = y0new1+(y1-y0)-margin*2
    canvas.create_rectangle(x0new1, y0new1, x1new1, y1new1, fill = 'blue')
    canvas.create_text(x0new1+(x1new1-x0new1)/2, y0new1+(y1new1-y0new1)/2, text = 'Computer Mode')
    
def drawStartLevelPopup(app, canvas):
    x0 = 200
    y0 = 200
    x1 = app.width-x0
    y1 = app.height - 2*y0

    canvas.create_rectangle(x0,y0,x1,y1, fill = 'gray')
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text = 'Click any arrow keys to start')
    canvas.create_text(x0+(x1-x0)/2, 20+y0+(y1-y0)/2, text = f'Level {app.level}', anchor = 's')

def drawEndLevelPopup(app, canvas):
    x0 = 200
    y0 = 200
    x1 = app.width-x0
    y1 = app.height - 2*y0

    canvas.create_rectangle(x0,y0,x1,y1, fill = 'gray')
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2-60, text = f'Finished Level {app.level}. Score: {app.score}')
    levelstrings = '''Press 1 to play Level 1\nPress 2 to play Level 2\nPress 3 to play Level 3'''
    canvas.create_text(x0+(x1-x0)/2, 20+y0+(y1-y0)/2, text = levelstrings, anchor = 's')

def drawbabAIpopup(app, canvas):
    x0 = 200
    y0 = 200
    x1 = app.width-x0
    y1 = app.height - 2*y0

    canvas.create_rectangle(x0,y0,x1,y1, fill = 'gray')
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2-50, text = f'Finished Level {app.level}. Score: {app.score}')
    levelstrings = '''Press 1 to play Easy Mode \nPress 2 to play Hard Mode\n'''
    canvas.create_text(x0+(x1-x0)/2, 30+y0+(y1-y0)/2, text = levelstrings, anchor = 's')

def drawbabAIENDpopup(app, canvas):
    x0 = 200
    y0 = 200
    x1 = app.width-x0
    y1 = app.height - 2*y0

    canvas.create_rectangle(x0,y0,x1,y1, fill = 'gray')
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2-50, text = f'Finished Level AI rounds. AI score:{app.aiScore} Score: {app.score}')
    levelstrings = 'click "o" to return to mode selection'
    canvas.create_text(x0+(x1-x0)/2, 30+y0+(y1-y0)/2, text = levelstrings, anchor = 's')
def redrawAll(app, canvas):
    # print(app.waitingForKeyPress, app.popupMode, app.startLevelPopup, app.endLevelPopup)
    if app.waitingForKeyPress:   
        drawSpashScreen(app, canvas)
    elif app.popupMode:
        drawPopupMode(app, canvas)
    elif app.startLevelPopup:
        drawStartLevelPopup(app, canvas)
    elif app.endLevelPopup:
        drawEndLevelPopup(app, canvas)
    elif app.babyAIpopup:
        drawbabAIpopup(app, canvas)
    elif app.aiEndPopup:
        drawbabAIENDpopup(app, canvas)
    else:
        if app.babyAI and app.aiTurn:
            drawRounds(app, canvas)
            
            redrawAll2(app, canvas)
        else:
            redrawAll1(app, canvas)



#################################################
# main
#################################################

def main():
    playGame()

if __name__ == '__main__':
    main()