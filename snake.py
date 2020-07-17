import pygame, sys, math, random, time


class Snake():
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.dir = ""
        self.list_snake_elements = [(self.x, self.y)]

    def move(self):
        if self.dir == 'left': 
            self.x -= 10
        elif self.dir == 'right': 
            self.x += 10
        elif self.dir == 'up': 
            self.y -= 10
        elif self.dir == 'down': 
            self.y += 10

    def check_edges(self):
        if self.x >= WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH - 10
        if self.y >= HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT - 10

    def check_collide(self):
        if (self.x, self.y) in self.list_snake_elements:  
            self.reset()

    def reset(self):
        global top_score
        if len(self.list_snake_elements)-1 > top_score:
            top_score = len(self.list_snake_elements)-1
        self.list_snake_elements = [(self.x, self.y)]

    def update(self):
        self.move()
        self.check_edges()
        self.check_collide()
        self.list_snake_elements.insert(0, (self.x, self.y))
        if not (food.x == self.x and food.y == self.y):
            del self.list_snake_elements[-1]
        else:
            food.eat = True

        for element in self.list_snake_elements:
            pygame.draw.rect(screen, (255, 255, 255), (*element, 10, 10))



class Food():
    def __init__(self):
        self.x = random.randint(0, WIDTH // 10) * 10
        self.y = random.randint(0, HEIGHT // 10) * 10
        self.eat = False

    def update(self):
        if self.eat:
            sheck_free_positions = []
            for x in range(0, WIDTH, 10):
                for y in range(0, HEIGHT, 10):
                    if (x, y) not in snake.list_snake_elements:
                        sheck_free_positions.append((x, y))
            self.x, self.y = random.choice(sheck_free_positions)
            self.eat = False

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 10, 10))

class Bot():
    def __init__(self):
        self.condition = False

    def work(self):
        dist = self.distance(snake.x, snake.y, food.x, food.y)  

        if (self.distance(snake.x-10, snake.y, food.x, food.y) < dist and
                not (snake.x-10, snake.y) in snake.list_snake_elements):
            snake.dir = 'left'
        if (self.distance(snake.x+10, snake.y, food.x, food.y) < dist and
                not (snake.x+10, snake.y) in snake.list_snake_elements):
            snake.dir = 'right'
        if (self.distance(snake.x, snake.y-10, food.x, food.y) < dist and
                not (snake.x, snake.y-10) in snake.list_snake_elements):
            snake.dir = 'up'
        if (self.distance(snake.x, snake.y+10, food.x, food.y) < dist and 
                not (snake.x, snake.y+10) in snake.list_snake_elements):
            snake.dir = 'down'


        if snake.dir == 'up' and (snake.x, snake.y-10) in snake.list_snake_elements:
            self.turn_on_empty_space()
        if snake.dir == 'down' and (snake.x, snake.y+10) in snake.list_snake_elements:
            self.turn_on_empty_space()
        if snake.dir == 'left' and (snake.x-10, snake.y) in snake.list_snake_elements:
            self.turn_on_empty_space()
        if snake.dir == 'right' and (snake.x+10, snake.y) in snake.list_snake_elements:
            self.turn_on_empty_space()

    def turn_on_empty_space(self):
        if not (snake.x-10, snake.y) in snake.list_snake_elements:
            snake.dir = 'left' 
        if not (snake.x+10, snake.y) in snake.list_snake_elements:
            snake.dir = 'right'
        if not (snake.x, snake.y-10) in snake.list_snake_elements:
            snake.dir = 'up'
        if not (snake.x, snake.y+10) in snake.list_snake_elements:
            snake.dir = 'down'



    def distance(self, x1, y1, x2, y2):
        return math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2)

class Button():
    def __init__(self, text, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = (100, 100, 100)
        self.time = time.time()

    def display(self):
        ''' Display button on the screen '''
        self.check_click()
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        write(self.text, self.x, self.y, 15, (0, 0, 0))


    def check_click(self):
        ''' Check if mouse pressed on button '''
        x, y = pygame.mouse.get_pos()
        if (x > self.x and x < self.x + self.width and
                y > self.y and y < self.y + self.height):
            self.color = (175, 175, 175)
            if time.time() - self.time > 0.5:
                if pygame.mouse.get_pressed()[0] and not bot.condition:
                    bot.condition = True
                    self.time = time.time()
                elif pygame.mouse.get_pressed()[0] and bot.condition:
                    bot.condition = False
                    self.time = time.time()
        else:
            self.color = (255, 255, 255)
        self.color = (0, 200, 0) if bot.condition else (200, 0, 0)

def check_events():
    ''' Check keyboand events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.dir = 'up'
            elif event.key == pygame.K_DOWN:
                snake.dir = 'down'
            elif event.key == pygame.K_LEFT:
                snake.dir = 'left'
            elif event.key == pygame.K_RIGHT:
                snake.dir = 'right'

def write(text, x, y, size, color):
    ''' Write text on the screen '''
    font = pygame.font.SysFont("arial", size)
    temp = font.render(text, True, color)
    screen.blit(temp, (x, y))

pygame.init()

WIDTH = 640
HEIGHT = 480


screen = pygame.display.set_mode([WIDTH+100, HEIGHT])
clock = pygame.time.Clock()

snake = Snake()
food = Food()
bot = Bot()
button = Button('Auto', WIDTH + 20, 100, 50, 20)

top_score = 0


while True:
    screen.fill((0, 0, 0))
    clock.tick(30)

    check_events()

    # right side
    pygame.draw.line(screen, (255, 255, 255), (WIDTH, 0), (WIDTH, HEIGHT))
    write(f'Score: {len(snake.list_snake_elements)-1}', WIDTH + 10, 10, 15, (255, 255, 255))
    write(f'Top score: {top_score}', WIDTH + 10, 30, 15, (255, 255, 255))

    if bot.condition:
        bot.work()

    button.display()

    snake.update()
    food.update()


    pygame.display.flip()