import sys
import pygame
from game.game_engine import GameEngine, STUDENT_SRN

# Initialize pygame
pygame.init()

# Base virtual dimensions for game logic
VIRTUAL_WIDTH = 800
VIRTUAL_HEIGHT = 400

# Create resizable window (enables Windows Maximize button on the title bar)
window = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(f"Endless Runner - {STUDENT_SRN} (Pygame Enhanced)")

# Virtual surface where game rendering takes place
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine instance
engine = GameEngine(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)

def get_scale_and_offset(win_w, win_h):
    """Calculates scaling factor and letterbox offsets to preserve 800x400 aspect ratio."""
    scale = min(win_w / VIRTUAL_WIDTH, win_h / VIRTUAL_HEIGHT)
    scaled_w = int(VIRTUAL_WIDTH * scale)
    scaled_h = int(VIRTUAL_HEIGHT * scale)
    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2
    return scale, offset_x, offset_y, scaled_w, scaled_h

def window_to_virtual(screen_pos, scale, offset_x, offset_y):
    """Translates screen pixel coordinates to virtual (800x400) coordinates."""
    if scale <= 0:
        return (0, 0)
    vx = int((screen_pos[0] - offset_x) / scale)
    vy = int((screen_pos[1] - offset_y) / scale)
    return (vx, vy)

def main():
    global window
    running = True

    while running and not engine.should_quit:
        win_w, win_h = window.get_size()
        scale, offset_x, offset_y, scaled_w, scaled_h = get_scale_and_offset(win_w, win_h)

        # Get translated virtual mouse position
        raw_mouse = pygame.mouse.get_pos()
        virtual_mouse = window_to_virtual(raw_mouse, scale, offset_x, offset_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Maximize / Window resize handling
            elif event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Keyboard shortcut for Fullscreen / Maximize toggle: F11 or Alt+Enter
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT))):
                is_fullscreen = bool(window.get_flags() & pygame.FULLSCREEN)
                if is_fullscreen:
                    window = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.RESIZABLE)
                else:
                    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            else:
                # Pass events with translated mouse coordinates
                engine.handle_event(event, mouse_pos=virtual_mouse)

        # Update game logic
        engine.handle_input()
        engine.update()

        # Render game to virtual surface
        engine.render(virtual_surface, mouse_pos=virtual_mouse)

        # Clear letterbox window background
        window.fill((15, 20, 25))

        # Scale virtual surface to fit window while preserving aspect ratio
        scaled_view = pygame.transform.smoothscale(virtual_surface, (scaled_w, scaled_h))
        window.blit(scaled_view, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
