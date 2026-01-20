import pygame
from rider_ import RiderIdle
from rider_move import RiderMove
from Rider_Jump import RiderJump
from RiderAttack import RiderAttack
from cyborg import CyborgEnemy
from rider_run_attack import RiderRunAttack
from RiderSuperAttack import RiderSuperAttack

pygame.init()
pygame.mixer.init()
# SOUND EFFECTS
PUNCH_SFX = pygame.mixer.Sound("Python/BackgroundMusic/Rider_punch.wav")
PUNCH_SFX.set_volume(1.0)

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MOB MECHA")
clock = pygame.time.Clock()

base_surface = pygame.image.load("python/Elements/Background.png").convert()
resized_base = pygame.transform.scale(base_surface, (800, 400))

rider = RiderIdle(100, 300)
all_sprites = pygame.sprite.Group(rider)
cyborg = CyborgEnemy(500, 300)
all_sprites.add(cyborg)

# XP SYSTEM
rider_xp = 0
rider_xp_max = 100
super_ready = False

# GAME STATE
game_state = "controls"   # "controls" or "game"

TUTORIAL_BGM = "Python/BackgroundMusic/cyberpunk.mp3"
GAME_BGM="Python/BackgroundMusic/cyberpunk_main.mp3"

pygame.mixer.music.load(TUTORIAL_BGM)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # loop continuously




def replace_rider(new_rider):
    for s in list(all_sprites):
        if isinstance(
            s,
            (RiderIdle, RiderMove, RiderJump, RiderAttack, RiderRunAttack, RiderSuperAttack)
        ):
            all_sprites.remove(s)

    all_sprites.add(new_rider)
    return new_rider


def draw_health_bar(surface, x, y, width, height, current, maximum):
    ratio = current / maximum
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))


def draw_xp_bar(surface, x, y, width, height, current, maximum):
    ratio = current / maximum
    color = (0, 180, 255) if current >= maximum else (0, 120, 255)
    pygame.draw.rect(surface, (40, 40, 40), (x, y, width, height))
    pygame.draw.rect(surface, color, (x, y, width * ratio, height))


def draw_controls_screen(surface):
    surface.fill((0, 0, 0))

    font_title = pygame.font.SysFont("arial", 36, bold=True)
    font_text = pygame.font.SysFont("arial", 22)

    title = font_title.render("CONTROLS", True, (0, 255, 0))
    surface.blit(title, (320, 40))

    controls = [
        "A / D        - Move Left / Right",
        "SPACE        - Jump",
        "Left Click   - Attack",
        "Left Click (while moving) - Run Attack",
        "Right Click  - Super Attack (XP full)",
        "",
        "Press ENTER to Start"
    ]

    y = 120
    for line in controls:
        text = font_text.render(line, True, (0, 255, 0))
        surface.blit(text, (220, y))
        y += 35


while True:
    keys = pygame.key.get_pressed()

    # ================= EVENT LOOP =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ENTER → START GAME
        if game_state == "controls":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("GAME BGM STARTED")

                game_state = "game"
                pygame.mixer.music.stop()
                pygame.mixer.music.load(GAME_BGM)
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)

        # BLOCK INPUT WHILE ON CONTROLS SCREEN
        if game_state != "game":
            continue

        # LEFT CLICK – NORMAL ATTACKS
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if isinstance(rider, RiderMove) and not isinstance(rider, RiderRunAttack):
                rider = replace_rider(
                    RiderRunAttack(rider.rect.x, rider.rect.y, facing_left=rider.facing_left)
                )
            elif rider.on_ground and not isinstance(rider, RiderAttack):
                rider = replace_rider(
                    RiderAttack(rider.rect.x, rider.rect.y, facing_left=rider.facing_left)
                )

        # RIGHT CLICK – SUPER ATTACK
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if super_ready and not isinstance(rider, RiderSuperAttack):
                rider = replace_rider(
                    RiderSuperAttack(rider.rect.x, rider.rect.y, facing_left=rider.facing_left)
                )
                rider_xp = 0
                super_ready = False

    # ================= CONTROLS SCREEN =================
    if game_state == "controls":
        draw_controls_screen(screen)
        pygame.display.update()
        clock.tick(50)
        continue

    # ================= GAME LOGIC =================
    old_x, old_y = rider.rect.x, rider.rect.y
    facing_left = getattr(rider, "facing_left", False)
    vel_y = getattr(rider, "vel_y", 0)
    on_ground = getattr(rider, "on_ground", True)

    # JUMP
    if keys[pygame.K_SPACE] and on_ground and not isinstance(rider, RiderAttack):
        rider = replace_rider(
            RiderJump(old_x, old_y, facing_left=facing_left, vel_y=-12, on_ground=False)
        )

    # MOVE
    elif (keys[pygame.K_a] or keys[pygame.K_d]) and isinstance(rider, RiderIdle):
        rider = replace_rider(
            RiderMove(old_x, old_y, facing_left=facing_left, vel_y=vel_y, on_ground=on_ground)
        )

    elif not (keys[pygame.K_a] or keys[pygame.K_d]) and isinstance(rider, RiderMove):
        rider = replace_rider(
            RiderIdle(old_x, old_y, facing_left=facing_left, vel_y=0, on_ground=True)
        )

    all_sprites.update(keys)
    cyborg.update_ai(rider)
    


    # CONTACT DAMAGE LOGIC
    rider_body = rider.get_body_hitbox() if hasattr(rider, "get_body_hitbox") else None
    cyborg_body = cyborg.get_hitbox()

    if (
        isinstance(rider, (RiderAttack, RiderRunAttack, RiderSuperAttack))
        and rider_body
        and rider_body.colliderect(cyborg_body)
        and rider.on_ground
        and not rider.hit_done
    ):
        cyborg.health -= rider.damage
        rider.hit_done = True
        PUNCH_SFX.play()


        if not super_ready:
            rider_xp += 10
            if rider_xp >= rider_xp_max:
                rider_xp = rider_xp_max
                super_ready = True

    # STATE RETURNS
    if isinstance(rider, RiderJump) and rider.on_ground:
        rider = replace_rider(RiderIdle(rider.rect.x, rider.rect.y, facing_left=rider.facing_left))

    if isinstance(rider, (RiderRunAttack, RiderAttack, RiderSuperAttack)) and rider.attack_finished:
        rider = replace_rider(
            RiderIdle(rider.rect.x, rider.rect.y, facing_left=rider.facing_left, vel_y=0, on_ground=True)
        )

    # ================= DRAW GAME =================
    screen.fill((10, 15, 40))
    screen.blit(resized_base, (0, 0))
    all_sprites.draw(screen)

    draw_health_bar(screen, 20, 20, 200, 15, rider.health, rider.max_health)
    draw_health_bar(screen, 580, 20, 200, 15, cyborg.health, cyborg.max_health)
    draw_xp_bar(screen, 20, 38, 200, 6, rider_xp, rider_xp_max)

    pygame.display.update()
    clock.tick(50)
