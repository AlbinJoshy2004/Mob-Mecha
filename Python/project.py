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

# ================= SOUND =================
PUNCH_SFX = pygame.mixer.Sound("Python/BackgroundMusic/Rider_punch.wav")
PUNCH_SFX.set_volume(1.0)

CYBORG_SFX = pygame.mixer.Sound("Python/BackgroundMusic/cyborg_punch.wav")
CYBORG_SFX.set_volume(2.0)


# ================= WINDOW =================
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MOB MECHA")
clock = pygame.time.Clock()

# ================= BACKGROUND =================
base_surface = pygame.image.load("python/Elements/Background.png").convert()
resized_base = pygame.transform.scale(base_surface, (800, 400))
# ================= MENU POSTER =================
menu_bg = pygame.image.load("python/Elements/MainMenu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (800, 400))


# ================= ENTITIES =================
rider = RiderIdle(100, 300)
rider.health = 100
rider.max_health = 100

cyborg = CyborgEnemy(500, 300)

all_sprites = pygame.sprite.Group()
all_sprites.add(rider)
all_sprites.add(cyborg)

# ================= XP =================
rider_xp = 0
rider_xp_max = 100
super_ready = False


# GAME STATE 
game_state = "menu"

menu_options = ["Controls", "Start Game"]
menu_index = 0
end_result = None   # "victory" or "defeat"



TUTORIAL_BGM = "Python/BackgroundMusic/cyberpunk.mp3"
GAME_BGM = "Python/BackgroundMusic/cyberpunk_main.mp3"

pygame.mixer.music.load(TUTORIAL_BGM)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ================= RIDER REPLACEMENT =================
def replace_rider(new_rider):
    global rider

    old_health = rider.health
    old_max_health = rider.max_health

    for s in list(all_sprites):
        if isinstance(
            s,
            (RiderIdle, RiderMove, RiderJump, RiderAttack, RiderRunAttack, RiderSuperAttack)
        ):
            all_sprites.remove(s)

    new_rider.health = old_health
    new_rider.max_health = old_max_health

    rider = new_rider
    all_sprites.add(rider)
    return rider

# ================= UI =================
def draw_health_bar(surface, x, y, width, height, current, maximum):
    ratio = current / maximum
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))

def draw_xp_bar(surface, x, y, width, height, current, maximum):
    ratio = current / maximum
    pygame.draw.rect(surface, (40, 40, 40), (x, y, width, height))
    pygame.draw.rect(surface, (0, 120, 255), (x, y, width * ratio, height))

def draw_menu(surface):
    surface.blit(menu_bg, (0, 0))

    font = pygame.font.SysFont("arial", 26, bold=True)

    start_y = 260
    for i, option in enumerate(menu_options):
        color = (0, 255, 255) if i == menu_index else (200, 200, 200)
        prefix = "> " if i == menu_index else "  "
        text = font.render(prefix + option, True, color)
        surface.blit(text, (300, start_y + i * 40))

def draw_controls(surface):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 22)
    title_font = pygame.font.SysFont("arial", 28, bold=True)

    surface.blit(
        title_font.render("CONTROLS", True, (0, 200, 255)),
        (330, 50)
    )

    lines = [
        "A / D        - Move",
        "SPACE        - Jump",
        "Left Click   - Attack",
        "Left + Move  - Run Attack",
        "Right Click - Super Attack (XP Full)",
        "",
        "Enemy is automated (AI-controlled)",
        "",
        "Press ESC to go back"
    ]

    y = 120
    for line in lines:
        surface.blit(font.render(line, True, (0, 255, 0)), (200, y))
        y += 30

def draw_end_screen(surface, result):
    surface.fill((0, 0, 0))

    title_font = pygame.font.SysFont("arial", 42, bold=True)
    font = pygame.font.SysFont("arial", 22)

    title_text = "VICTORY" if result == "victory" else "DEFEAT"
    title_color = (0, 255, 0) if result == "victory" else (255, 0, 0)

    surface.blit(
        title_font.render(title_text, True, title_color),
        (300, 130)
    )

    surface.blit(
        font.render("Press ENTER to return to Main Menu", True, (200, 200, 200)),
        (210, 200)
    )

    surface.blit(
        font.render("Press ESC to Exit", True, (200, 200, 200)),
        (300, 240)
    )




#  MAIN LOOP 
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ===== MENU INPUT =====
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[menu_index] == "Controls":
                        game_state = "controls"
                    elif menu_options[menu_index] == "Start Game":
                        game_state = "game"
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(GAME_BGM)
                        pygame.mixer.music.play(-1)

        # ===== CONTROLS INPUT =====
        elif game_state == "controls":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "menu"

        # ===== GAME INPUT =====
        elif game_state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if isinstance(rider, RiderMove) and not isinstance(rider, RiderRunAttack):
                    rider = replace_rider(
                        RiderRunAttack(rider.rect.x, rider.rect.y, rider.facing_left)
                    )
                elif rider.on_ground and not isinstance(rider, RiderAttack):
                    rider = replace_rider(
                        RiderAttack(rider.rect.x, rider.rect.y, rider.facing_left)
                    )

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if super_ready and not isinstance(rider, RiderSuperAttack):
                    rider = replace_rider(
                        RiderSuperAttack(rider.rect.x, rider.rect.y, rider.facing_left)
                    )
                    rider_xp = 0
                    super_ready = False

        elif game_state == "end":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rider.health = rider.max_health
                    cyborg.health = cyborg.max_health
                    rider_xp = 0
                    super_ready = False

                    rider = replace_rider(RiderIdle(100, 300))
                    cyborg.rect.x = 500

                    end_result = None
                    game_state = "menu"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


    # ===== DRAW MENU =====
    if game_state == "menu":
        draw_menu(screen)
        pygame.display.update()
        clock.tick(50)
        continue

    # ===== DRAW CONTROLS =====
    if game_state == "controls":
        draw_controls(screen)
        pygame.display.update()
        clock.tick(50)
        continue

    # ===== DRAW END SCREEN =====
    if game_state == "end":
        draw_end_screen(screen, end_result)
        pygame.display.update()
        clock.tick(50)
        continue


    # ================= GAME LOGIC =================

    if isinstance(rider, RiderIdle):
        if keys[pygame.K_a] or keys[pygame.K_d]:
            rider = replace_rider(
                RiderMove(
                    rider.rect.x,
                    rider.rect.y,
                    facing_left=keys[pygame.K_a],
                    vel_y=rider.vel_y,
                    on_ground=rider.on_ground
                )
            )
        elif keys[pygame.K_SPACE] and rider.on_ground:
            rider = replace_rider(
                RiderJump(rider.rect.x, rider.rect.y, rider.facing_left)
            )

    elif isinstance(rider, RiderMove):
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            rider = replace_rider(
                RiderIdle(rider.rect.x, rider.rect.y, rider.facing_left, 0, True)
            )
        elif keys[pygame.K_SPACE] and rider.on_ground:
            rider = replace_rider(
                RiderJump(rider.rect.x, rider.rect.y, rider.facing_left)
            )

    # ================= JUMP LANDING FIX =================
    if isinstance(rider, RiderJump) and rider.on_ground:
        rider = replace_rider(
            RiderIdle(
                rider.rect.x,
                rider.rect.y,
                rider.facing_left,
                0,
                True
            )
        )


    if isinstance(rider, (RiderAttack, RiderRunAttack, RiderSuperAttack)):
        if getattr(rider, "attack_finished", False):
            rider = replace_rider(
                RiderIdle(rider.rect.x, rider.rect.y, rider.facing_left, 0, True)
            )

    cyborg.update_ai(rider)

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

    if cyborg.state == "attack" and not cyborg.hit_done and rider_body:
        if cyborg_body.colliderect(rider_body):
            rider.health -= cyborg.damage
            cyborg.hit_done = True
            CYBORG_SFX.play()

    # ================= END CONDITIONS =================
    if game_state == "game":
        if cyborg.health <= 0:
            end_result = "victory"
            game_state = "end"

            pygame.mixer.music.stop()
            pygame.mixer.music.load(TUTORIAL_BGM)
            pygame.mixer.music.play(-1)

        elif rider.health <= 0:
            end_result = "defeat"
            game_state = "end"

            pygame.mixer.music.stop()
            pygame.mixer.music.load(TUTORIAL_BGM)
            pygame.mixer.music.play(-1)


    all_sprites.update(keys)

    screen.blit(resized_base, (0, 0))
    all_sprites.draw(screen)

    draw_health_bar(screen, 20, 20, 200, 15, rider.health, rider.max_health)
    draw_health_bar(screen, 580, 20, 200, 15, cyborg.health, cyborg.max_health)
    draw_xp_bar(screen, 20, 38, 200, 6, rider_xp, rider_xp_max)

    pygame.display.update()
    clock.tick(50)

