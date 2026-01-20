import pygame

GROUND_Y = 395


class CyborgEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ===== STATS =====
        self.health = 150
        self.max_health = 150
        self.damage = 15

        # ===== STATE =====
        self.state = "idle"     # idle | run | attack
        self.facing_left = True

        # ===== SPEED TUNING =====
        self.speed = 4                 # FASTER MOVEMENT
        self.chase_range = 220
        self.attack_range = 85

        # ===== ATTACK CONTROL =====
        self.hit_done = False
        self.attack_start = 3
        self.attack_end = 5

        self.attack_cooldown = 30   # frames
        self.attack_timer = 0


        # ===== ANIMATION =====
        self.counter = 0
        self.anim_speed = 0.25         # FASTER ATTACK ANIMATION

        # ===== IDLE =====
        idle_sheet = pygame.image.load("python/Elements/Cyborg_idle.png").convert_alpha()
        self.idle_right = []
        for i in range(4):
            f = idle_sheet.subsurface((i * 48, 0, 48, 48))
            self.idle_right.append(pygame.transform.scale(f, (96, 96)))
        self.idle_left = [pygame.transform.flip(f, True, False) for f in self.idle_right]

        # ===== RUN =====
        run_sheet = pygame.image.load("python/Elements/Cyborg_run.png").convert_alpha()
        self.run_right = []
        for i in range(6):
            f = run_sheet.subsurface((i * 48, 0, 48, 48))
            self.run_right.append(pygame.transform.scale(f, (96, 96)))
        self.run_left = [pygame.transform.flip(f, True, False) for f in self.run_right]

        # ===== ATTACK =====
        atk_sheet = pygame.image.load("python/Elements/Cyborg_attack2.png").convert_alpha()
        self.atk_right = []
        for i in range(8):
            f = atk_sheet.subsurface((i * 48, 0, 48, 48))
            self.atk_right.append(pygame.transform.scale(f, (96, 96)))
        self.atk_left = [pygame.transform.flip(f, True, False) for f in self.atk_right]

        # ===== SPRITE =====
        self.image = self.idle_right[0]
        self.rect = self.image.get_rect(midbottom=(x, GROUND_Y))

    # ===== BODY HITBOX =====
    def get_hitbox(self):
        width = 40
        height = 70
        x = self.rect.centerx - width // 2
        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)

    # ===== ATTACK HITBOX =====
    def get_attack_hitbox(self):
        width = 55
        height = 45

        if self.facing_left:
            x = self.rect.left - width
        else:
            x = self.rect.right

        y = self.rect.bottom - height
        return pygame.Rect(x, y, width, height)

    # ===== AI BRAIN =====
    def update_ai(self, rider):
        # Face rider
        self.facing_left = rider.rect.centerx < self.rect.centerx
        dist = abs(rider.rect.centerx - self.rect.centerx)

        if self.attack_timer > 0:
            self.attack_timer -= 1

        # Start attack (only once)
        if (
            self.state != "attack"
            and dist <= self.attack_range
            and self.attack_timer == 0
        ):
            self.state = "attack"
            self.counter = 0
            self.hit_done = False
            return


        # Chase
        if self.state != "attack":
            if dist < self.chase_range:
                self.state = "run"
                if self.facing_left:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed
            else:
                self.state = "idle"

    # ===== ANIMATION UPDATE =====
    def update(self, *_):
        self.counter += self.anim_speed

        if self.state == "attack":
            frames = self.atk_left if self.facing_left else self.atk_right
        elif self.state == "run":
            frames = self.run_left if self.facing_left else self.run_right
        else:
            frames = self.idle_left if self.facing_left else self.idle_right

        if self.counter >= len(frames):
            self.counter = 0
            if self.state == "attack":
                self.state = "idle"
                self.attack_timer=self.attack_cooldown

        self.image = frames[int(self.counter)]
        self.rect.bottom = GROUND_Y
