import pygame

class RiderMove(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left=False, vel_y=0, on_ground=True):
        super().__init__()
        self.health = 5
        self.max_health = 5
        self.on_ground = on_ground
        self.vel_y = vel_y
        self.state = "run"
        self.speed = 8
        self.facing_left = facing_left

        self.sprite_sheet = pygame.image.load("python/Elements/Biker_run.png").convert_alpha()
        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 6

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
        self.animation_speed = 0.15
        self.counter = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys=None):
        moving_left = moving_right = False

        if keys:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                moving_left = True
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                moving_right = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

        self.counter += self.animation_speed
        if self.counter >= len(self.frames_right):
            self.counter = 0
        self.current_frame = int(self.counter)

        if moving_left:
            self.facing_left = True
        elif moving_right:
            self.facing_left = False

        self.frames = self.frames_left if self.facing_left else self.frames_right
        self.image = self.frames[self.current_frame]
