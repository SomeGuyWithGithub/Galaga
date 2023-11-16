import basic_enemy
import pygame
from sys import exit


def create_enemy_array():
    enemy_list = []
    for y in range(25, 201, 40):
        for x in range(10, 351, 50):
            enemy_list.append(basic_enemy.BasicEnemy((x, y)))
    return enemy_list


def enemy_movement(dir):
    movement = 1 if dir == 'right' else -1
    return movement


def update_enemies(enemy_list, movement, missile_list, score, enemy_move, farthest, current_time, enemy_missile_list, screen):
    for enemy in list(enemy_list):
        enemy.rect.x += movement
        enemy.animation()

        # collisionlist() returns index of first collision
        collision_index = enemy.rect.collidelist(missile_list)
        if collision_index != -1:
            del missile_list[collision_index]
            enemy.health -= 1
            if not enemy.health:
                enemy_list.remove(enemy)
                score += enemy.score_gain

        # if the enemy is moving to right, then gives the farthest right position
        # else, gives the farthest left position
        if enemy_move == 'right':
            if enemy.rect.right > farthest:
                farthest = enemy.rect.right
        else:
            if enemy.rect.left < farthest:
                farthest = enemy.rect.left

        # checks to see if create_missile returns a missile rect or None
        enemy_missile = enemy.create_missile(current_time)
        if enemy_missile is not None:
            enemy_missile_list.append(enemy_missile)

        screen.blit(enemy.surf, enemy.rect)
    return enemy_list, missile_list, score, farthest, enemy_missile_list, screen


def change_move(enemy_move, farthest):
    if enemy_move == 'right' and farthest >= 475:
        enemy_move = 'left'
    elif enemy_move == 'left' and farthest <= 25:
        enemy_move = 'right'
    return enemy_move


def is_stage_clear(enemy_list, stage_clear, time_at_stage_clear, current_time):
    if enemy_list == [] and not stage_clear:
        stage_clear = True
        time_at_stage_clear = current_time
    return stage_clear, time_at_stage_clear


def display_new_stage(new_stage, time_at_reset, screen, new_stage_surf, new_stage_rect):
    if new_stage:
        if pygame.time.get_ticks() - time_at_reset >= 2500:
            new_stage = False
        screen.blit(new_stage_surf, new_stage_rect)
    return new_stage, screen


def display_score(screen, score_title, font, score):
    screen.blit(score_title, (25, 25))
    score_surf = font.render(str(score), False, (255, 255, 255))
    score_rect = score_surf.get_rect(topleft=(25, 50))
    screen.blit(score_surf, score_rect)
    return screen


def player_missile_update(missile_list, missile_surf, screen):
    for missile in missile_list:
        missile.y -= 5
        if missile.bottom <= 0:
            missile_list.remove(missile)
            continue
        screen.blit(missile_surf, missile)
    return missile_list, screen


def enemy_missile_update(enemy_missile_list, enemy_missile_surf, stage, screen):
    for missile in enemy_missile_list:
        missile.y += 5 * (stage / 5 + 1)
        if missile.top >= 600:
            enemy_missile_list.remove(missile)
            continue
        screen.blit(enemy_missile_surf, missile)
    return enemy_missile_list, screen


def player_colls(player_rect, enemy_missile_list, life_count):
    collision_index = player_rect.collidelist(enemy_missile_list)
    if collision_index != -1:
        del enemy_missile_list[collision_index]
        life_count -= 1
    return enemy_missile_list, life_count


def main():
    # move code only needed once here
    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption('Galaga')
    clock = pygame.time.Clock()

    player_surf = pygame.image.load('Graphics/player_images/player_image.png').convert_alpha()
    player_rect = player_surf.get_rect(center=(250, 550))

    alive = True
    new_stage = True
    stage = 1
    font = pygame.font.Font('font/Emulogic-zrEw.ttf', 20)
    new_stage_surf = font.render(f'Stage {stage}', False, (255, 0, 0))
    new_stage_rect = new_stage_surf.get_rect(center=(250, 300))
    game_over_surf = font.render('Game Over', False, (255, 0, 0))
    game_over_rect = game_over_surf.get_rect(center=(250, 300))

    life_surf = pygame.image.load('Graphics/player_images/life_image.png').convert_alpha()
    life_count = 2

    score = 0
    score_title = font.render('Score', False, (255, 0, 0))

    missile_list = []
    player_missile_time = 0
    missile_surf = pygame.image.load('Graphics/player_images/player_missile.png').convert_alpha()

    enemy_list = create_enemy_array()
    enemy_move = 'right'
    farthest = 0

    enemy_missile_surf = pygame.image.load('Graphics/enemy_missile.png').convert_alpha()
    enemy_missile_list = []

    time_at_reset = 0
    time_at_stage_clear = 0
    stage_clear = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not alive:
                alive = True
                player_rect = player_surf.get_rect(center=(250, 550))

                life_count = 2

                missile_list = []
                player_missile_time = 0

                enemy_move = 'right'
                farthest = 0

                enemy_list = create_enemy_array()

                enemy_missile_list = []

                time_at_reset = pygame.time.get_ticks()
                stage_clear = False

        if alive:
            current_time = pygame.time.get_ticks() - time_at_reset

            # keys for when the player moves or shoots
            keys = pygame.key.get_pressed()
            # exits game when esc key pressed
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            # move left
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_rect.left >= 25:
                player_rect.x -= 2
            # move right
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_rect.right <= 475:
                player_rect.x += 2
            # shoot missile
            if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[
                pygame.K_UP]) and current_time - player_missile_time >= 500:
                player_missile_time = current_time
                missile_rect = missile_surf.get_rect(center=player_rect.midtop)
                missile_list.append(missile_rect)

            # background
            screen.fill('Black')

            # moves enemy to the right or left
            movement = enemy_movement(enemy_move)

            # dont know why this **** works, but dont touch it
            # iterates over a copy of the enemy list
            enemy_list, missile_list, score, farthest, enemy_missile_list, screen = update_enemies(
                enemy_list, movement, missile_list, score, enemy_move,
                farthest, current_time, enemy_missile_list, screen)

            # once the farthest enemy is close enough to the border, then reverses direction
            enemy_move = change_move(enemy_move, farthest)

            # checks when stage is clear and assigns variables
            stage_clear, time_at_stage_clear = is_stage_clear(enemy_list, stage_clear, time_at_stage_clear, current_time)

            if current_time - time_at_stage_clear > 1000 and stage_clear:
                stage_clear = False
                new_stage = True
                stage += 1
                new_stage_surf = font.render(f'Stage {stage}', False, (255, 0, 0))
                new_stage_rect = new_stage_surf.get_rect(center=(250, 300))
                player_missile_time = 0
                time_at_reset = pygame.time.get_ticks()
                enemy_list = create_enemy_array()

            # display new stage
            new_stage, screen = display_new_stage(new_stage, time_at_reset, screen, new_stage_surf, new_stage_rect)

            # display score
            screen = display_score(screen, score_title, font, score)

            # moves player missiles and remove once they go off-screen
            missile_list, screen = player_missile_update(missile_list, missile_surf, screen)

            # moves enemy missiles and remove once they go off of screen
            enemy_missile_list, screen = enemy_missile_update(enemy_missile_list, enemy_missile_surf, stage, screen)

            # checks for player collisions
            enemy_missile_list, life_count = player_colls(player_rect, enemy_missile_list, life_count)

            # displays life counter at bottom left
            for x in range(1, life_count + 1):
                life_rect = life_surf.get_rect(bottomleft=(x * 30, 575))
                screen.blit(life_surf, life_rect)

            # if the player is still alive, display player
            if life_count >= 0:
                # display player
                screen.blit(player_surf, player_rect)
            else:
                alive = False
        else:
            screen.blit(game_over_surf, game_over_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
