from pygame import *
from time import sleep
import random

init()
CELL_SIZE = 32
cells = 24
WIDTH, HEIGHT = CELL_SIZE*cells, CELL_SIZE*cells

GREEN = (0, 255, 0)

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Snake Game")
bg = transform.scale(image.load("bg.png"), (WIDTH*2, HEIGHT))

clock = time.Clock()
FPS = 60

font.init()
mixer.init()

eat = mixer.Sound("eat.mp3")
over = mixer.Sound("over.mp3")
fnt = font.SysFont("Bahnschrift", 16)
over2 = font.SysFont("Bahnschrift", 48).render("Game Over :(", True, (255, 100, 100))

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        self.body.insert(0, new_head)

    def change_direction(self, direction):
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.direction = direction

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

    def draw(self):
        for cube in self.body:
            draw.rect(screen, GREEN, (cube[0], cube[1], CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.image = transform.scale(image.load("epl.png"), (CELL_SIZE, CELL_SIZE))
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def respawn(self):
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def draw(self):
        screen.blit(self.image, (self.position[0], self.position[1]))

# Initialize game objects
snake = Snake()
food = Food()

# Game loop
running = True
frame = 0
score = 0

Keyss = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
Corr = [(0, -CELL_SIZE), (0, CELL_SIZE), (-CELL_SIZE, 0), (CELL_SIZE, 0)]

while running:
    frame += 1
    if frame > 30:
        frame = 1
    #screen.blit(bg, (-WIDTH/3,0))
    screen.fill("black")

    for evnt in event.get():
        if evnt.type == QUIT:
            running = False

    # Handle input
    keys = key.get_pressed()
    for i in Keyss:
        if keys[i]:
            cor = Corr[Keyss.index(i)]
            snake.change_direction(cor)
            break

    # Update game objects
    if frame%11 == 5:
        snake.move()
        ch = False

    # Check for collisions
    if snake.check_collision():
        running = False

    # Check if snake eats the food
    if snake.body[0] == food.position:
        snake.grow = True
        food.respawn()
        eat.play()
        score += 1

    # Draw everything
    snake.draw()
    food.draw()

    score_txt = fnt.render("Score: "+str(score), True, "white")
    screen.blit(score_txt, (10, 10))

    display.flip()
    clock.tick(FPS)

over.play()

for _ in range(1, 4):
    over_rect = over2.get_rect()
    display.flip()
    screen.blit(over2, ((WIDTH/3)-(over_rect.x/2), (HEIGHT/2)-(over_rect.y/2)))
    sleep(.5)
    display.flip()
    sleep(.5)

sleep(3)
quit()