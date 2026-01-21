import pygame

class RiderJump(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left=False, vel_y=-15, on_ground=False):
        super().__init__()
        self.health = 120
        self.max_health = 120


        self.facing_left = facing_left
        self.vel_y = vel_y
        self.on_ground = on_ground
        self.gravity = 0.9
        self.state = "jump"

        self.air_speed = 10

        self.sprite_sheet = pygame.image.load("python/Elements/Biker_jump.png").convert_alpha()
        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 4

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
            self.frames_left.append(pygame.transform.flip(frame, True, False))

        self.frames = self.frames_left if self.facing_left else self.frames_right

        self.current_frame = 0
        self.animation_speed = 0.2
        self.counter = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys=None):
        if keys:
            if keys[pygame.K_a]:
                self.rect.x -= self.air_speed
                self.facing_left = True
            if keys[pygame.K_d]:
                self.rect.x += self.air_speed
                self.facing_left = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        ground_y = 300
        if self.rect.y >= ground_y:
            self.rect.y = ground_y
            self.vel_y = 0
            self.on_ground = True
            self.state = "idle"

        self.counter += self.animation_speed
        if self.counter >= len(self.frames_right):
            self.counter = len(self.frames_right) - 1

        self.current_frame = int(self.counter)
        self.frames = self.frames_left if self.facing_left else self.frames_right
        self.image = self.frames[self.current_frame]
