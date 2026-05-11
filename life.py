import pygame
import copy
import random
class Grid():
    def __init__(self, position, divisions, size, color, gridColor, outline):
        self.position = pygame.math.Vector2(position)
        self.divisions = pygame.math.Vector2(divisions)
        self.size = pygame.math.Vector2(size)
        self.color = color 
        self.gridColor = gridColor
        self.cell = pygame.math.Vector2(self.size.x/self.divisions.x, self.size.y/self.divisions.y)
        self.outline = outline
        self.rects = [\
                [ pygame.Rect( \
                self.position.x + self.cell.x * i,\
                self.position.y + self.cell.y * j,\
                self.cell.x - outline, self.cell.y - outline) \
                for j in range(int(self.divisions.y))] \
                for i in range(int(self.divisions.x))\
                ]

        self.state = [\
                [ False\
                for i in range(int(self.divisions.y))] \
                for j in range(int(self.divisions.x))\
                      ]
        self.newState =  self.state

    def draw(self, screen, grid):
        for columns, states in zip(self.rects, self.state):
            for cell, state in zip(columns, states):
                if state:
                    pygame.draw.rect(screen, self.color, cell, 0)
                    #pygame.draw.circle(screen, self.color, cell.center ,cell.width/2)
                if grid:
                    pygame.draw.rect(screen, self.gridColor, cell, 1)
        return

    def clear(self, state):
        self.state = [[ state\
                for i in range(int(self.divisions.y))]\
                for j in range(int(self.divisions.x))]
        self.newState = copy.deepcopy(self.state)
        return 

    def rngState(self):
        self.state = [[\
                True if random.uniform(0.0, 1.0) > random.uniform(0.3, 1.0) else False\
                for _ in range(int(self.divisions.y))] \
                for p in range(int(self.divisions.x))]
        self.newState = copy.deepcopy(self.state)
        return

    def set(self, position, newState):
        x = int((position[0] - self.position.x)/self.cell.x)
        y = int((position[1] - self.position.y)/self.cell.y)
        if x >= 0 and y >= 0 and x < self.divisions.x and y < self.divisions.y:
            self.state[x][y] = newState  
            self.newState[x][y] = newState  

    def update(self):
        #Identify the 8 or less neighbours.
        for x in range(int(self.divisions.x)):
            for y in range(int(self.divisions.y)):
                indices = [
                        (x-1,y+1), (x,y+1), (x+1,y+1),\
                        (x-1,y  )         , (x+1,y  ),\
                        (x-1,y-1), (x,y-1), (x+1,y-1) \
                        ]
                neighbours = list()
                for i,j in indices:
                    if i >= 0 and j >=0 and i < self.divisions.x and j < self.divisions.y:
                        neighbours.append(self.state[i][j])
                #Get neighbours properties
                alive = 0
                current = self.state[x][y]
                for cell in neighbours:
                    if cell:
                        alive+=1
                if current:
                    if alive < 2:
                        self.newState[x][y] = False
                    elif alive < 4:
                        self.newState[x][y] = True
                    else:
                        self.newState[x][y] = False
                else:
                    if alive == 3:
                        self.newState[x][y] = True
        self.state = copy.deepcopy(self.newState)
        return

def init():
    global size, grid, updateSpeed, updateDelay, running, left_Held, right_Held, update, animate, UPDATE_EVENT
    display = pygame.display.Info()
    size = (display.current_w, display.current_h)
    grid = Grid(\
            (0,0),\
            (320,180),\
            size,\
            (200,200,200),\
            (60, 60, 60), 1)

    updateSpeed = 5 #Updates per second
    updateDelay = int(1000/updateSpeed) #Time taken for one update

    running = True
    left_Held = False
    right_Held = False
    update = False
    animate = False
    UPDATE_EVENT = pygame.USEREVENT + 1

def keyDown(key):
    global running, update, animate 
    match key:
        case pygame.K_ESCAPE:
            running = False
        case pygame.K_c:
            grid.clear(False)
        case pygame.K_f:
            grid.clear(True)
        case pygame.K_RETURN:
            update = True
        case pygame.K_r:
            grid.rngState()
        case pygame.K_SPACE:
            animate = not animate
            if animate:
                pygame.time.set_timer(UPDATE_EVENT, updateDelay)
                grid.update()
            else:
                pygame.time.set_timer(UPDATE_EVENT, 0)
        case _:
            pass

def mouse(button, state):
    global left_Held, right_Held
    match button:
        case 1:
            left_Held = state
        case 3:
            right_Held = state
        case _:
            pass
    
def input():
    global running, update
    update = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;

        elif event.type ==  pygame.KEYDOWN:
            keyDown(event.key)

        elif event.type == UPDATE_EVENT:
            grid.update()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse(event.button, True)

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse(event.button, False)

def main():
    init()
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    while running:
        input()
        screen.fill((0, 0, 0))
        if(left_Held):
            grid.set(pygame.mouse.get_pos(), True)
        if(right_Held):
            grid.set(pygame.mouse.get_pos(), False)
        if(update):
            grid.update()

        grid.draw(screen, True)
        pygame.display.update()
    return

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
