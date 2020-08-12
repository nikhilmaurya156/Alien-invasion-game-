import pygame 
from buttons import Button
from aliens import Alien
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group 
from game_stats import GameStats
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_s = Settings()
    running = True 
    screen = pygame.display.set_mode((ai_s.screen_width, ai_s.screen_height))
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_s, screen, 'Play')
    stats = GameStats(ai_s)
    sb = Scoreboard(ai_s, screen, stats)
    bg_color = (230,230,230)
    ship = Ship(ai_s, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_s, screen, ship, aliens)

    while running:
        gf.check_events(ai_s, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_s, screen, stats, sb, ship,aliens, bullets)
            gf.update_aliens(ai_s, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_s, screen, stats, sb, ship, aliens, bullets, play_button)
run_game()
