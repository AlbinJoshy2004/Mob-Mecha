import pygame

class CyborgEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.health = 150
        self.max_health = 150
        self.sprite_sheet = pygame.image.load("python/Elements/Cyborg_idle.png").convert_alpha()
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

        self.frames = self.frames_left

        self.counter = 0
        self.animation_speed = 0.12
        self.current_frame = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys=None):
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0

        self.current_frame = int(self.counter)
        self.image = self.frames[self.current_frame]
    
    def get_hitbox(self):
        width = 40
        height = 70
        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)



