import pygame
import sys
import os

from enum import Enum
from asteroidal.constants import *
from asteroidal.shapes import *
from asteroidal.asteroidfield import *


# Define game states using Enum
class GameState(Enum):
    MENU = 0
    GAMEPLAY = 1
    PAUSE = 2
    GAME_OVER = 3

class GameStateManager:
    def __init__(self):    
        # audio handling in WLS2
        if sys.platform == "linux":
            os.environ["SDL_AUDIODRIVER"] = "dummy"
        
        # Pygame inits
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroidal")
        
        # define variables
        self.clock = pygame.time.Clock()
        self.dt: float = 0.0
        
        # set gamestate for startup
        self.current_state = GameState.MENU
        
        # setting up groups and containers
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Player reference
        self.player: Player | None = None

    def start(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.dt = self.clock.tick(FPS) / 1000

    # Handle any input events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if self.current_state == GameState.MENU:
                    self.handle_menu_input(event.key)
                elif self.current_state == GameState.GAMEPLAY:
                    self.handle_gameplay_input(event.key)
                elif self.current_state == GameState.PAUSE:
                    self.handle_pause_input(event.key)
                elif self.current_state == GameState.GAME_OVER:
                    self.handle_game_over_input(event.key)

    # Handle input events in the MENU state
    def handle_menu_input(self, key):
        if key == pygame.K_1:  # start gameplay
            self.start_gameplay()
        elif key == pygame.K_2:  # quit game
            self.quit_game()

    # Handle input events in the GAMEPLAY state
    def handle_gameplay_input(self, key):
        if key == pygame.K_p:  # pause
            self.current_state = GameState.PAUSE

    # Handle input events in the PAUSE state
    def handle_pause_input(self, key):
        if key == pygame.K_p:  # resume gameplay
            self.current_state = GameState.GAMEPLAY
        elif key == pygame.K_q:  # quit game
            self.quit_game()

    # Handle input events in the GAME_OVER state
    def handle_game_over_input(self, key):
        if key == pygame.K_r:  # restart game
            self.current_state = GameState.MENU

    def start_gameplay(self):
        self.current_state = GameState.GAMEPLAY        
        
        # Assigning containers
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Shot.containers = (self.shots, self.updatable, self.drawable)
        
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2, PLAYER_RADIUS)
        AsteroidField()


    # Update the game state
    def update(self):
        if self.current_state == GameState.GAMEPLAY:
            self.updatable.update(self.dt)

            for asteroid in self.asteroids:
                if asteroid.collides_with(self.player):
                    self.current_state = GameState.GAME_OVER
                
                for shot in self.shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()


    # Render the current state
    def render(self):
        self.screen.fill("black")  # clear screen

        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.GAMEPLAY:
            self.render_gameplay()
        elif self.current_state == GameState.PAUSE:
            self.render_pause()
        elif self.current_state == GameState.GAME_OVER:
            self.render_game_over()

        pygame.display.flip()  # update screen

    # Render the menu screen
    def render_menu(self):
        font = pygame.font.Font(None, 36)
        text1 = font.render("Press 1 to start", True, "white")
        text2 = font.render("Press 2 to quit", True, "white")
        self.screen.blit(text1, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 40))
        self.screen.blit(text2, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2))

    # Render the gameplay screen
    def render_gameplay(self):
        for sprite in self.drawable:
            sprite.draw(self.screen)

    # Render the pause screen
    def render_pause(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Paused - Pushin' P, like Gunna", True, "white")
        self.screen.blit(text, (SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2))

    # Render the game over screen
    def render_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over - Press R for menu", True, "white")
        self.screen.blit(text, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2))

    # Quit the game
    def quit_game(self):
        pygame.quit()
        quit()


# Entry point of the program
if __name__ == "__main__":
    game_state_manager = GameStateManager()
    game_state_manager.start()