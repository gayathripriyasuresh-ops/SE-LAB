import pygame

class Obstacle:
    def __init__(self, x, ground_y, speed, width=26, height=42):
        self.x = float(x)
        self.prev_x = float(x)
        self.width = width
        self.height = height
        self.y = ground_y - height
        self.speed = speed
        self.scored = False

    def move(self):
        self.prev_x = self.x
        self.x -= self.speed

    def off_screen(self):
        return (self.x + self.width) < -10

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def swept_rect(self):
        """
        Task 1 Fix: Swept-box covering the entire displacement of the obstacle
        between the previous frame and current frame.
        Prevents high-speed tunneling past the player.
        """
        left = min(self.x, self.prev_x)
        right = max(self.x + self.width, self.prev_x + self.width)
        return pygame.Rect(int(left), int(self.y), int(right - left), int(self.height))

    def collides_with_player(self, player):
        """
        Task 1 Fix: Continuous Collision Detection (CCD).
        Checks both current frame AABB intersection and swept horizontal path
        intersection against the player's vertical profile.
        """
        p_rect = player.rect()

        # 1. Direct instantaneous collision
        if self.rect().colliderect(p_rect):
            return True

        # 2. Continuous swept path collision (prevents tunneling through the player)
        swept = self.swept_rect()
        if swept.colliderect(p_rect):
            # Verify vertical overlap exists during path intersection
            vertical_overlap = (player.y + player.height > self.y) and (player.y < self.y + self.height)
            if vertical_overlap:
                return True

        return False

    def render(self, screen):
        ox = int(self.x)
        oy = int(self.y)
        w = int(self.width)
        h = int(self.height)

        # Draw stylized cactus / hurdle obstacle
        OBSTACLE_DARK = (25, 95, 30)
        OBSTACLE_LIGHT = (45, 155, 55)
        SPINE_COL = (15, 60, 20)

        # Main stem
        main_rect = pygame.Rect(ox + 4, oy, w - 8, h)
        pygame.draw.rect(screen, OBSTACLE_DARK, main_rect, border_radius=4)
        pygame.draw.rect(screen, OBSTACLE_LIGHT, (ox + 6, oy + 2, 4, h - 4))

        # Left branch
        b1_y = oy + 12
        pygame.draw.rect(screen, OBSTACLE_DARK, (ox - 1, b1_y, 6, 4))
        pygame.draw.rect(screen, OBSTACLE_DARK, (ox - 1, b1_y - 8, 4, 10), border_radius=2)

        # Right branch
        b2_y = oy + 16
        pygame.draw.rect(screen, OBSTACLE_DARK, (ox + w - 5, b2_y, 6, 4))
        pygame.draw.rect(screen, OBSTACLE_DARK, (ox + w - 3, b2_y - 8, 4, 10), border_radius=2)

        # Hazard needles / spikes
        for sy in range(oy + 6, oy + h - 6, 8):
            pygame.draw.line(screen, SPINE_COL, (ox + 2, sy), (ox + 4, sy), 1)
            pygame.draw.line(screen, SPINE_COL, (ox + w - 4, sy + 3), (ox + w - 2, sy + 3), 1)
