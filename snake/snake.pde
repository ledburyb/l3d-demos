import java.util.Collections;
import L3D.*;
L3D cube;


public class NoMovesException extends Exception {
  public NoMovesException(String message){
     super(message);
  }
}

int deathFrame;
PVector[] directions = {
    new PVector(1,0,0),
    new PVector(-1,0,0),
    new PVector(0,1,0),
    new PVector(0,-1,0),
    new PVector(0,0,1),
    new PVector(0,0,-1)
};
PVector direction = directions[0];
ArrayList<PVector> snake;
ArrayList<PVector> treats;

int snakeLength;
int speed;


void setup() {
    size(700, 700, P3D);
    frameRate(1);
    background(0);

    cube = new L3D(this);
    cube.enableDrawing();
    cube.enablePoseCube();
    cube.enableMulticastStreaming();

    snake = new ArrayList<PVector>();
    treats = new ArrayList<PVector>();

    resetCube();
}


void addTreat() {
    PVector treat;

    while (true) {
        treat = new PVector(int(random(7.99)), int(random(7.99)), int(random(7.99)));
        if (!snake.contains(treat)) {
            treats.add(treat);
            return;
        }
    }
}

void resetCube() {
    direction = new PVector(1, 0, 0);
    snakeLength = 5;
    snake.clear();
    snake.add(new PVector(0, 0, 0));
    speed = 10;
    frameRate(speed);
    deathFrame = -1;
    treats.clear();
    addTreat();
}


boolean canMove(PVector direction) {
    PVector front = PVector.add(snake.get(0), direction);
    return front.x >= 0 && front.y >= 0 && front.z >= 0 && front.x <= 7 && front.y <= 7 && front.z <= 7 && !snake.contains(front);
}


PVector getNextDirection(PVector currentDirection) throws NoMovesException {
    // Mostly reuse the same direction but sometimes turn at random
    if (canMove(currentDirection) && random(1) < 0.8) {
        return currentDirection;
    }

    ArrayList<PVector> availableDirections = new ArrayList<PVector>();

    for (int i=0; i<directions.length; i++) {
        if (directions[i] != currentDirection && canMove(directions[i])) {
            availableDirections.add(directions[i]);
        }
    }

    if (availableDirections.size() == 0) {
        throw new NoMovesException("");
    }

    Collections.shuffle(availableDirections);

    if (treats.size() == 0) {
        return availableDirections.get(0);
    }

    PVector bestMove = availableDirections.get(0);
    PVector front;
    float bestDistance = -1;
    float distance;

    for (int i=0; i<availableDirections.size(); i++) {
        front = PVector.add(snake.get(0), availableDirections.get(i));
        distance = PVector.dist(front, treats.get(0));
        if (bestDistance == -1 || distance < bestDistance) {
            bestMove = availableDirections.get(i);
            bestDistance = distance;
        }
    }
    
    return bestMove;
}

void moveSnake() {
    PVector front;
    PVector nextDirection;
    try {
        nextDirection = getNextDirection(direction);
    } catch (NoMovesException e) {
        deathFrame = frameCount;
        return;
    }

    front = PVector.add(snake.get(0), nextDirection);

    int treatIndex = -1;
    try {
        treatIndex = treats.indexOf(front);
        treats.remove(treatIndex);
        snakeLength++;
        speed = min(speed + 1, 60);
    } catch (ArrayIndexOutOfBoundsException e) {

    }

    snake.add(0, front);
    while (snake.size() > snakeLength) {
        snake.remove(snake.size() - 1);
    }

    if (treatIndex != -1) {
        addTreat();
    }        
}

void worldUpdate() {
    frameRate(speed);
    if (deathFrame != -1) {
        if (frameCount - deathFrame > 100) {
            resetCube();
        }
    } else {
        moveSnake();
    }
}


void draw() {
    background(0);
    cube.background(0);

    worldUpdate();

    for (int i=0; i<snake.size(); i++) {
        int segmentColor = color(255 - (i*255)/snake.size(), 0, 0);
        if (deathFrame != -1 && frameCount % 16 < 8) {
            segmentColor = color(255 - (i*255)/snake.size(), 255 - (i*255)/snake.size(), 255 - (i*255)/snake.size());
        }

        cube.setVoxel(snake.get(i), segmentColor);
    }

    if (deathFrame == -1) {
        for (int i=0; i<treats.size(); i++) {
            cube.setVoxel(treats.get(i), color(0, 0, 255));
        }
    }
}