import math, copy, random
from cmu_112_graphics import *

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
        self.vy = 0
    
    def findInitialSpeed(self, power):
        # v = IBO + (L - 30) * 10 - W / 3 + min (0, -(A - 5D)/3)
        # assume that additional weigth on string (W) and draw weight (D) are constant values
        # power is propotional to the draw length 
        # assume that peak draw is a constant 70 lbs
        #power will be from 10- 100 and maxL is 2
        maxL = 50
        L = power/100*maxL
        self.v0 = self.IBO + (L - 30) * 10 - self.addWeight / 3 + min (0, -(Arrow.weight - 5*self.drawWeight)/3)
        print('v0s',self.v0)
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
    app.target2 = Target(3)
    xRange = (app.width-app.margin-30-(app.width-app.margin*2)//6,app.width-app.margin-30)
    yRange = (app.margin+30,app.height-app.margin-30)
    app.target1.generateRandomLocation(xRange, yRange)
    xRange = (app.width-app.margin-30-(app.width-app.margin*2)//6,app.width-app.margin-30)
    yRange = (app.margin+30+app.height//2,app.height-app.margin-30)
    app.target2.generateRandomLocation(xRange, yRange)
    app.arrowPresent = False
    app.timerDelay = 50
    app.timer = 0
    app.peakx = 0
    app.peaky = 0
    app.totalTime = 0
    app.trajectoryCirlces = []
    app.drawEnd = False
    app.ypos = 0
    app.level = 1
    app.score = 0
    app.babyAI = True
    app.waitingForKeyPress = True
    app.playerAngle = math.pi/4
    app.incrementAngle = math.pi/32

def trajectoryPeak(app):
    v0 = app.arrow.findInitialSpeed(70)
    v0y = v0*math.sin(app.arrow.angle)
    vfy = 0
    a = -9.8

    #Vf^2 = Vi^2 + 2ay
    #distance y = (Vf^2 - Vi^2)/2a
    dy = -(v0y**2)/(2*a)

    #time
    t = v0y-(math.sqrt((v0y**2)-(a*0.5)))/9.8

    #distance x
    v0x = v0*math.cos(app.arrow.angle)
    dx = v0x*t
    
    print(app.arrow.x, app.arrow.y)
    peaky = app.arrow.y - dy
    peakx = app.arrow.x + dx 
    print('dy', dy)
    print(peakx, peaky, t)
    app.totalTime = t
    return (peaky, peakx, t)



def trajectoryEnd(app):
    dy = (app.height-app.margin)-app.peaky
    v0y = 0
    a = 9.8
    vfy = (v0y**2 + 2*a*dy)**(1/2)
    #time
    t = (vfy-v0y)/a
    print('vfy', vfy)
    print('v0y',v0y)
    print('dy', dy)
    print('t', t)
    #distance x
    v0x = vfx = app.arrow.v0*math.cos(app.arrow.angle)
    dx = (v0x+vfx)/2*t
    print(app.arrow.x, app.arrow.y)
    app.arrow.y += dy 
    app.arrow.x += dx
    print(app.arrow.x, app.arrow.y)
    app.drawEnd = True

def findTrajectoryPeak(app):
    v0 = app.arrow.findInitialSpeed(50)
    v0y = v0*math.sin(app.arrow.angle)
    vfy = 0
    a = -9.8
    #distance y
    dy = -(v0y**2)/(2*a)
    #time
    t = (vfy-v0y)/a
    #distance x
    v0x = v0*math.cos(app.arrow.angle)
    dx = v0x*t
    print(app.arrow.x, app.arrow.y)
    peaky = app.arrow.y - dy
    peakx = app.arrow.x + dx 
    print('dy', dy)
    print(peakx, peaky, t)
    app.totalTime = t
    return (peaky, peakx, t)


def findTrajectoryEnd(app):
    dy = (app.height-app.margin)-app.peaky
    v0y = 0
    a = 9.8
    vfy = (v0y**2 + 2*a*dy)**(1/2)
    #time
    t = (vfy-v0y)/a
    print('vfy', vfy)
    print('v0y',v0y)
    print('dy', dy)
    print('t', t)
    #distance x
    v0x = vfx = app.arrow.v0*math.cos(app.arrow.angle)
    dx = (v0x+vfx)/2*t
    print(app.arrow.x, app.arrow.y)
    app.arrow.y += dy 
    app.arrow.x += dx
    print(app.arrow.x, app.arrow.y)
    app.drawEnd = True

def timerFired(app):
    if app.arrowPresent:
        
        app.timer += app.timerDelay
        # if app.ypos == 1:
        #     app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
        #     updateArrowPositionPositiveY(app)
        # elif app.ypos == 2:
        #     app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
        #     updateArrowPositionNegativeY(app)

        if app.ypos == 1:
            app.trajectoryCirlces.append((app.arrow.x, app.arrow.y))
            updateArrowPostion(app)

def updateArrowPostion(app): 
    a=9.81
    velocity = app.arrow.v0
    angle = app.arrow.angle
    vx=velocity * math.cos(angle)
    vy=velocity * math.sin(angle)
    t=app.timer/1000
    x = app.startPostion[0]
    y = app.startPostion[1]

    dx = x+vx*t
    dy = y-(vy*t - (a/2)*t*t)

    app.arrow.x = dx
    app.arrow.y = dy

    if dy > y:
        print("HEHEEELELELELELELEE")
        app.ypos = 0


def updateArrowPositionPositiveY(app):
    a = -9.8
    t = app.timerDelay/1000
    v0x = app.arrow.v0*math.cos(app.arrow.angle)
    dx = v0x*t
    v0y = app.arrow.v0*math.sin(app.arrow.angle)
    dy = v0y*t+(1/2)*a*(t)**2
    app.arrow.vy = v0y +a*t
    app.arrow.x += dx
    app.arrow.y -= dy
    print('x',app.arrow.x, 'dx', dx, 'y', app.arrow.y, 't', t)
    if app.arrow.y <= app.peaky:
        print(app.arrow.y, app.arrow.x, app.timer/1000)
        app.ypos = 2


def updateArrowPositionNegativeY(app):
    a = 9.8
    t = app.timerDelay/1000
    v0x = app.arrow.v0*math.cos(app.arrow.angle)
    dx = v0x*t
    v0y = app.arrow.v0*math.sin(app.arrow.angle)
    dy = v0y*t+(1/2)*a*(t)**2
    app.arrow.vy = v0y+a*t
    app.arrow.x += dx
    app.arrow.y += dy
    print('x',app.arrow.x, 'dx', dx, 'y', app.arrow.y, 't', t)
    if app.arrow.y >= app.height-app.margin:
        print(app.timer/1000)
        app.ypos = 0

def keyPressed(app, event):
    if event.key == 's':
        app.arrowPresent = True
        app.ypos = 1
        app.peaky, app.peakx, app.totalTime = trajectoryPeak(app)
    if event.key == 'e':
        trajectoryEnd(app)
    if event.key == 'Up' :
        updateArrowAngle(app, 'Up')
    if event.key == 'Down':
        updateArrowAngle(app, 'Down')
    if event.key == '1':
        app.level = 1
    if event.key == '2':
        app.level = 2
    if event.key == '3':
        app.level = 3
    if event.key == 'a':
        app.babyAI = True

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
    print(app.playerAngle)

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

def drawTarget2(app, canvas):
    x0 = app.target2.x-30
    y0 =  app.target2.y-app.target2.rings*30
    x1 =  app.target2.x+30
    y1 =  app.target2.y+app.target2.rings*30
    canvas.create_oval(x0, y0, x1, y1, fill='blue')

    x0 = app.target2.x-20
    y0 =  app.target2.y-app.target2.rings*20
    x1 =  app.target2.x+20
    y1 =  app.target2.y+app.target2.rings*20
    canvas.create_oval(x0, y0, x1, y1, fill='green')

    x0 = app.target2.x-5
    y0 =  app.target2.y-app.target2.rings*5
    x1 =  app.target2.x+5
    y1 =  app.target2.y+app.target2.rings*5
    canvas.create_oval(x0, y0, x1, y1, fill='red')

def drawArrow(app, canvas):
    vy = app.arrow.vy
    vx = app.arrow.v0*math.cos(app.arrow.angle)
    arrowAngle = math.atan(vy/vx)
    angle = app.playerAngle
    arrowL = 30
    x0 = app.arrow.x+arrowL*math.cos(math.pi-arrowAngle)
    y0 = app.arrow.y+arrowL*math.sin(math.pi-arrowAngle)
    x1 = app.arrow.x+arrowL*math.cos(arrowAngle)
    y1 = app.arrow.y-arrowL*math.sin(arrowAngle)
    canvas.create_line(x0,y0,x1,y1)

def drawTrajectory(app, canvas):
    for x,y in app.trajectoryCirlces:
        canvas.create_oval(x-10, y-10, x+10, y+10, fill = 'black')

def drawAngle(app, canvas):
    angle = app.playerAngle
    arrowL = 30
    x0 = app.startPostion[0]
    y0 = app.startPostion[1]
    x1 = arrowL*math.cos(angle)+x0
    y1 = y0-arrowL*math.sin(angle)
    canvas.create_line(x0,y0,x1,y1)

def redrawAll(app, canvas):
    x0 = app.startPostion[0]-10
    y0 = app.startPostion[1]-10
    x1 = app.startPostion[0]+10
    y1 = app.startPostion[1]+10
    canvas.create_oval(x0, y0, x1, y1, fill='green')

    drawTarget1(app, canvas)
    drawTarget2(app, canvas)
    drawAngle(app, canvas)
    if app.arrowPresent: 
        drawArrow(app, canvas)
        drawTrajectory(app, canvas)
        canvas.create_oval(app.peakx-10, app.peaky-10, app.peakx+10, app.peaky+10, fill = 'red')
    if app.drawEnd:
        canvas.create_oval(app.arrow.x-10, app.arrow.y-10, app.arrow.x+10, app.arrow.y+10, fill = 'red')

#################################################
# main
#################################################

def main():
    playGame()

if __name__ == '__main__':
    main()