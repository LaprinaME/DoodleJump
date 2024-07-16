import random
import math
import pygame

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Doodle Jump')

# Load fonts
big_font = pygame.freetype.Font('font.ttf', 75)
middle_font = pygame.freetype.Font('font.ttf', 40)
small_font = pygame.freetype.Font('font.ttf', 25)

# Load images
player_image = pygame.transform.scale(pygame.image.load('doodle2.png'), (90, 90))
platform_image = pygame.transform.scale(pygame.image.load('platform.png'), (200, 70))
menu_background = pygame.transform.scale(pygame.image.load('menu_background.png'), (800, 800))
game_background = pygame.transform.scale(pygame.image.load('jungles.png'), (800, 800))
center_sprite_image = pygame.transform.scale(pygame.image.load('sprite.png'), (700, 800))

# Christmas version images
christmas_player_image = pygame.transform.scale(pygame.image.load('doodle7.png'), (90, 90))
christmas_platform_image = pygame.transform.scale(pygame.image.load('christmas_platform.png'), (200, 70))
christmas_game_background = pygame.transform.scale(pygame.image.load('christmas_background.png'), (800, 800))
christmas_center_sprite_image = pygame.transform.scale(pygame.image.load('christmas_sprite.png'), (700, 800))

# Initial game variables
high_score = 0
on_ground = True
speed = 0
player = None
is_christmas_version = False


# Center sprite shaking animation
def get_shaking_position(base_position, amplitude, frequency, time):
    x, y = base_position
    shake_x = amplitude * math.sin(frequency * time)
    shake_y = amplitude * math.cos(frequency * time)
    return x + shake_x, y + shake_y


def draw_menu_header():
    text_surface, rect = big_font.render('Doodle Jump', (0, 0, 0))
    screen.blit(text_surface, (300, 200))

    text_surface, rect = small_font.render(f'Highscore: {high_score}', (0, 0, 0))
    screen.blit(text_surface, ((screen.get_rect().w - rect.w) / 2, 300))


def draw_button(button_rect, text, font, color=(242, 165, 22)):
    pygame.draw.rect(screen, color, button_rect, border_radius=25)
    text_surf, text_rect = font.render(text, (255, 255, 255))
    screen.blit(
        text_surf,
        (
            button_rect.x + (button_rect.width - text_rect.width) / 2,
            button_rect.y + (button_rect.height - text_rect.height) / 2,
        ),
    )


def version_menu():
    standard_button_rect = pygame.Rect(275, 450, 250, 50)
    christmas_button_rect = pygame.Rect(275, 520, 250, 50)
    menu_run = True

    while menu_run:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if standard_button_rect.collidepoint(pos):
                    global is_christmas_version
                    is_christmas_version = False
                    menu_run = False
                    menu()
                if christmas_button_rect.collidepoint(pos):
                    is_christmas_version = True
                    menu_run = False
                    menu()

        screen.blit(menu_background, (0, 0))
        draw_menu_header()
        draw_button(standard_button_rect, 'Standard Version', middle_font)
        draw_button(christmas_button_rect, 'Christmas Version', middle_font)
        pygame.display.flip()

        clock.tick(20)


def menu():
    global player
    play_button_rect = pygame.Rect(325, 515, 150, 50)
    switch_version_button_rect = pygame.Rect(275, 590, 250, 50)  # Button to switch versions
    menu_run = True

    while menu_run:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pos):
                    menu_run = game()
                if switch_version_button_rect.collidepoint(pos):  # Check if switch version button is clicked
                    version_menu()

        screen.blit(menu_background, (0, 0))
        draw_menu_header()
        draw_button(play_button_rect, 'Play', middle_font)
        draw_button(switch_version_button_rect, 'Switch Version', middle_font)  # Draw switch version button
        pygame.display.flip()

        clock.tick(20)


def draw_result(score):
    pygame.draw.rect(screen, (242, 165, 22), (10, 40, 150, 50), border_radius=10)  # Colorful border for score
    text_surface, rect = small_font.render(f'Score: {score}', (255, 255, 255))
    screen.blit(text_surface, (20, 50))


def boundaries(player, platforms):
    global on_ground, speed

    for platform in platforms:
        if (
                player['rect'].right >= platform['rect'].left and
                player['rect'].left <= platform['rect'].right and
                platform['rect'].bottom >= player['rect'].bottom >= platform['rect'].top
        ):
            if speed >= 0:
                speed = 0
                on_ground = True
    if not on_ground:
        speed += 1


def game():
    global on_ground, speed, high_score

    game_run = True
    power = 10
    next_level = 10

    if is_christmas_version:
        player = {'rect': pygame.Rect(400, 500, 90, 90), 'image': christmas_player_image}
        background = christmas_game_background
        center_sprite = christmas_center_sprite_image
        platform_image = christmas_platform_image
    else:
        player = {'rect': pygame.Rect(400, 500, 90, 90), 'image': player_image}
        background = game_background
        center_sprite = center_sprite_image
        platform_image = pygame.transform.scale(pygame.image.load('platform.png'), (200, 70))

    score = 0

    platforms = [{'rect': pygame.Rect(random.randint(230, 550), (i * 100) + 100, 250, 30), 'image': platform_image} for
                 i in range(10)]
    upper_platform = platforms[0]

    speed = 0
    on_ground = True
    fail = False

    center_sprite_base_position = (screen.get_width() // 2 - center_sprite.get_width() // 2,
                                   screen.get_height() // 2 - center_sprite.get_height() // 2)
    amplitude = 5
    frequency = 0.1
    time = 0

    while game_run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player['rect'].x -= 5
        if keys[pygame.K_d]:
            player['rect'].x += 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False

        if on_ground:
            speed = -power
            on_ground = False

        player['rect'].y += speed

        if upper_platform['rect'].y > power * 10:
            upper_platform = {'rect': pygame.Rect(random.randint(230, 550), 0, 250, 30), 'image': platform_image}
            platforms.append(upper_platform)

        for platform in platforms:
            if speed < 0:
                if player['rect'].y < 300:
                    platform['rect'].y -= speed * 2
                platform['rect'].y -= speed
            if platform['rect'].y >= 820:
                platforms.remove(platform)
                score += 1

        screen.blit(background, (0, 0))

        # Draw center sprite with shaking animation
        time += 1
        center_sprite_position = get_shaking_position(center_sprite_base_position, amplitude, frequency, time)
        screen.blit(center_sprite, center_sprite_position)

        draw_result(score)
        screen.blit(player['image'], player['rect'].topleft)
        for platform in platforms:
            screen.blit(platform['image'], platform['rect'].topleft)
        boundaries(player, platforms)

        if player['rect'].y >= 820:
            if score > high_score:
                high_score = score
            game_run = False
            fail = True

        if score > next_level:
            next_level += 10
            power += 1

        pygame.display.flip()
        clock.tick(60)

    if fail:
        game_over_menu()


def game_over_menu():
    global player
    restart_button_rect = pygame.Rect(325, 515, 150, 50)
    exit_button_rect = pygame.Rect(325, 585, 150, 50)
    menu_run = True

    while menu_run:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(pos):
                    menu_run = game()
                if exit_button_rect.collidepoint(pos):
                    pygame.quit()
                    return

        screen.blit(menu_background, (0, 0))
        draw_menu_header()
        draw_button(restart_button_rect, 'Restart', middle_font)
        draw_button(exit_button_rect, 'Exit', middle_font)
        pygame.display.flip()

        clock.tick(20)

menu()
pygame.quit()
