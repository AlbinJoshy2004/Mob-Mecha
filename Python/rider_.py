import pygame

class RiderIdle(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left=False, vel_y=0, on_ground=True):
        super().__init__()
        self.health = 100
        self.max_health = 100
        # shared variables
        self.on_ground = on_ground
        self.vel_y = vel_y
        self.state = "idle"
        self.speed = 5
        self.facing_left = facing_left

        # load sheet
        self.sprite_sheet = pygame.image.load("python/Elements/Biker_idle.png").convert_alpha()

        self.frame_width = 48
        self.frame_height = 48
        self.num_frames = 4

        # load frames once for both directions
        self.frames_right = []
        self.frames_left = []
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            frame = pygame.transform.scale(frame, (self.frame_width * 2, self.frame_height * 2))
            self.frames_right.append(frame)
            self.frames_left.append(pygame.transform.flip(frame, True, False))

        # current frames reference
        self.frames = self.frames_left if self.facing_left else self.frames_right

        self.current_frame = 0
        self.animation_speed = 0.15
        self.counter = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_body_hitbox(self):
        width = 40
        height = 70
        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)


    def update(self, keys=None):
        # animate
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0

        # ensure correct frame list for direction
        self.frames = self.frames_left if self.facing_left else self.frames_right
        self.current_frame = int(self.counter)
        self.image = self.frames[self.current_frame]
