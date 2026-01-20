import pygame
GROUND_Y = 395



class CyborgEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ================= BASIC STATS =================
        self.health = 150
        self.max_health = 150

        # ================= ANIMATION =================
        self.counter = 0
        self.animation_speed = 0.2
        self.current_frame = 0

        # ================= IDLE ANIMATION =================
        idle_sheet = pygame.image.load(
            "python/Elements/Cyborg_idle.png"
        ).convert_alpha()

        self.frames_right = []
        for i in range(4):
            frame = idle_sheet.subsurface((i * 48, 0, 48, 48))
            frame = pygame.transform.scale(frame, (96, 96))
            self.frames_right.append(frame)

        self.frames_left = [
            pygame.transform.flip(f, True, False) for f in self.frames_right
        ]

        # ================= RUN ANIMATION =================
        run_sheet = pygame.image.load(
            "python/Elements/Cyborg_run.png"
        ).convert_alpha()

        self.run_frames_right = []
        self.run_frames_left = []

        for i in range(6):
            frame = run_sheet.subsurface((i * 48, 0, 48, 48))
            frame = pygame.transform.scale(frame, (96, 96))
            self.run_frames_right.append(frame)
            self.run_frames_left.append(pygame.transform.flip(frame, True, False))

        # ================= SPRITE SETUP =================
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect(midbottom=(x, GROUND_Y))

        # ================= AI STATE =================
        self.state = "idle"      # idle | run
        self.facing_left = True

        self.speed = 2           # heavy movement
        self.chase_range = 200   # when to start chasing

    # ================= BODY HITBOX =================
    def get_hitbox(self):
        width = 40
        height = 70
        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)

    # ================= AI BRAIN =================
    def update_ai(self, rider):
        # Face rider
        if rider.rect.centerx < self.rect.centerx:
            self.facing_left = True
        else:
            self.facing_left = False

        # Distance check
        distance = abs(rider.rect.centerx - self.rect.centerx)

        if distance < self.chase_range:
            self.state = "run"
        else:
            self.state = "idle"

        # Move toward rider
        if self.state == "run":
            if self.facing_left:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

    # ================= ANIMATION UPDATE =================
    def update(self, keys=None):
        # SAVE FEET POSITION (CRITICAL FIX)
        bottom = self.rect.bottom
        centerx = self.rect.centerx

        self.counter += self.animation_speed

        if self.state == "run":
            frames = self.run_frames_left if self.facing_left else self.run_frames_right
        else:
            frames = self.frames_left if self.facing_left else self.frames_right

        if self.counter >= len(frames):
            self.counter = 0

        self.current_frame = int(self.counter)
        self.image = frames[self.current_frame]

        self.rect.bottom = GROUND_Y


        
