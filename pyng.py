#!/usr/bin/python2.7

## 
## Pyng - Another Pong written in python2.7.
## Author: Hyd3L
##

import pygame, sys, os
from pygame.locals import * # required for QUIT constant

# CURSOR_UP_ONE = '\x1b[1A'
# ERASE_LINE = '\x1b[2K'

## GAME WINDOW
WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 555
WINDOW_SIZE   = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_FPS    = 400

## SOUNDS
## Sounds use "beep" command for Linux to emit a sound
## when the ball hit the paddle or falls behind it.
## If you don't have "beep", install it on your system
## in order to hear sounds. Otherwise disable this feature
## or program will crash because of this missing command.
SOUND_ENABLED = False
## TODO: Add .wav sounds and play them with pygame.mixer
##       to have full compatibility with other OS.

## MIDLINE PARAMETERS
MID_LINE = ((WINDOW_WIDTH/2,0),(1,WINDOW_HEIGHT))

## PADDLE PARAMETERS
PADDLE_WIDTH  = WINDOW_WIDTH/60
PADDLE_HEIGHT = WINDOW_HEIGHT/6
PADDLE_OFFSET = WINDOW_WIDTH/30
PADDLE_SPRITE = (PADDLE_WIDTH, PADDLE_HEIGHT)
PADDLE_ONE_X  = PADDLE_OFFSET - PADDLE_WIDTH/2
PADDLE_TWO_X  = WINDOW_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH/2
PADDLE_INIT_Y = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
PADDLE_SPEED  =  600/WINDOW_FPS #Questo rende la velocità delle racchette costante anche cambiando gli fps

## BALL PARAMETERS
BALL_SIZE   = WINDOW_WIDTH/70
BALL_SPRITE = (BALL_SIZE, BALL_SIZE)
BALL_INIT_X = (WINDOW_WIDTH/2)-BALL_SIZE/2
BALL_INIT_Y = (WINDOW_HEIGHT/2)-BALL_SIZE/2
BALL_COUNTDOWN = WINDOW_FPS
BALL_GUM_ENABLED = True ## Ball speed increases if hit
BALL_MAX_SPEED = 10

## COLORS
COLOR_BLACK = (000,000,000)
COLOR_WHITE = (255,255,255)

## SCORE
MAX_SCORE = 11

class Window:
  def __init__(self):
    global SURFACE
    global FPS_CLOCK
    self.surface = pygame.display.set_mode(WINDOW_SIZE)
    self.fps = WINDOW_FPS
    self.clock = pygame.time.Clock()
    SURFACE = self.surface
    FPS_CLOCK = self.clock
    pygame.display.set_caption("Pyng")
  def update(self):
    FPS_CLOCK = self.clock.tick(self.fps)
    pygame.display.update()
    SURFACE.fill(COLOR_BLACK)

class Line:
  def draw(self):
    pygame.draw.rect(SURFACE, COLOR_WHITE, MID_LINE, 1)

class Paddle:
  def __init__(self, player):
    self.player = player
    self.y = PADDLE_INIT_Y
    self.speed = PADDLE_SPEED
    self.score = 0
    self.font = pygame.font.Font("fixedsys.ttf",24)
  ## Draw paddles and score indicators
  def draw(self):
    if self.player == 0:
      pygame.draw.rect(SURFACE,COLOR_WHITE,((PADDLE_ONE_X,self.y),PADDLE_SPRITE),0)
      scoreBlit = self.font.render(str(self.score), 1, COLOR_WHITE)
      SURFACE.blit(scoreBlit,(WINDOW_WIDTH/2.5, PADDLE_OFFSET))
    elif self.player == 1:
      pygame.draw.rect(SURFACE,COLOR_WHITE,((PADDLE_TWO_X,self.y),PADDLE_SPRITE),0)
      scoreBlit = self.font.render(str(self.score), 1, COLOR_WHITE)
      SURFACE.blit(scoreBlit,(WINDOW_WIDTH - WINDOW_WIDTH/2.4, PADDLE_OFFSET))
  ## Get paddle Y position
  def getY(self):
    return self.y
  ## Get player score
  def getScore(self):
    return self.score
  ## Increase player score.
  def incScore(self):
    self.score += 1
    return self.getScore()
  def move(self):
    keys = pygame.key.get_pressed()
    if self.player == 0: ## First player moves with W and S
      if keys[pygame.K_w]:
        self.y -= self.speed
      if keys[pygame.K_s]:
        self.y += self.speed
    if self.player == 1: ## Second player moves with UP and DOWN
      if keys[pygame.K_UP]:
        self.y -= self.speed
      if keys[pygame.K_DOWN]:
        self.y += self.speed
    self.collision()
  def collision(self):
    if self.y <= 0: ## Prevent paddle moving too high or too low
      self.y = 0
    elif self.y >= WINDOW_HEIGHT-PADDLE_HEIGHT:
      self.y = WINDOW_HEIGHT-PADDLE_HEIGHT

class Ball:
  def __init__(self):
    self.x = BALL_INIT_X
    self.y = BALL_INIT_Y
    self.dirX = -1
    self.dirY = 1
    ## A little pause before launching the ball
    self.start = True
    self.counter = BALL_COUNTDOWN 
  def draw(self):
    pygame.draw.rect(SURFACE,COLOR_WHITE,((self.x,self.y),BALL_SPRITE),0)
  def getPos(self):
    return (self.x, self.y)
  def move(self):
    if self.start == True:
      self.counter -= 1
      if self.counter == 0:
        self.start = False
    else:
      self.x += self.dirX
      self.y += self.dirY
      # sys.stdout.write(CURSOR_UP_ONE)
      # sys.stdout.write(ERASE_LINE)
      # print "Ball: x:", self.x, "y:",self.y
      self.collision()
  def reset(self, player):
    if SOUND_ENABLED:
      os.system("beep -f 100 -l 30")
    self.x = BALL_INIT_X
    self.y = BALL_INIT_Y
    self.start = True
    self.counter = BALL_COUNTDOWN
    # sys.stdout.write(CURSOR_UP_ONE)
    # sys.stdout.write(ERASE_LINE)
    # print "Ball: x:", self.x, "y:",self.y
    if player == 0:
      self.dirX = -1
    else:
      self.dirX = 1
  def collision(self):
    # TOP and BOTTOM collision
    if self.y >= WINDOW_HEIGHT-BALL_SIZE or self.y <= 0:
      self.dirY *= -1
    # LEFT and RIGHT collision
    #if self.x <= 0 or self.x >= WINDOW_WIDTH-BALL_SIZE:
    #  self.dirX *= -1
    # Left pad collision
    if self.x <= PADDLE_OFFSET+PADDLE_WIDTH:
      Y1 = pong.playerOne.getY()
      ## UPCOL and DWCOL are two conditions that check weather
      ## the collision point is in the bottom side of the ball
      ## This prevent the bounce to be ignored whenever you hit the
      ## ball on its bottom side.
      UPCOLA = (self.y >= Y1 and self.y <= Y1+PADDLE_HEIGHT)
      DWCOLA = (self.y+BALL_SIZE >= Y1 and self.y+BALL_SIZE <= Y1+PADDLE_HEIGHT)
      if UPCOLA or DWCOLA:
        if SOUND_ENABLED:
          os.system("beep -f 1000 -l 30")
        if BALL_GUM_ENABLED:
          self.dirX *= -1.1
          ## MAX BALL SPEED
          if self.dirX > BALL_MAX_SPEED:
            self.dirX = BALL_MAX_SPEED
          if self.dirX < -BALL_MAX_SPEED:
            self.dirX = -BALL_MAX_SPEED
        else: self.dirX *= -1
      elif pong.playerTwo.incScore() == MAX_SCORE: ## Check if playerTwo won
        print "Player 2 wins"
        pygame.quit()
        sys.exit()
      else: self.reset(0)
    # Right pad collision
    if self.x >= WINDOW_WIDTH-PADDLE_OFFSET-PADDLE_WIDTH-BALL_SIZE:
      Y2 = pong.playerTwo.getY()
      UPCOLB = (self.y >= Y2 and self.y <= Y2+PADDLE_HEIGHT)
      DWCOLB = (self.y+BALL_SIZE >= Y2 and self.y+BALL_SIZE <= Y2+PADDLE_HEIGHT)
      if UPCOLB or DWCOLB:
        if SOUND_ENABLED:
          os.system("beep -f 500 -l 30")
        if BALL_GUM_ENABLED:
          self.dirX *= -1.1
          ## MAX BALL SPEED
          if self.dirX > BALL_MAX_SPEED:
            self.dirX = BALL_MAX_SPEED
          if self.dirX < -BALL_MAX_SPEED:
            self.dirX = -BALL_MAX_SPEED
        else: self.dirX *= -1
      elif pong.playerOne.incScore() == MAX_SCORE: ## Check if playerOne won
          print "Player 1 wins"
          pygame.quit()
          sys.exit()
      else: self.reset(1)

class Game:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(0) ## Hide mouse pointer
    pygame.mixer.init() ## Initialize SDL2 sound mixer
    self.window = Window()
    self.line = Line()
    self.playerOne = Paddle(0)
    self.playerTwo = Paddle(1)
    self.ball = Ball()
  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          print "Pyng: got quit signal by user."
          pygame.quit()
          sys.exit()
      self.window.update()
      self.line.draw()
      self.playerOne.draw()
      self.playerTwo.draw()
      self.playerOne.move()
      self.playerTwo.move()
      self.ball.move()
      self.ball.draw()

pong = Game()
pong.run()
