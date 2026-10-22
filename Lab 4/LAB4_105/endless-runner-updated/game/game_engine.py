import math
import random
import pygame
from .player import Player
from .obstacle import Obstacle
from .sound_manager import SoundManager

# Palette
SKY = (195, 220, 245)
GROUND_BROWN = (120, 80, 45)
GRASS_GREEN = (70, 160, 60)
WHITE = (255, 255, 255)
BLACK = (20, 25, 30)
GOLD = (255, 215, 0)
DARK_GRAY = (40, 45, 55)
CARD_BG = (30, 40, 55)
OVERLAY_BG = (10, 20, 30, 205)
BTN_GREEN = (45, 175, 75)
BTN_GREEN_HOVER = (60, 205, 95)
ACCENT_BLUE = (70, 150, 240)

DIFFICULTIES = {
    "Easy": {"speed": 5.0, "interval": 85, "ramp": 0.0015, "max_speed": 11.0},
    "Medium": {"speed": 7.0, "interval": 65, "ramp": 0.003, "max_speed": 14.0},
    "Hard": {"speed": 9.0, "interval": 50, "ramp": 0.005, "max_speed": 16.5},
}

STATE_START = "START"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"

STUDENT_SRN = "PES1UG24AM105"

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 45

        # Ensure pygame font is initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # Sounds
        self.sound = SoundManager()

        # Difficulty setup
        self.current_difficulty = "Medium"
        self._apply_difficulty(self.current_difficulty)

        # Entities
        self.player = Player(90, self.ground_y)
        self.obstacles = []
        self._spawn_timer = 0
        self.ground_offset = 0.0

        # Clouds for visual parallax
        self.clouds = [
            {"x": 120, "y": 60, "speed": 0.8, "size": 38},
            {"x": 380, "y": 45, "speed": 0.6, "size": 48},
            {"x": 650, "y": 70, "speed": 0.9, "size": 34},
        ]

        # States: START -> PLAYING -> GAME_OVER
        self.state = STATE_START
        self.game_over = False
        self.should_quit = False

        # Scoring
        self.score = 0
        self.high_score = 0
        self.distance = 0.0

        # UI Interactive Buttons on Virtual Canvas (800 x 400)
        self.start_btn_rect = pygame.Rect(300, 230, 200, 52)
        self.diff_btn_rects = {
            "Easy": pygame.Rect(235, 175, 100, 36),
            "Medium": pygame.Rect(350, 175, 100, 36),
            "Hard": pygame.Rect(465, 175, 100, 36)
        }

        # Fonts
        self.font_score = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_badge = pygame.font.SysFont("Arial", 14, bold=True)

    def _apply_difficulty(self, diff_name):
        config = DIFFICULTIES.get(diff_name, DIFFICULTIES["Medium"])
        self.current_difficulty = diff_name
        self.starting_speed = config["speed"]
        self.speed = config["speed"]
        self.spawn_interval = config["interval"]
        self.speed_ramp = config["ramp"]
        self.max_speed = config["max_speed"]

    def start_game(self):
        """Starts a fresh gameplay run."""
        self.state = STATE_PLAYING
        self.game_over = False
        self.player.reset()
        self.player.jump() # Start with an energetic hop
        self.obstacles = []
        self._spawn_timer = 0
        self.speed = self.starting_speed
        self.score = 0
        self.distance = 0.0
        self.sound.play_jump()

    def reset(self, difficulty="Medium"):
        """Task 3: Resets game state with chosen difficulty."""
        self._apply_difficulty(difficulty)
        self.start_game()

    def handle_event(self, event, mouse_pos=None):
        m_pos = mouse_pos if mouse_pos is not None else getattr(event, "pos", (0, 0))

        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        # 1. START Screen Events
        if self.state == STATE_START:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._apply_difficulty("Easy")
                elif event.key == pygame.K_2:
                    self._apply_difficulty("Medium")
                elif event.key == pygame.K_3:
                    self._apply_difficulty("Hard")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP, pygame.K_w):
                    self.start_game()
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.should_quit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check difficulty button clicks
                clicked_diff = False
                for diff_name, rect in self.diff_btn_rects.items():
                    if rect.collidepoint(m_pos):
                        self._apply_difficulty(diff_name)
                        clicked_diff = True
                        break

                if not clicked_diff:
                    if self.start_btn_rect.collidepoint(m_pos) or m_pos[1] > 120:
                        self.start_game()

        # 2. PLAYING State Events
        elif self.state == STATE_PLAYING:
            if (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w)) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if self.player.jump():
                    # Task 4: Sound on jump
                    self.sound.play_jump()

        # 3. GAME OVER State Events
        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.reset("Easy")
                elif event.key == pygame.K_2:
                    self.reset("Medium")
                elif event.key == pygame.K_3:
                    self.reset("Hard")
                elif event.key in (pygame.K_SPACE, pygame.K_r, pygame.K_RETURN):
                    self.reset(self.current_difficulty)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.should_quit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.reset(self.current_difficulty)

    def handle_input(self):
        pass

    def trigger_game_over(self):
        """Task 2 & 4: Game Over condition, high score recording, sound feedback."""
        if self.state == STATE_PLAYING:
            self.state = STATE_GAME_OVER
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            # Task 4: Death / hit sound feedback
            self.sound.play_hit()
            print(f"Game Over! Final Score: {self.score} | Student: {STUDENT_SRN}")

    def update(self):
        # Update clouds for alive background feeling
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -80:
                cloud["x"] = self.width + random.randint(20, 100)
                cloud["y"] = random.randint(30, 90)

        if self.state == STATE_START:
            self.player.update()
            return

        if self.state == STATE_GAME_OVER:
            return

        # Task 1 Fix: Ramp speed progressively but cap at max_speed to avoid breaking physics
        if self.speed < self.max_speed:
            self.speed = min(self.max_speed, self.speed + self.speed_ramp)

        self.player.update()
        self.distance += self.speed
        self.ground_offset = (self.ground_offset + self.speed) % 30

        # Spawn obstacles with safe interval
        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            # Slight random width / height variance for variety
            w = random.choice([24, 28, 32])
            h = random.choice([38, 42, 46])
            self.obstacles.append(Obstacle(self.width, self.ground_y, self.speed, width=w, height=h))

        # Update obstacles and perform continuous swept collision detection
        for obstacle in self.obstacles:
            obstacle.speed = self.speed
            obstacle.move()

            # Task 1 Fix: Swept continuous collision detection eliminates tunneling
            if obstacle.collides_with_player(self.player):
                self.trigger_game_over()
                return

            # Score counting when obstacle cleared safely
            if not obstacle.scored and (obstacle.x + obstacle.width < self.player.x):
                obstacle.scored = True
                self.score += 1
                # Task 4: Sound effect on scoring
                self.sound.play_score()

        # Clean up off-screen obstacles
        self.obstacles = [o for o in self.obstacles if not o.off_screen()]

    def render(self, screen, mouse_pos=(0, 0)):
        # 1. Sky
        screen.fill(SKY)

        # 2. Clouds
        for cloud in self.clouds:
            cx, cy, sz = int(cloud["x"]), int(cloud["y"]), cloud["size"]
            pygame.draw.circle(screen, WHITE, (cx, cy), sz // 2)
            pygame.draw.circle(screen, WHITE, (cx + sz // 3, cy - 4), sz // 2)
            pygame.draw.circle(screen, WHITE, (cx + sz * 2 // 3, cy), sz // 3)

        # 3. Ground
        ground_rect = pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y)
        pygame.draw.rect(screen, GROUND_BROWN, ground_rect)
        pygame.draw.rect(screen, GRASS_GREEN, (0, self.ground_y, self.width, 8))
        pygame.draw.line(screen, (50, 110, 40), (0, self.ground_y), (self.width, self.ground_y), 2)

        # Moving ground texture dashes
        for x in range(-int(self.ground_offset), self.width + 30, 30):
            pygame.draw.line(screen, (95, 65, 35), (x, self.ground_y + 16), (x + 14, self.ground_y + 16), 2)
            pygame.draw.line(screen, (85, 55, 28), (x + 10, self.ground_y + 26), (x + 22, self.ground_y + 26), 2)

        # 4. Obstacles
        for obstacle in self.obstacles:
            obstacle.render(screen)

        # 5. Player
        self.player.render(screen)

        # 6. Render based on active state
        if self.state == STATE_START:
            self._render_start_screen(screen, mouse_pos)
        elif self.state == STATE_PLAYING:
            self._render_hud(screen)
        elif self.state == STATE_GAME_OVER:
            self._render_hud(screen)
            self._render_game_over_screen(screen)

    def _render_hud(self, screen):
        # Score & High Score
        score_surf = self.font_score.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_surf, (18, 14))

        best_surf = self.font_small.render(f"Best: {self.high_score}", True, (50, 50, 60))
        screen.blit(best_surf, (18, 44))

        # Speedometer & Mode
        speed_txt = self.font_small.render(f"Speed: {self.speed:.1f}x ({self.current_difficulty})", True, (40, 50, 70))
        screen.blit(speed_txt, (self.width - speed_txt.get_width() - 18, 14))

        # Student SRN badge
        srn_txt = self.font_badge.render(f"SRN: {STUDENT_SRN}", True, (60, 80, 120))
        screen.blit(srn_txt, (self.width - srn_txt.get_width() - 18, 38))

    def _render_start_screen(self, screen, mouse_pos):
        # Title with drop shadow
        title = self.font_title.render("ENDLESS RUNNER", True, (30, 45, 75))
        shadow = self.font_title.render("ENDLESS RUNNER", True, (160, 190, 220))
        tx = (self.width - title.get_width()) // 2
        screen.blit(shadow, (tx + 3, 48))
        screen.blit(title, (tx, 45))

        # SRN Subtitle Banner
        srn_banner = self.font_medium.render(f"Lab 4 Edition  •  SRN: {STUDENT_SRN}", True, (50, 80, 130))
        screen.blit(srn_banner, ((self.width - srn_banner.get_width()) // 2, 105))

        # Difficulty Selector Buttons
        diff_label = self.font_small.render("Select Difficulty:", True, (40, 50, 70))
        screen.blit(diff_label, ((self.width - diff_label.get_width()) // 2, 148))

        for diff_name, rect in self.diff_btn_rects.items():
            is_active = (diff_name == self.current_difficulty)
            is_hover = rect.collidepoint(mouse_pos)
            bg_col = (45, 115, 200) if is_active else ((80, 110, 145) if is_hover else (50, 70, 95))
            border_col = GOLD if is_active else (180, 200, 225)

            pygame.draw.rect(screen, bg_col, rect, border_radius=8)
            pygame.draw.rect(screen, border_col, rect, width=2 if is_active else 1, border_radius=8)

            txt_col = GOLD if is_active else WHITE
            label = self.font_small.render(diff_name, True, txt_col)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        # Start Button
        is_btn_hover = self.start_btn_rect.collidepoint(mouse_pos)
        btn_col = BTN_GREEN_HOVER if is_btn_hover else BTN_GREEN
        pygame.draw.rect(screen, btn_col, self.start_btn_rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, self.start_btn_rect, width=2, border_radius=14)

        btn_txt = self.font_btn.render("▶ START GAME", True, WHITE)
        screen.blit(btn_txt, (self.start_btn_rect.centerx - btn_txt.get_width() // 2, self.start_btn_rect.centery - btn_txt.get_height() // 2))

        # Instructions Hint
        hint1 = self.font_small.render("Press [SPACE / W / UP] or Click to Start & Jump", True, (40, 50, 70))
        hint2 = self.font_small.render("Press [F11] to Toggle Fullscreen / Maximize", True, (80, 100, 130))
        screen.blit(hint1, ((self.width - hint1.get_width()) // 2, 305))
        screen.blit(hint2, ((self.width - hint2.get_width()) // 2, 335))

    def _render_game_over_screen(self, screen):
        # Darkened overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY_BG)
        screen.blit(overlay, (0, 0))

        # Central Modal Card
        card_w, card_h = 480, 280
        card_x = (self.width - card_w) // 2
        card_y = (self.height - card_h) // 2 - 10
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=16)
        pygame.draw.rect(screen, GOLD, card_rect, width=3, border_radius=16)

        # Title: GAME OVER
        title = self.font_title.render("GAME OVER", True, (255, 80, 80))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, card_y + 18))

        # Scores
        score_txt = self.font_medium.render(f"Final Score:  {self.score}", True, WHITE)
        best_txt = self.font_medium.render(f"Best Score:   {self.high_score}", True, GOLD)
        screen.blit(score_txt, (self.width // 2 - score_txt.get_width() // 2, card_y + 75))
        screen.blit(best_txt, (self.width // 2 - best_txt.get_width() // 2, card_y + 104))

        # Divider line
        pygame.draw.line(screen, (80, 100, 130), (card_x + 30, card_y + 140), (card_x + card_w - 30, card_y + 140), 2)

        # Replay / Difficulty Prompts
        diff_prompt = self.font_small.render("Choose Difficulty to Replay:", True, (180, 220, 255))
        screen.blit(diff_prompt, (self.width // 2 - diff_prompt.get_width() // 2, card_y + 152))

        diff_line = self.font_small.render("[1] Easy    •    [2] Medium    •    [3] Hard", True, (255, 230, 140))
        screen.blit(diff_line, (self.width // 2 - diff_line.get_width() // 2, card_y + 182))

        replay_line = self.font_small.render("[SPACE / R] Quick Replay      [Q] Exit", True, (200, 215, 235))
        screen.blit(replay_line, (self.width // 2 - replay_line.get_width() // 2, card_y + 214))

        srn_footer = self.font_badge.render(f"Candidate: {STUDENT_SRN}", True, (130, 155, 185))
        screen.blit(srn_footer, (self.width // 2 - srn_footer.get_width() // 2, card_y + 248))
