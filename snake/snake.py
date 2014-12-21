import random

from collections import deque
from L3D import L3D

death_frame = None
cube = None
direction = None
snake = []
treats = []
snake_length = None
speed = None


def setup():
    global cube
    size(700, 700, P3D)
    frameRate(1)
    background(0)

    cube = L3D(this)
    cube.enableDrawing()
    cube.enablePoseCube()
    
    reset_cube()


def add_treat():
    global treats

    while True:
        treat = PVector(random.randint(0, 7), random.randint(0, 7), random.randint(0, 7))
        if treat not in snake:
            treats.append(treat)
            return

def reset_cube():
    global death_frame, direction, snake, snake_length, speed, treats
    cube.background(0)  

    direction = PVector(1, 0, 0)
    snake_length = 5
    snake = deque([PVector(0, 0, 0)])
    speed = 10
    frameRate(speed)

    death_frame = None

    treats = []
    add_treat()


def can_move(direction):
    front = PVector.add(snake[0], direction)
    return front.x >= 0 and front.y >= 0 and front.z >= 0 and front.x <= 7 and front.y <= 7 and front.z <= 7 and front not in snake


def get_next_direction(current_direction):
    # Mostly reuse the same direction but sometimes turn at random
    if can_move(current_direction) and random.random() < 0.8:
        return current_direction

    directions = [
        PVector(1,0,0),
        PVector(-1,0,0),
        PVector(0,1,0),
        PVector(0,-1,0),
        PVector(0,0,1),
        PVector(0,0,-1)
    ]
    directions.remove(current_direction)
    directions = filter(can_move, directions)
    random.shuffle(directions)

    if not directions:
        raise ValueError('No possible moves')

    if not treats:
        return directions[0]

    best_move, distance = None, None
    for direction in directions:
        front = PVector.add(snake[0], direction)
        treat_distance = PVector.dist(front, treats[0])
        if not distance or treat_distance < distance:
            best_move, distance = direction, treat_distance
    
    if best_move:
        return best_move
    else:
        raise ValueError('No possible moves')


def move_snake():
    global death_frame, direction, snake, speed, treats, snake_length

    try:
        direction = get_next_direction(direction)
    except ValueError:
        death_frame = frameCount

    front = PVector.add(snake[0], direction)

    treat_index = None
    try:
        treat_index = treats.index(front)
    except ValueError:
        pass
    else:
        treats.pop(treat_index)
        snake_length += 1
        # Max 60FPS
        speed = min(speed + 1, 60)

    snake.appendleft(front)
    while len(snake) > snake_length:
        snake.pop()

    if treat_index is not None:
        add_treat()


def world_update():
    global death_frame
    frameRate(speed)
    if not death_frame:
        move_snake()
    else:
        if frameCount - death_frame > 100:
            reset_cube()
            death_frame = None

def draw():
    background(0)
    cube.background(0)

    world_update()

    for i, vector in enumerate(snake):
        segment_color = color(255 - (i*255)/snake_length, 0, 0)
        if death_frame and frameCount % 16 < 8:
            segment_color = color(255 - (i*255)/snake_length, 255 - (i*255)/snake_length, 255 - (i*255)/snake_length)

        cube.setVoxel(vector, segment_color)

    if not death_frame:
        for treat in treats:
            cube.setVoxel(treat, color(0, 0, 255))
