import pygame
from constants import *
from ui import *
from screens import *

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Chaos Equations")
    clock = pygame.time.Clock()

    simulation = Simulation(screen, clock)
    simulation.Run()

    pygame.quit()

class Simulation:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        n_height = HEIGHT / 4

        # BUTTONS
        self.ChaosEquationButton = Button(WIDTH//2 - 100, n_height, 200, 60, "Chaos Equation")
        self.LorenzAttractorButton = Button(WIDTH//2 - 100, n_height + 100, 200, 60, "Lorenz Attractor")
        self.AizawaAttractorButton = Button(WIDTH//2 - 100, n_height + 200, 200, 60, "Aizawa Attractor")
        self.ThomasAttractorButton = Button(WIDTH//2 - 100, n_height + 300 , 200, 60, "Thomas Attractor")
        # SCREENS
        self.chaosScreen = Chaos(screen, clock)
        self.Attractors = Attractor(screen, clock)

        self.running = True
    
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
    def ClearScreen(self):
        self.screen.fill(BLACK)
    
    def Run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.ClearScreen()
            self.HandleEvent()
            # Main Menu

            if self.ChaosEquationButton.Draw(self.screen):
                self.chaosScreen.Run()
            elif self.LorenzAttractorButton.Draw(self.screen):
                self.Attractors.Lorenz()
            elif self.ThomasAttractorButton.Draw(self.screen):
                self.Attractors.Thomas()
            elif self.AizawaAttractorButton.Draw(self.screen):
                self.Attractors.Aizawa()
            
            pygame.display.update()
            


if __name__ == "__main__":
    main()

