import pygame

class Player:
    def __init__(self, x, ground_y, width=30, height=40):
        self.initial_x = x
        self.ground_y = ground_y
        self.width = width
        self.height = height
        self.x = x
        self.y = ground_y - height
        self.vy = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.on_ground = True
        self.anim_tick = 0

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
            return True
        return False

    def update(self):
        self.vy += self.gravity
        self.y += self.vy

        ground_level = self.ground_y - self.height
        if self.y >= ground_level:
            self.y = ground_level
            self.vy = 0
            self.on_ground = True

        if self.on_ground:
            self.anim_tick += 1

    def reset(self):
        self.x = self.initial_x
        self.y = self.ground_y - self.height
        self.vy = 0
        self.on_ground = True
        self.anim_tick = 0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def render(self, screen):
        px = int(self.x)
        py = int(self.y)
        w = int(self.width)
        h = int(self.height)

        # Colors
        SKIN = (255, 205, 160)
        SHIRT = (40, 120, 220)
        PANTS = (30, 45, 75)
        HEADBAND = (235, 60, 60)
        EYE = (20, 20, 20)

        # Head (top 12px)
        head_rect = pygame.Rect(px + 4, py, w - 8, 12)
        pygame.draw.rect(screen, SKIN, head_rect, border_radius=3)
        # Headband
        pygame.draw.rect(screen, HEADBAND, (px + 4, py + 2, w - 8, 3))
        # Eye looking forward
        pygame.draw.rect(screen, EYE, (px + w - 7, py + 5, 2, 2))

        # Body / Shirt (middle 16px)
        body_rect = pygame.Rect(px + 2, py + 12, w - 4, 16)
        pygame.draw.rect(screen, SHIRT, body_rect, border_radius=2)

        # Legs / Pants (bottom 12px)
        leg_y = py + 28
        leg_h = 12
        if self.on_ground:
            # Alternating running stride animation
            stride = (self.anim_tick // 5) % 2
            if stride == 0:
                pygame.draw.rect(screen, PANTS, (px + 3, leg_y, 8, leg_h))
                pygame.draw.rect(screen, PANTS, (px + w - 11, leg_y, 8, leg_h - 3))
            else:
                pygame.draw.rect(screen, PANTS, (px + 3, leg_y, 8, leg_h - 3))
                pygame.draw.rect(screen, PANTS, (px + w - 11, leg_y, 8, leg_h))
        else:
            # Tucked legs during jump
            pygame.draw.rect(screen, PANTS, (px + 4, leg_y, 9, 8))
            pygame.draw.rect(screen, PANTS, (px + 15, leg_y - 2, 9, 8))
