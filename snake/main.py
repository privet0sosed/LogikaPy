def RunGame(cells=14, CELL_SIZE=32, bgimg=None):
    import pygame, time, random, math

    _strttm_ = time.time()
    def tick():
        return time.time() - _strttm_

    def Img(image, size):
        return pygame.transform.scale(pygame.image.load(image), size)

    pygame.init()
    WIDTH, HEIGHT = CELL_SIZE*cells, CELL_SIZE*cells

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Funny Snake Game")
    if bgimg:
        bg = Img("bg.png", (WIDTH*2, HEIGHT))

    clock = pygame.time.Clock()
    FPS = 60

    pygame.font.init()
    pygame.mixer.init()

    eat = pygame.mixer.Sound("eat.mp3")
    win = pygame.mixer.Sound("Chug_Jug_With_You.mp3")
    over = pygame.mixer.Sound("over.mp3")
    fnt = pygame.font.SysFont("Bahnschrift", 24)
    end_fnt = pygame.font.SysFont("Bahnschrift", 48)
    eff_fnt = pygame.font.SysFont("Bahnschrift", 20)
    over2 = end_fnt.render("Game Over :(", True, (255, 100, 100))
    win2 = end_fnt.render("You won!", True, (100, 255, 100))

    mappings = [[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT],
                [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]]
    directions = [(0, -CELL_SIZE), (0, CELL_SIZE), (-CELL_SIZE, 0), (CELL_SIZE, 0)]
    cdir = (0, 0)

    def getrotmove(m):
        if m == directions[1]:
            return 180
        elif m == directions[2]:
            return 90
        elif m == directions[3]:
            return -90
        return 0

    class Snake:
        def __init__(self):
            self.headimg = Img("head.png", (CELL_SIZE, CELL_SIZE))
            self.body = [(((WIDTH // CELL_SIZE)-1)*CELL_SIZE, ((HEIGHT // CELL_SIZE)-1)*CELL_SIZE)]
            self.direction = (0, 0)
            self.grow = False

            self.invincible = 0
            self.slow = 0


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
            if (head in self.body[1:] and snake.invincible <= 0):
                return True
            return False

        def draw(self):
            if self.body[0]:
                screen.blit(pygame.transform.rotate(self.headimg, getrotmove(self.direction)), (self.body[0][0], self.body[0][1]))
            for cube in self.body[1:]:
                pygame.draw.rect(screen, (59, 206, 59), (cube[0], cube[1], CELL_SIZE, CELL_SIZE))

    class Food:
        def __init__(self, Snak, img):
            self.snake = Snak
            self.image = Img(img, (CELL_SIZE, CELL_SIZE))
            self.position = (WIDTH, HEIGHT)

        def respawn(self):
            self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            if len(self.snake.body) >= cells*cells:
                self.hide()
            if self.position in self.snake.body:
                self.respawn()

        def hide(self):
            self.position = (WIDTH, HEIGHT)

        def draw(self):
            screen.blit(self.image, (self.position[0], self.position[1]))

    snake = Snake()
    apple = Food(snake, "epl.png")
    gapple = Food(snake, "gepl.png")
    melon = Food(snake, "melon.png")

    running = True
    stop_reason = None
    frame = 0
    score = 0

    apple.respawn()

    def dobg():
        if bgimg:
            screen.blit(bg, (-(WIDTH/2), 0))
        else:
            screen.fill("black")

    while running:
        frame += 1
        if frame > FPS:
            frame = 1
        dobg()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for map in mappings:
            for reg in map:
                if keys[reg]:
                    t = directions[map.index(reg)]
                    if (snake.direction[0] * -1, snake.direction[1] * -1) != t:
                        cdir = t
                    break
        
        if snake.slow>0:
            if frame%20 == 0:
                snake.change_direction(cdir)
                snake.move()
        elif frame%15 == 0:
            snake.change_direction(cdir)
            snake.move()

        if snake.check_collision():
            running = False
            stop_reason = "lost"

        if len(snake.body) >= cells*cells:
            running = False
            stop_reason = "won"

        if snake.body[0] == apple.position:
            snake.grow = True
            apple.respawn()
            eat.play()
            score += 1
        if snake.body[0] == gapple.position:
            snake.invincible = 15
            gapple.hide()
            eat.play()
        if snake.body[0] == melon.position:
            snake.slow = 20
            melon.hide()
            eat.play()

        for v in [snake, apple, gapple, melon]:
            v.draw()
        
        effcount = 0
        if snake.slow > 0:
            effcount += 1
            tx = eff_fnt.render(f"Slowness: {math.floor(snake.slow)}", True, "white")
            s = tx.get_size()
            screen.blit(tx, (-2+WIDTH-s[0], 2+(effcount-1)*s[1]))
            if frame == 1:
                snake.slow -= 1

        if snake.invincible > 0:
            effcount += 1
            tx = eff_fnt.render(f"Invincibility: {math.floor(snake.invincible)}", True, "white")
            s = tx.get_size()
            screen.blit(tx, (-2+WIDTH-s[0], 2+(effcount-1)*s[1]))
            if frame == 1:
                snake.invincible -= 1

        score_txt = fnt.render(f"Score: {score}", True, "white")
        time_txt = fnt.render(f"Time: {math.floor(tick()/60%60):02}:{math.floor(tick()%60):02}", True, "white")
        screen.blit(time_txt, (10, 34))
        screen.blit(score_txt, (10, 10))

        if melon.position == (WIDTH, HEIGHT) and math.floor(tick()%50) == 0 and score > 7:
            melon.respawn()
        if gapple.position == (WIDTH, HEIGHT) and math.floor(tick()%80) == 0 and score > 14:
            gapple.respawn()

        pygame.display.flip()
        clock.tick(FPS)
    
    if stop_reason == None:
        quit()
    elif stop_reason == "lost":
        dobg()
        over.play()
        osz = over2.get_size()
        screen.blit(over2, ((WIDTH/2)-osz[0]/2, (HEIGHT/2)-osz[1]/2))
        for i in range(4):
            pygame.display.flip()
            time.sleep(1)
        quit()
    elif stop_reason == "won":
        dobg()
        win.play()
        osz = win2.get_size()
        screen.blit(win2, ((WIDTH/2)-osz[0]/2, (HEIGHT/2)-osz[1]/2))
        for i in range(5):
            pygame.display.flip()
            time.sleep(1)
        quit()
debug=False
if debug:
    RunGame()