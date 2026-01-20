import pygame

class RiderAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left=False):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.active_start = 2
        self.active_end = 3


        self.state = "attack"
        self.facing_left = facing_left
        self.on_ground = True
        self.vel_y = 0
        self.attack_finished = False
        self.damage = 5
        self.hit_done = False

        self.sprite_sheet = pygame.image.load(
            "python/Elements/RiderAttack.png"
        ).convert_alpha()

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

        self.frames_left = [
            pygame.transform.flip(f, True, False) for f in self.frames_right
        ]

        self.frames = self.frames_left if self.facing_left else self.frames_right

        self.counter = 0
        self.animation_speed = 0.5
        self.current_frame = 0

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_damage_box(self):
        width = 18
        height = 30
        y_offset = 20
        x_offset = 6  

        if self.facing_left:
            return pygame.Rect(self.rect.left - width + x_offset,self.rect.top + y_offset,width,height)
        else:
            return pygame.Rect(self.rect.right - x_offset,self.rect.top + y_offset,width,height)
        
    def get_body_hitbox(self):
        width = 40
        height = 70
        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)




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

