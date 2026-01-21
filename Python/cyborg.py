import pygame

GROUND_Y = 395


class CyborgEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ===== STATS =====
        self.health = 180
        self.max_health = 180

        # ===== DAMAGE =====
        self.punch_damage = 12
        self.kick_damage = 15
        self.super_damage = 22
        self.damage = self.punch_damage

        # ===== MOVEMENT =====
        self.speed = 3
        self.attack_range = 70
        self.stop_distance = 10

        # ===== STATE =====
        self.state = "run"
        self.facing_left = False

        # ===== ATTACK =====
        self.attack_timer = 0
        self.attack_cooldown = 35
        self.hit_done = False
        self.attack_locked_x = None

        self.attack_type = "punch"
        self.attack_count = 0
        self.super_every = 10  # 1 in 10 attacks

        # ===== ANIMATION =====
        self.counter = 0
        self.anim_speed = 0.28

        # ===== LOAD SPRITES SAFELY =====
        self.run_right = self._load_strip("python/Elements/Cyborg_run.png")
        self.run_left = [pygame.transform.flip(f, True, False) for f in self.run_right]

        self.punch_right = self._load_strip("python/Elements/Cyborg_attack2.png")
        self.punch_left = [pygame.transform.flip(f, True, False) for f in self.punch_right]

        self.kick_right = self._load_strip("python/Elements/Cyborg_kick.png")
        self.kick_left = [pygame.transform.flip(f, True, False) for f in self.kick_right]

        self.super_right = self._load_strip("python/Elements/Cyborg_attack3.png")
        self.super_left = [pygame.transform.flip(f, True, False) for f in self.super_right]

        self.image = self.run_right[0]
        self.rect = self.image.get_rect(midbottom=(x, GROUND_Y))

    def _load_strip(self, path, frame_width=48):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        count = sheet.get_width() // frame_width

        for i in range(count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_width))
            frames.append(pygame.transform.scale(frame, (96, 96)))

        return frames

    def get_hitbox(self):
        return pygame.Rect(
            self.rect.centerx - 22,
            self.rect.bottom - 75,
            44,
            75
        )

    def update_ai(self, rider):
        dx = rider.rect.centerx - self.rect.centerx
        distance = abs(dx)
        self.facing_left = dx < 0

        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.state != "attack" and distance <= self.attack_range and self.attack_timer == 0:
            self.state = "attack"
            self.counter = 0
            self.hit_done = False
            self.attack_locked_x = self.rect.x

            self.attack_count += 1
            if self.attack_count >= self.super_every:
                self.attack_type = "super"
                self.damage = self.super_damage
                self.attack_count = 0
            else:
                self.attack_type = "punch" if self.attack_count % 2 else "kick"
                self.damage = self.punch_damage if self.attack_type == "punch" else self.kick_damage
            return

        if self.state != "attack" and distance > self.stop_distance:
            self.rect.x += self.speed if dx > 0 else -self.speed

    def update(self, *_):
        if self.state == "attack" and self.attack_locked_x is not None:
            self.rect.x = self.attack_locked_x

        self.counter += self.anim_speed

        if self.state == "attack":
            if self.attack_type == "punch":
                frames = self.punch_left if self.facing_left else self.punch_right
            elif self.attack_type == "kick":
                frames = self.kick_left if self.facing_left else self.kick_right
            else:
                frames = self.super_left if self.facing_left else self.super_right
        else:
            frames = self.run_left if self.facing_left else self.run_right

        if self.counter >= len(frames):
            self.counter = 0
            if self.state == "attack":
                self.state = "run"
                self.attack_timer = self.attack_cooldown
                self.attack_locked_x = None

        self.image = frames[int(self.counter)]
        self.rect.bottom = GROUND_Y
