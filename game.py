import pygame
import sys


from game_modules.screen import Screen
from game_modules.levels.level_infinite import LevelInfinite
from game_modules.save_score import Save_Score


from game_modules.controllers.player import Player


from game_modules.settings.sprites import PlayerSprites
from game_modules.settings.strings import GameTexts
from game_modules.settings.colors import GameColors
from game_modules.settings.audio import GameAudios
from game_modules.settings.platform import PlatformSettings


class Game:
    """
        Game is responsible for user interactions
    """

    def __init__(self):
        
        self.playing = None
        self.main_menu = False

        
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()
       
        self.screen = Screen(self)
        self.player = Player(self)
        self.level = LevelInfinite(self)
        self.save_score = Save_Score(self)

        
        img_icon = pygame.image.load(
            PlayerSprites.PLAYER_IMAGE_LIST_RIGHT[2]).convert_alpha()
        pygame.display.set_icon(img_icon)
        pygame.display.set_caption(GameTexts.TITLE)

        
        self.clock = pygame.time.Clock()
        self.pause = False

       
        self.music_number = 0
        self.sum = False
        self.playlist = list()

        self.playlist.append(GameAudios.MUSIC[0])
        self.playlist.append(GameAudios.MUSIC[1])

    def show_menu(self):
        """
            Show the main menu
        """
        self.screen.show_start_screen()

    def music_playlist(self): 

        if pygame.mixer.music.get_busy() == False:
            if self.sum == True:
                self.music_number += 1
            else:
                self.sum = True
            
            pygame.mixer.music.load(self.playlist[self.music_number])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()

            if self.music_number == len(self.playlist)-1:
                self.music_number = 0
                self.sum = False

    def new(self): 

        self.main_menu = False

        
        if len(self.level.all_sprites) != 0:
            self.level.killAllSprites()

        
        pygame.mixer.music.stop()

        
        self.music_playlist()

        
        self.run()

    def run(self): 

        self.playing = True

       
        self.level.score = 0
        self.level.max_enemies = 0
        self.level.initSprites()

        
        while self.playing:
            self.clock.tick(PlatformSettings.FPS)
            self.events()
            self.update()
            self.draw()
            self.music_playlist()

    def update(self): 

        self.level.all_sprites.update()

        
        keys = pygame.key.get_pressed()

        
        self.player.collisionDetection()

        

        if self.player.pos.x <= 0:
            self.player.pos.x = 0

       
        if self.player.rect.right >= (PlatformSettings.WIDTH - 250):
            self.player.pos.x -= abs(self.player.vel.x)

       
        if keys[pygame.K_RIGHT]:

           
            self.level.kill_move("Enemy")

            
            self.level.kill_move("Platform")

            
            self.level.kill_move("Asset")

           
            self.level.kill_move("Base")

       
        if len(self.level.platforms) < 1:
            self.level.randEntities("Platform")

        if len(self.level.enemies) < 1:
            self.level.randEntities("Enemy")

        if len(self.level.assets) < 2:
            self.level.randEntities("Asset")

        
        if self.player.rect.bottom >= PlatformSettings.HEIGHT:
            self.screen.game_over()

    def events(self): 

        for event in pygame.event.get():

            
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_ESCAPE:
                    if self.pause == True:
                        self.unpause()
                    elif self.pause == False:
                        self.pause = True
                        self.screen.paused()

    def draw(self): 

        self.screen.surface.fill(GameColors.WHITE)

        self.level.all_sprites.draw(self.screen.surface)

       
        self.level.showScore()

        
        pygame.display.flip()

    def unpause(self): 

        self.pause = False
        pygame.mixer.music.unpause()

    def quit_game(self):  

        if self.main_menu:
            pygame.quit()
            sys.exit(0)



g = Game()


g.show_menu()
