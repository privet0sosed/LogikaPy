from typing import Any
import pygame

pygame.init()
winsize = (800, 600)
pygame.mixer.init()

pygame.mixer.music.load("tobi.ogg")
pygame.mixer.music.play()

kick = pygame.mixer.Sound("kick.ogg")

win = pygame.display.set_mode(winsize)
pygame.display.set_caption("Yipe")

bg = pygame.transform.scale(pygame.image.load("bg.png"), winsize)
# plr = pygame.transform.scale(pygame.image.load("plr.png"), (120, 120))
# nemy = pygame.transform.scale(pygame.image.load("sprite.png"), (160, 160))
# tresure = pygame.transform.scale(pygame.image.load("ice.png"), (160, 160))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x=0, y=0, sp=10, sz=(160,160)):
        super().__init__()
        self.sz = sz
        self.speed = sp
        self.image = pygame.transform.scale(pygame.image.load(img), self.sz)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        win.blit(self.image, (self.rect.x-self.sz[0]/2, self.rect.y-self.sz[1]/2))

class Player(GameSprite):
    def Update(self):
        # Movement
        k = pygame.key.get_pressed()
        self.rect.x += (int(k[pygame.K_d])-int(k[pygame.K_a]))*self.speed
        self.rect.y += (int(k[pygame.K_s])-int(k[pygame.K_w]))*self.speed
        self.rect.x, self.rect.y = sM(self.rect.x, self.rect.y)
        self.draw()

class Enemy(GameSprite):
    def Update(self):
        if self.rect.x >= winsize[0]:
            self.speed = -7
        if self.rect.x <= winsize[0]-400:
            self.speed = 7
        self.rect.x += self.speed
        self.draw()


doo = True
clock = pygame.time.Clock()
fps = 60

def sMM(v,m,ma):
    if v>ma:
        return ma
    if v<m:
        return m
    return v

def sM(x,y):
    if x>winsize[0]:
        x=winsize[0]
    if x<0:
        x=0
    if y>winsize[1]:
        y=winsize[1]
    if y<0:
        y=0
    return x, y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size, col):
        super().__init__()
        self.color = col
        self.size = size
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

plr = Player("plr.png", 100, 100, 10, (70,120))
nemy = Enemy("sprite.png", 400, 400, 10, (90, 150))
tresure = GameSprite("ice.png", 300, 300, 10, (70, 70))

walls = []
walls.append(Wall(100, 20, (400, 20), (255,255,255)))

while doo:
    win.blit(bg, (0,0))
    plr.Update()
    nemy.Update()
    tresure.draw()

    for i in walls:
        i.draw()
        if i.rect.colliderect(plr):
            doo = Falsesss

    if nemy.rect.colliderect(plr):
        doo = False

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            doo = False

    pygame.display.update()
    clock.tick(fps)
pygame.quit()