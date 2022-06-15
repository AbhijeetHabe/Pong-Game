import pygame
pygame.init()

# Variables
WIDTH = 1200
HEIGHT = 600
BORDER = 20
RADIUS = 10
VELOCITY = 1
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
FPS = 60
pygame.display.set_caption("Pong")
fgColor = pygame.Color("white")
bgColor = pygame.Color("black")
screen = pygame.display.set_mode((WIDTH,HEIGHT))
SCORE_FONT = pygame.font.SysFont('comicsans', 50)

# Define my class

class Paddle:
    VEL = 4
    COLOR = fgColor

    def __init__(self, x, y , width, height):
        self.x = self.original_x = x 
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, color):
        global screen
        pygame.draw.rect(screen, fgColor, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 5
    
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.velx = self.MAX_VEL
        self.vely = 0

    def show(self, color):
        global screen
        pygame.draw.circle(screen, fgColor, (self.x, self.y), self.radius)
    
    def update(self):
        global bgColor, fgColor
        
        self.x += self.velx
        self.y += self.vely

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.vely = 0
        self.velx *= -1

def draw(screen, paddles, ball, left_score, right_score):
    screen.fill(bgColor)
    left_score_text = SCORE_FONT.render(f'{left_score}',1, fgColor)
    right_score_text = SCORE_FONT.render(f'{right_score}',1, fgColor)
    screen.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    screen.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))


    for paddle in paddles:
        paddle.draw(screen)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i%2 == 1:
            continue
        pygame.draw.rect(screen, fgColor, (WIDTH//2 - 5,i, 10, HEIGHT//20))

    ball.show(screen)

    pygame.display.update()


# Draw the scenerio
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.vely *= -1
    elif ball.y - ball.radius <= 0:
        ball.vely *= -1

    if ball.velx < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.velx *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2) / ball.MAX_VEL
                vely = difference_in_y/ reduction_factor
                ball.vely = -1*vely 

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.velx *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2) / ball.MAX_VEL
                vely = difference_in_y/ reduction_factor
                ball.vely = -1*vely 

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH -10- PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, RADIUS)
    left_score = 0
    right_score = 0
    WINNING_SCORE = 10
    while run:
        draw(screen, [left_paddle, right_paddle], ball, left_score, right_score)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.update()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score +=1
            ball.reset()
        elif ball.x > WIDTH:
            left_score +=1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!!"

        if won:
            text = SCORE_FONT.render(win_text, 1, fgColor)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0 

    pygame.quit()

if __name__ == '__main__':
    main()