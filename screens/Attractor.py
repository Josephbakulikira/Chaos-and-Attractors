import pygame
from constants import *
from utils import *

class Attractor:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        self.running = True

        self.toggleDots = False

        self.points = []
        self.angle = 0
        self.previous = None
        self.hue = 160
        self.limit_size = 3000
    
    def ClearScreen(self):
        self.screen.fill(BLACK)
    
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key == pygame.K_SPACE:
                    self.toggleDots = not self.toggleDots
    
    def Lorenz(self):
        # parameteres
        x = 0.01
        y = 0
        z = 0
        rho = 28
        beta = 8/4
        sigma = 10
    
        scale = 15

        time_step = 0.01
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.ClearScreen()
            self.HandleEvent()
            

            dx = (sigma * (y-x)) * time_step
            dy = (x * (rho - z) - y) * time_step
            dz = (x * y - beta *  z) * time_step

            x = x + dx
            y = y + dy
            z = z + dz
            
            point = [[round(x,3)], [round(y,3)], [round(z,3)]]
            self.points.append(point)
            # Perspective Projection of 3D point to 2D
            self.Render(self.points, scale, False)

            self.angle += 0.002
            self.hue += 0.1
                
            pygame.display.update()
        # Reset 
        self.points = []
        self.hue = 0
        self.angle = 0
        self.previous = None
        self.running = True

    def Aizawa(self):
        x = 0.01
        y = 0
        z = 0

        a = 0.95
        b = 0.7
        c = 0.6
        d = 3.5
        e = 0.25
        f = 0.1

        dx = 0
        dy = 0
        dz = 0

        scale = 1000

        time_step = 0.01
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.ClearScreen()
            self.HandleEvent()
            

            dx = ((z- b) * x - d * y) * time_step
            dy = (d * x + (z - b) * y) * time_step
            dz = (c + a * z - ((z**3)/3) - (x*x + y*y)*(1+e*z) + f*z*(x**3)) * time_step

            x = x + dx
            y = y + dy
            z = z + dz
            
            point = [[round(x,3)], [round(y,3)], [round(z,3)]]
            self.points.append(point)
            self.Render(self.points, scale)
            self.angle += 0.002
            self.hue += 0.1
                
            pygame.display.update()
        # Reset 
        self.points = []
        self.hue = 0
        self.angle = 0
        self.previous = None
        self.running = True

    def Thomas(self):
        x = 0.01
        y = 0
        z = 0

        b = 0.208186
        scale = 300
        
        time_step = 0.5
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.ClearScreen()
            self.HandleEvent()
            

            dx = (math.sin(y) - b * x) * time_step
            dy = (math.sin(z) - b * y) * time_step
            dz = (math.sin(x) -  b * z) * time_step

            x = x + dx
            y = y + dy
            z = z + dz

            
            point = [[round(x,3)], [round(y,3)], [round(z,3)]]
            self.points.insert(0, point)
            self.Render(self.points, scale)

            if len(self.points) > self.limit_size:
                self.points.pop()
            self.angle += 0.002
            self.hue += 0.1
                
            pygame.display.update()
        

        # Reset 
        self.points = []
        self.hue = 0
        self.angle = 0
        self.previous = None
        self.running = True

    def Render(self, points, scale, depth=True):
        for i in range(len(points)):
            transformed = matrix_multiplication(RotationY(self.angle), self.points[i])
            # transformed = matrix_multiplication(RotationZ(self.angle), transformed)
            distance = 5
            val = 1/ (distance - transformed[2][0])
            if depth:
                projection_matrix = [
                    [val, 0, 0],
                    [0, val, 0]
                ]
            else:
                projection_matrix = [
                    [1, 0, 0],
                    [0, 1, 0]
                ]
            projected_2D = matrix_multiplication(projection_matrix, transformed)

            x_pos = int(projected_2D[0][0] * scale) + WIDTH//2 + 100
            y_pos = int(projected_2D[1][0] * scale) + HEIGHT//2

            c = pygame.Color(0, 0, 0)
            ix, iy, iz = self.points[i]
            c.hsva = ((self.hue + (ix[0]+iy[0]+iz[0]))%360, 100, 100, 100)

            if self.toggleDots:
                pygame.draw.circle(self.screen, c, (round(x_pos), round(y_pos)), 2)
            elif self.previous and i != 0:
                pygame.draw.line(self.screen, c, (round(x_pos), round(y_pos)), self.previous, 2)
            
            self.previous = (round(x_pos), round(y_pos))