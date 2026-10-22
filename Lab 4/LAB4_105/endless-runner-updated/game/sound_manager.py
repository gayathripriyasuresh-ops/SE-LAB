import os
import pygame

class SoundManager:
    """
    Manages sound effects for the Endless Runner game.
    Initializes pygame mixer safely with fallback handling.
    """
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.enabled = True
        except Exception as e:
            print(f"[SoundManager] Audio initialization warning: {e}. Running in silent mode.")
            self.enabled = False
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_dir = os.path.abspath(os.path.join(current_dir, "..", "assets", "sounds"))

        required = ["jump.wav", "score.wav", "hit.wav"]
        missing = [name for name in required if not os.path.exists(os.path.join(sound_dir, name))]
        if missing:
            try:
                from assets.sounds.generate_sounds import generate_all_sounds
                generate_all_sounds(sound_dir)
            except Exception as e:
                print(f"[SoundManager] Could not generate sounds: {e}")

        for name in required:
            path = os.path.join(sound_dir, name)
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.65)
                    self.sounds[name] = sound
                except Exception as e:
                    print(f"[SoundManager] Error loading {name}: {e}")

    def play_jump(self):
        if self.enabled and "jump.wav" in self.sounds:
            try:
                self.sounds["jump.wav"].play()
            except Exception:
                pass

    def play_score(self):
        if self.enabled and "score.wav" in self.sounds:
            try:
                self.sounds["score.wav"].play()
            except Exception:
                pass

    def play_hit(self):
        if self.enabled and "hit.wav" in self.sounds:
            try:
                self.sounds["hit.wav"].play()
            except Exception:
                pass
