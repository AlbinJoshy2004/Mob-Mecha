import pygame
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class RiderSuperAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left=False):
        super().__init__()

        self.health = 120
        self.max_health = 120

        self.state = "super_attack"
        self.facing_left = facing_left
        self.on_ground = True
        self.vel_y = 0

        self.attack_finished = False
        self.damage = 20   # BIG DAMAGE
        self.hit_done = False

        self.active_start = 2
        self.active_end = 6   # longer active window

        self.sprite_sheet = pygame.image.load(resource_path(
            "Elements/Biker_attack3.png"
        )).convert_alpha()

        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 8

        self.frames_right = []
        self.frames_left = []

        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            frame = pygame.transform.scale(
                frame, (self.frame_width * 2, self.frame_height * 2)
            )
            self.frames_right.append(frame)

        self.frames_left = [
            pygame.transform.flip(f, True, False) for f in self.frames_right
        ]

        self.frames = self.frames_left if self.facing_left else self.frames_right

        self.counter = 0
        self.animation_speed = 0.4
        self.current_frame = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys=None):
        self.counter += self.animation_speed

        if self.counter >= len(self.frames):
            self.attack_finished = True
            self.counter = len(self.frames) - 1

        self.current_frame = int(self.counter)
        self.frames = self.frames_left if self.facing_left else self.frames_right
        self.image = self.frames[self.current_frame]

    def is_active(self):
        return self.active_start <= int(self.counter) <= self.active_end

    def get_damage_box(self):
        width = 60     # WIDER RANGE
        height = 50
        y_offset = 10

        if self.facing_left:
            return pygame.Rect(
                self.rect.left - width,
                self.rect.top + y_offset,
                width,
                height
            )
        else:
            return pygame.Rect(
                self.rect.right,
                self.rect.top + y_offset,
                width,
                height
            )

    def get_body_hitbox(self):
        # Rider cannot be hit in air
        if not self.on_ground:
            return None

        # Grounded hitbox (legs + torso only)
        width = 26
        height = 40

        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height

        return pygame.Rect(x, y, width, height)


