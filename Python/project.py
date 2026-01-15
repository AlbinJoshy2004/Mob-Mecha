import pygame
from rider_ import RiderIdle
from rider_move import RiderMove
from Rider_Jump import RiderJump
from RiderAttack import RiderAttack
from cyborg import CyborgEnemy
from rider_run_attack import RiderRunAttack


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MOB MECHA")
clock = pygame.time.Clock()

base_surface = pygame.image.load("python/Elements/Background.png").convert() 
resized_base = pygame.transform.scale(base_surface, (800, 400))

rider = RiderIdle(100, 300)
all_sprites = pygame.sprite.Group(rider)
cyborg = CyborgEnemy(500, 300)
all_sprites.add(cyborg)


def replace_rider(new_rider):
    for s in list(all_sprites):
        if isinstance(
            s,
            (RiderIdle, RiderMove, RiderJump, RiderAttack, RiderRunAttack)
        ):
            all_sprites.remove(s)

    all_sprites.add(new_rider)
    return new_rider


def draw_health_bar(surface, x, y, width, height, current, maximum):
    ratio = current / maximum
    (surface, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))



while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if isinstance(rider, RiderMove) and not isinstance(rider, RiderRunAttack):
                rider = replace_rider(RiderRunAttack(rider.rect.x,rider.rect.y,facing_left=rider.facing_left ))

            elif rider.on_ground and not isinstance(rider, RiderAttack):
                rider = replace_rider(RiderAttack(rider.rect.x,rider.rect.y,facing_left=rider.facing_left))
 
   

    old_x, old_y = rider.rect.x, rider.rect.y
    facing_left = getattr(rider, "facing_left", False)
    vel_y = getattr(rider, "vel_y", 0)
    on_ground = getattr(rider, "on_ground", True)

    if keys[pygame.K_SPACE] and on_ground and not isinstance(rider, RiderAttack):
        rider = replace_rider(RiderJump(old_x, old_y, facing_left=facing_left, vel_y=-12, on_ground=False))

    elif (keys[pygame.K_a] or keys[pygame.K_d]) and isinstance(rider, RiderIdle):
        rider = replace_rider(RiderMove(old_x, old_y, facing_left=facing_left, vel_y=vel_y, on_ground=on_ground))

    elif not (keys[pygame.K_a] or keys[pygame.K_d]) and isinstance(rider, RiderMove):
        rider = replace_rider(RiderIdle(old_x, old_y, facing_left=facing_left, vel_y=0, on_ground=True))

    all_sprites.update(keys)
    if isinstance(rider, (RiderAttack, RiderRunAttack)) and rider.is_active():
        damage_box = rider.get_damage_box()
        cyborg_hitbox = cyborg.get_hitbox()

        in_front = (
        (not rider.facing_left and cyborg_hitbox.left >= rider.rect.centerx) or
        (rider.facing_left and cyborg_hitbox.right <= rider.rect.centerx)
        )

        if in_front and damage_box.colliderect(cyborg_hitbox) and not rider.hit_done:
            cyborg.health -= rider.damage
            rider.hit_done = True



    if isinstance(rider, RiderJump) and rider.on_ground:
        rider = replace_rider(RiderIdle(rider.rect.x, rider.rect.y, facing_left=rider.facing_left))

    if isinstance(rider, RiderRunAttack) and rider.attack_finished:
        rider = replace_rider(RiderIdle(rider.rect.x,rider.rect.y,facing_left=rider.facing_left,vel_y=0,on_ground=True))

    if isinstance(rider, RiderAttack) and rider.attack_finished:
        rider = replace_rider(RiderIdle(rider.rect.x,rider.rect.y,facing_left=rider.facing_left,vel_y=0,on_ground=True))



    screen.fill((0, 0, 0))
    screen.blit(resized_base, (0, 0))
    all_sprites.draw(screen)

    draw_health_bar(screen, 20, 20, 200, 15, rider.health, rider.max_health)
    draw_health_bar(screen, 580, 20, 200, 15, cyborg.health, cyborg.max_health)

    pygame.display.update()
    clock.tick(50)
