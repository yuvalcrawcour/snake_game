import pygame, sys
from pygame import Vector2
import random

BLOCK_SIZE = 20


# class fruit represent the fruits in the game.
# each fruit has its location as a vector and its image
class Fruit:
    # for initialization each fruit is being placed randomly
    def __init__(self):
        pos_x = random.randint(0, 19)
        pos_y = random.randint(0, 24)
        self.pos = Vector2(pos_x, pos_y)
        self.apple_image = pygame.image.load("Graphics/apple1.jpg").convert_alpha()
        self.apple_image = pygame.transform.scale(self.apple_image, (20, 20))

    # draw fruit method, responsible for drawing the fruit according to its location
    def draw_fruit(self):
        pos_x = int(self.pos.x * BLOCK_SIZE)
        pos_y = int(self.pos.y * BLOCK_SIZE)
        fruit_rect = pygame.Rect(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
        screen.blit(self.apple_image, fruit_rect)

    # if the snake eats that fruit we initialize the fruit, which will randomize its new location
    def was_eaten(self):
        self.__init__()


# each snake is made of snake nodes that are connected to each other with references like a linked list.
class SnakeNode:
    def __init__(self, x=0, y=0):
        self.pos = Vector2(x, y)
        self.next = None
        self.prev = None
# the game board is actually a grid of blocks with the size BLOCK_SIZE
# so the position to draw the node is the number of row and column in the grid * BLOCK_SIZE
    def draw_node(self):
        pos_x = int(self.pos.x * BLOCK_SIZE)
        pos_y = int(self.pos.y * BLOCK_SIZE)
        node_rect = pygame.Rect(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, (70, 125, 125), node_rect)


# in the snake class we have references to the head of the snake and to the tail
# movement direction of the snake is represented as a vector 2D
class Snake:
    def __init__(self, head_x, head_y):
        self.head = SnakeNode(head_x, head_y)
        self.tail = self.head
        self.direction = Vector2(1, 0)
        self.update_eat = False
        head_image = pygame.image.load("Graphics/head.jpg").convert_alpha()
        self.head_image_down = pygame.transform.scale(head_image, (20, 20))
        self.head_image_right = pygame.transform.rotate(self.head_image_down, 90)
        self.head_image_up = pygame.transform.rotate(self.head_image_down, 180)
        self.head_image_left = pygame.transform.rotate(self.head_image_down, 270)

    def set_direction(self, vec):
        self.direction = vec

    def eat(self):
        self.update_eat = True

    def add(self, node):
        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    # each movement requires running with a while loop over the snake from the head to the tail
    # moving each node to the position where the previous node was and moving the head forward
    def move(self):
        if (self.update_eat == True):
            new_tail = SnakeNode(self.tail.pos.x, self.tail.pos.y)
            self.add(new_tail)
        cur = self.tail
        while not (cur == self.head):
            cur.pos.x = cur.prev.pos.x
            cur.pos.y = cur.prev.pos.y
            cur = cur.prev
        self.head.pos += self.direction
        self.update_eat = False

# basically, drawing the snake means running over the linked list of nodes and drawing each one of them
# the complicated part is to draw the picture of the head facing the right direction
    def draw_snake(self):
        pos_x = int(self.head.pos.x * BLOCK_SIZE)
        pos_y = int(self.head.pos.y * BLOCK_SIZE)
        head_rect = pygame.Rect(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
        if self.direction == Vector2(1, 0):
            screen.blit(self.head_image_right, head_rect)
        elif self.direction == Vector2(-1, 0):
            screen.blit(self.head_image_left, head_rect)
        elif self.direction == Vector2(0, 1):
            screen.blit(self.head_image_down, head_rect)
        else:
            screen.blit(self.head_image_up, head_rect)

        cur = self.head.next
        while not (cur == None):
            cur.draw_node()
            cur = cur.next

# method to check if the head intersects with one of the nodes of the body of the snake
    def check_if_intersects(self):
        cur = self.head.next
        while not (cur == None):
            if self.head.pos == cur.pos:
                return True
            cur = cur.next
        return False

# method to check if the snake is going out of the screen
    def check_out_of_screen(self):
        if self.head.pos.x == 0 or self.head.pos.x >= 20:
            return True
        if self.head.pos.y == 0 or self.head.pos.y >= 25:
            return True

# method to draw the grass, one square dark followed by one lighter, and so on
def draw_grass():
    for x in range(0, 20):
        for y in range(0, 25):
            pos_x = int(x * BLOCK_SIZE)
            pos_y = int(y * BLOCK_SIZE)
            grass_rect = pygame.Rect(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
            if (x * y % 2 == 0):
                pygame.draw.rect(screen, (150, 215, 70), grass_rect)
            else:
                pygame.draw.rect(screen, (142, 200, 77), grass_rect)


pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()

# initializing all the game components
def init_game():
    global nahash
    global fruits
    nahash = Snake(5, 5)
    nahash.add(SnakeNode(5, 6))
    nahash.add(SnakeNode(5, 7))
    nahash.add(SnakeNode(5, 8))
    fruits = [Fruit(), Fruit(), Fruit()]
    global score
    score = 0


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
init_game()
run = True


def print_score():
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    text = "score: " + str(score)
    textsurface = myfont.render(text, False, (0, 0, 0))
    screen.blit(textsurface, (0, 0))

# the main loop of the game
# here we draw everything on the screen and react to events that the user make
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # user pressing an arrow button changes the direction in which the snake move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not (nahash.direction == Vector2(0, 1)):
                nahash.set_direction(Vector2(0, -1))
            if event.key == pygame.K_DOWN and not (nahash.direction == Vector2(0, -1)):
                nahash.set_direction(Vector2(0, 1))
            if event.key == pygame.K_LEFT and not (nahash.direction == Vector2(1, 0)):
                nahash.set_direction(Vector2(-1, 0))
            if event.key == pygame.K_RIGHT and not (nahash.direction == Vector2(-1, 0)):
                nahash.set_direction(Vector2(1, 0))

        if event.type == SCREEN_UPDATE:
            nahash.move()

        # if the snake is out of the window or intersecting itself the game stops and restarts
        if nahash.check_if_intersects() or nahash.check_out_of_screen():
            nahash.draw_snake()
            for pri in fruits:
                pri.draw_fruit()
            print_score()
            pygame.display.update()
            pygame.time.wait(1500)
            init_game()

# the snake going over a fruit resulting the snake to grow and the fruit to be reinitialized
        for pri in fruits:
            if nahash.head.pos == pri.pos:
                pri.was_eaten()
                nahash.eat()
                score += 1

    draw_grass()
    for pri in fruits:
        pri.draw_fruit()
    nahash.draw_snake()

    pygame.display.update()
    clock.tick(60)


def main():
    pass



if __name__ == '__main__':
    main()


