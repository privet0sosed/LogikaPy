from pygame import *
from random import randint

init()
mixer.init()
mixer.music.load("10. The Hallow.mp3")
mixer.music.play()
fire_sound = mixer.Sound("pew-roblox.mp3")

font.init()
font1 = font.Font("PressStart2P-Regular.ttf", 48)
font2 = font.Font("PressStart2P-Regular.ttf", 36)
win = font1.render("YOU WIN!", True, "white")
lose = font1.render("YOU LOSE!", True, "crimson")

img_bg = "bg.jpg"
img_hero = "Ship_1.png"
img_bullet = "99133f400f2a4f5.png"
img_enemy = "Ship_3.png"

score = 0
goal = 10
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(img), (size_x, size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        self.rect.x += self.speed * (int(keys[K_RIGHT]) - int(keys[K_LEFT]))

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
bg = transform.scale(image.load(img_bg), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 90, 90, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(bg, (0,0))

        text = font2.render("Рахунок: " + str(score), 1, "white")
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, "white")
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        monsters.update()
        bullets.update()

        colliders = sprite.groupcollide(monsters, bullets, True, True)
        for c in colliders:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        clock.tick(30)

time.delay(50)