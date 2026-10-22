# Project: Real-Time Endless Runner Game (Completed & Enhanced)
**Candidate SRN:** `PES1UG24AM105`  
**Lab Assignment:** Lab 4 Vibe Coding (Individual Assignment)

---

## Completed Tasks & Architectural Fixes

### Task 1: Refined Continuous Collision Detection (CCD) & Speed Ramping
* **Bug in Starter Code**: In the initial version, collision was only checked against the obstacle's instantaneous rectangle *after* it moved. As game speed accelerated without bound, the distance jumped per frame exceeded the player's 30px width. Obstacles hopped entirely across the player's hitbox between two consecutive frames without registering a collision ("tunneling").
* **Implemented Solution**:
  1. **Continuous Swept-Box Collision**: Implemented `swept_rect()` in `Obstacle` tracking `[min(x, prev_x), max(x + w, prev_x + w)]`. If the horizontal displacement interval intersects the player during the frame and vertical clearance overlap exists, collision is reliably detected.
  2. **Bounded Speed Acceleration**: Capped speeds by difficulty level (`max_speed = 11.0` for Easy, `14.0` for Medium, `16.5` for Hard) with tuned acceleration per frame so high-speed runs stay challenging yet physically fair.

### Task 2: In-Game Game Over Screen
* **Bug in Starter Code**: The starter game abruptly froze and only printed text to the terminal console (`print("Game over! Final score:", self.score)`).
* **Implemented Solution**: Added an in-game Game Over modal overlay displaying:
  * Prominent **GAME OVER** title
  * **Final Score** and **Best Session Score**
  * Student identification: **SRN: PES1UG24AM105**
  * Interactive replay and difficulty selection menu.

### Task 3: Dynamic Replay & Difficulty System
* **Bug in Starter Code**: The game had no way to restart without manually killing and restarting Python.
* **Implemented Solution**: Clean state reset supporting difficulty selection directly on Game Over:
  * **[1] Easy**: Starting speed `5.0`, spawn interval `85 frames`, max speed `11.0`
  * **[2] Medium**: Starting speed `7.0`, spawn interval `65 frames`, max speed `14.0`
  * **[3] Hard**: Starting speed `9.0`, spawn interval `50 frames`, max speed `16.5`
  * **[SPACE / R]**: Quick restart using the current difficulty
  * **[Q / ESC]**: Graceful exit

### Task 4: Retro Sound Effects Feedback
* Generated standalone 16-bit PCM WAV sound effects via standard library `wave` and `math`:
  * **`jump.wav`**: Upward pitch chirp played on jumping
  * **`score.wav`**: Bright two-tone chime played when clearing an obstacle
  * **`hit.wav`**: Low impact thud on obstacle collision
* Managed by `SoundManager` with automatic fallback handling so execution never crashes on systems without sound devices.

### Additional Enhancements:
1. **Interactive Start Screen**:
   * Opens into an attractive Title Screen with animated runner character.
   * Prominent **[ START GAME ]** button and difficulty selectors (can click with mouse or press <kbd>Space</kbd> / <kbd>Enter</kbd>).
2. **Window Resizing & Screen Maximize**:
   * Enabled native Windows **Maximize button** on the title bar using `pygame.RESIZABLE`.
   * Preserves 800x400 aspect ratio with smooth scaling (`pygame.transform.smoothscale`) and clean letterboxing.
   * Auto-translates mouse coordinates so clicking buttons works in maximized and fullscreen mode.
   * Toggle fullscreen / maximize anytime with <kbd>F11</kbd> or <kbd>Alt</kbd> + <kbd>Enter</kbd>.

---

## Folder Structure

```
C:\LAB4_105\
├── endless-runner-original\            <-- [STARTER CODE to record Video 1]
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── game\
│       ├── game_engine.py
│       ├── obstacle.py
│       └── player.py
│
└── endless-runner-updated\             <-- [COMPLETED VERSION to record Video 2]
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── assets\
    │   └── sounds\
    │       ├── jump.wav
    │       ├── score.wav
    │       ├── hit.wav
    │       └── generate_sounds.py
    └── game\
        ├── __init__.py
        ├── game_engine.py
        ├── obstacle.py
        ├── player.py
        └── sound_manager.py
```

---

## Instructions for Videos & Evaluation

### Video 1: Before Changes (Original Code)
1. In PowerShell:
   ```powershell
   cd C:\LAB4_105\endless-runner-original
   python main.py
   ```
2. Demonstrate:
   * Game immediately drops into play without a start screen.
   * Complete silence (no jump, score, or death audio).
   * Upon hitting an obstacle, the window freezes in place with no Game Over screen and only logs to the console terminal.

### Video 2: After Changes (Updated Code)
1. In PowerShell:
   ```powershell
   cd C:\LAB4_105\endless-runner-updated
   python main.py
   ```
2. Demonstrate:
   * **Start Screen**: Shows "ENDLESS RUNNER", Candidate SRN `PES1UG24AM105`, and clickable **START GAME** button.
   * **Maximize Screen**: Click the Windows Maximize button on the title bar (or press <kbd>F11</kbd>) to show smooth full-screen scaling.
   * **Sound Effects**: Audio on jump, clearing obstacle, and impact collision.
   * **Collision Precision**: Accurate continuous collision detection.
   * **Game Over Screen**: Shows Final Score, Best Score, SRN, and replay options (<kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd>, <kbd>Space</kbd>).
