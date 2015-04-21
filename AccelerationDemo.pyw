# AccelerationDemo.pyw
# by Kurt D kurtd5105@gmail.com
# Description: A pygame demo of a cube that moves around the window, accelerating
#              if there is user input with the arrow keys. If there is no user
#              input and it is in motion, it will decelerate.
import pygame, sys
from pygame.locals import *
from math import sqrt

# Colour Setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GOLD  = (255, 215, 0)
GREY_DARK  = (128, 128, 128)
GREY_LIGHT = (192, 192, 192)

# Constants Setup
FPS = 60

# Player
# Description: Player class that contains all of the player's movement
#              variables as well as the sprite. Contains all methods required
#              to draw and translate the sprite on screen.
class Player:
    def __init__(self, WINDOW, SPRITE, vector, accelConsts):
        self.WINDOW = WINDOW
        self.vector = vector
        # Image gets loaded
        self.SPRITE = pygame.image.load(SPRITE)
        self.xVel, self.yVel, self.xAccel, self.yAccel = 0, 0, 0, 0
        self.accelAmount, self.decelAmount = accelConsts[0], accelConsts[1]
        self.draw()
        
    def draw(self):
        self.WINDOW.blit(self.SPRITE, self.vector)
        
    def move(self):
        self.vector[0] += self.xVel
        self.vector[1] += self.yVel
        
    def translate(self, newVector):
        self.vector = newVector

    
    def changeAccel(self, newAccel):
        self.xAccel += newAccel[0]
        self.yAccel += newAccel[1]

    # updateVel
    # Description: Update the velocity based on the acceleration
    def updateVel(self):
        if self.xAccel >= 0:
            self.xVel = sqrt(self.xAccel)
        else:
            self.xVel = -sqrt(-self.xAccel)
        if self.yAccel >= 0:
            self.yVel = sqrt(self.yAccel)
        else:
            self.yVel = -sqrt(-self.yAccel)

    # returnToBounds
    # Description: returns the player onto the screen if the player leaves it.
    # NOTE: Pygame bounding only works for x >= 0 and y >= 0, so edge scrolling when
    #       player is not in those bounds does not work properly. Player will not
    #       be drawn on screen until its x >= 0 and y >= 0.
    def returnToBounds(self):
        rightBound = 800
        bottomBound = 600
        leftBound, upBound = 0, 0
        # Player off x bounds
        # Out of right side
        if self.vector[0] > rightBound:
            # Move the player back around to the left side
            self.vector[0] = self.vector[0] - rightBound
        # Out of left side
        elif self.vector[0] < leftBound:
            # Move the player back around to the right side
            self.vector[0] = -self.vector[0] + rightBound
            
        # Player off y bounds
        # Out of bottom side
        if self.vector[1] > bottomBound:
            # Move the player back around to the top side
            self.vector[1] = bottomBound - self.vector[1]
        # Out of top size
        elif self.vector[1] < upBound:
            # Move the player back around to the bottom side
            self.vector[1] = -self.vector[1] + bottomBound

    def accelChangeVector(self, accelDir, amount):
        if accelDir == 'x':
            return [amount, 0]
        return [0, amount]

    # updateAcceleration
    # Description: Updates the player's acceleration in a given direction based
    #              on whether or not there was user input. If there was user
    #              input, the player will accelerate. Otherwise the player will
    #              decelerate.
    def updateAcceleration(self, moveArray, accelDir):
        # Setup the +dir and -dir values
        if accelDir == 'x':
            accel = self.xAccel
            indexes = [0, 1]
        else:
            accel = self.yAccel
            indexes = [2, 3]

        # Start by changing acceleration based on user input or slowing down
        # Acceleration change for +dir (indexes[0]) and -dir (indexes[1])
        if moveArray[indexes[0]] == 1:
            self.changeAccel(self.accelChangeVector(accelDir, -self.accelAmount))
        elif moveArray[indexes[1]] == 1:
            self.changeAccel(self.accelChangeVector(accelDir, self.accelAmount))
        # Deceleration as no key was pressed
        else:
            if accel > 0:
                # Check to see which value will get closer to 0 without going over
                if self.decelAmount > accel:
                    self.changeAccel(self.accelChangeVector(accelDir, -accel))
                else:
                    self.changeAccel(self.accelChangeVector(accelDir, -self.decelAmount))
            elif accel < 0:
                if self.decelAmount < accel:
                    self.changeAccel(self.accelChangeVector(accelDir, -accel))
                else:
                    self.changeAccel(self.accelChangeVector(accelDir, self.decelAmount))

    # moveStep
    # Description: Corrects the player's position to be on screen, and then
    #              changes the acceleration based on the user input. After
    #              it changes the velocity based on the acceleration and 
    #              then the position based on the velocity.
    def moveStep(self, moveArray):
        self.returnToBounds()
        self.updateAcceleration(moveArray, 'x')
        self.updateAcceleration(moveArray, 'y')
        self.updateVel()
        self.move()

class AccelerationDemo:
    def __init__(self):
        # left, right, up, down
        self.moveArray = [0, 0, 0, 0]
        # Game Launch
        pygame.init()
        pygame.display.set_caption("Acceleration Demo")

        self.fpsClock = pygame.time.Clock()

        self.WINDOW = pygame.display.set_mode((800, 600))
        
        self.WINDOW.fill(GREY_DARK)
        # Player creation at 400, 300; acceleration at a rate of 1 and deceleraton at 0.5
        self.player = Player(self.WINDOW, "player.png", [400,300], [1, 0.5])
        pygame.display.update()

        self.mainLoop()

    def mainLoop(self):
        while True:
            # Detect input
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # Change the appropriate moveArray variable to show input happened
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.moveArray[0] = 1
                    elif event.key == K_RIGHT:
                        self.moveArray[1] = 1
                    elif event.key == K_UP:
                        self.moveArray[2] = 1
                    elif event.key == K_DOWN:
                        self.moveArray[3] = 1
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.moveArray[0] = 0
                    elif event.key == K_RIGHT:
                        self.moveArray[1] = 0
                    elif event.key == K_UP:
                        self.moveArray[2] = 0
                    elif event.key == K_DOWN:
                        self.moveArray[3] = 0
            # Process game based on this input
            self.player.moveStep(self.moveArray)
            # Draw the updated player
            self.WINDOW.fill(GREY_DARK)#Comment out this to add a trail effect!
            self.player.draw()
            pygame.display.update()
            self.fpsClock.tick(FPS)


if __name__ == '__main__':
    app = AccelerationDemo()
