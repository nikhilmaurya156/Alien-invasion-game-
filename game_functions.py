import pygame
from bullets import Bullet
from aliens import Alien
import sys
from time import sleep
import shelve

def check_high_score(stats, sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_aliens_bottom(ai_s, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_s, screen, stats, sb, ship, aliens, bullets)
            break
        
def ship_hit(ai_s, screen, stats, sb, ship, aliens, bullets):
    if stats.ship_left>0:
        stats.ship_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_s, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_fleet_edges(ai_s, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_s, aliens)
            break

def change_fleet_direction(ai_s, aliens):
    for alien in aliens.sprites():
        alien.rect.y+= ai_s.fleet_drop_speed
    ai_s.fleet_direction *= -1

def update_aliens(ai_s, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_s, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_s, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_s, screen, stats, sb, ship, aliens, bullets)
    
def get_number_rows(ai_s, ship_height, alien_height):
    available_space_y = (ai_s.screen_height - (3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def get_number_aliens_x(ai_s, alien_width):
    available_space_x = ai_s.screen_width-2*alien_width
    number_alien_x = int(available_space_x/(2*alien_width))
    return number_alien_x

def create_alien(ai_s, screen, aliens, alien_number, row_number):
    alien = Alien(ai_s, screen)
    alien_width = alien.rect.width
    alien.x = alien_width+2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_s, screen, ship,aliens):
    alien = Alien(ai_s, screen)
    number_aliens_x = get_number_aliens_x(ai_s, alien.rect.width)
    number_rows = get_number_rows(ai_s, ship.rect.height, alien.rect.height)
    
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_s, screen, aliens, alien_number, row_number)
        
def update_bullets(ai_s, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_s, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_s, screen, stats, sb, ship, aliens, bullets):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        for aliens in collision.values():
            stats.score += ai_s.alien_points* len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens)== 0:
        bullets.empty()
        ai_s.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_s, screen, ship, aliens)
    
def check_keydown_events(event, ai_s, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_s, screen, ship, bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()

def fire_bullets(ai_s, screen, ship, bullets):
    if len(bullets)<ai_s.bullet_allowed:
        new_bullet = Bullet(ai_s, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_s, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_s, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) 
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_s, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_s, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_s.initialize_dynamic_setting()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        create_fleet(ai_s, screen, ship, aliens)
        ship.center_ship()
                             
def update_screen(ai_s, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_s.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()
