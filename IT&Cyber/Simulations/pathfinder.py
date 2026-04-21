
import pygame
import random 
import math 

pygame.init() 
DISPLAYSIZE = (800, 800) 
HUNTERCOLOR = (255, 0, 0) 
PREYCOLOR = (0, 0, 255) 

hunterR = 10 
preyR = 5 
hunterSpeed = 3 # pixels per frame 

pygame.display.set_caption("Pathfinder Algorith Test | Amundworks") 
window = pygame.display.set_mode(DISPLAYSIZE) 

class Hunter: 
    def __init__(self, startpos: tuple): 
        self.pos = startpos
        self.trail: list[trailParticle] = [] 
    def move(self, preypos): 
        dx = preypos[0] - self.pos[0] 
        dy = preypos[1] - self.pos[1] 
        rad = math.atan2(dy, dx) 
        newX = self.pos[0] + math.cos(rad) * hunterSpeed 
        newY = self.pos[1] + math.sin(rad) * hunterSpeed 
        self.pos = (newX, newY) 
    def updateTrail(self): 
        self.trail.append(trailParticle(self.pos)) 
        for p in self.trail: p.update() 
        self.trail = [p for p in self.trail if p.life > 0] 
    def draw(self): 
        for p in self.trail: fade = p.life / p.max_life 
        color = ( int(HUNTERCOLOR[0] * fade), int(HUNTERCOLOR[1] * fade), int(HUNTERCOLOR[2] * fade) ) 
        pygame.draw.circle(window, color, p.pos, p.radius) 
        pygame.draw.circle(window, HUNTERCOLOR, self.pos, hunterR) 

class trailParticle: 
    def __init__(self, pos): 
        self.pos = pos 
        self.max_life = 255 
        self.life = self.max_life 
        self.radius = 10 
    def update(self): 
        self.life -= 1 
        self.radius -= 0.05 
    def draw(self): 
        fade = self.life / self.max_life 
        r = int(HUNTERCOLOR[0] * fade) 
        g = int(HUNTERCOLOR[1] * fade) 
        b = int(HUNTERCOLOR[2] * fade) 
        pygame.draw.circle(window, (r, g, b), self.pos, self.radius) 

def coordinateDelta(pos1: float, pos2: float) -> float: 
    return abs(pos1 - pos2) 

def getRandomPos(screensize: tuple) -> tuple: 
    x = random.randint(0, screensize[0]) 
    y = random.randint(0, screensize[1]) 
    return (x, y) 

def checkIfTouch(hunterPos: tuple, preypos: tuple) -> bool: 
    if None in [hunterPos, preypos]: 
        return False 
    distance = math.hypot(coordinateDelta(hunterPos[0], preypos[0]), coordinateDelta(hunterPos[1], preypos[1])) 
    if distance <= (hunterR + preyR): 
        return True 
    else: return False 

run = True 
clock = pygame.time.Clock() 
hunterinit: bool = False # True when user has initialized the agent 
preypos: tuple = getRandomPos(DISPLAYSIZE) 
trailParticles: list = [] 
hunter = None 

while run: 
    window.fill((0, 0, 0)) 
    pygame.time.delay(16) 
    pygame.draw.circle(window, PREYCOLOR, preypos, preyR) 
    
    for event in pygame.event.get(): 
        if event.type == pygame.K_UP: 
            hunterSpeed += 1 
        if event.type == pygame.K_DOWN: 
            hunterSpeed -= 1 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            hunter = Hunter(pygame.mouse.get_pos()) 
        if event.type == pygame.QUIT: 
            run = False 
            
    if hunter: 
        hunter.move(preypos) 
        hunter.updateTrail() 
        hunter.draw()
        
        if checkIfTouch(hunter.pos, preypos): 
            preypos = getRandomPos(DISPLAYSIZE) 
            hunterR += 1 
            print(f"prey caught. Current size: {hunterR}") 

    pygame.display.flip() 
    clock.tick(60) 

pygame.quit()