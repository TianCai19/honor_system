import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load the music file
music_file = "music/music1.wav"

try:
    pygame.mixer.music.load(music_file)
    print(f"Playing {music_file}...")
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    print("Music playback finished.")
except pygame.error as e:
    print(f"Could not play {music_file}: {e}")