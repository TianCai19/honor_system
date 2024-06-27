import os
import pygame
from PIL import Image
import time
import json

class HonorSystem:
    def __init__(self, thresholds, badge_dir, music_dir, data_file):
        self.thresholds = thresholds
        self.badge_dir = badge_dir
        self.music_dir = music_dir
        self.data_file = data_file

        pygame.mixer.init()

        # Load data from file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.score = data.get('score', 0)
                self.current_rank = data.get('current_rank', 0)
        else:
            self.score = 0
            self.current_rank = 0

    def save_data(self):
        data = {
            'score': self.score,
            'current_rank': self.current_rank
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def adjust_score(self, points):
        self.score += points
        self.check_for_badge()
        self.save_data()

    def check_for_badge(self):
        for i, threshold in enumerate(self.thresholds):
            if self.score >= threshold and i > self.current_rank:
                self.award_badge(i)
                self.current_rank = i
                self.save_data()

    def award_badge(self, rank):
        print(f"Congratulations! You've reached rank {rank + 1}!")
        self.display_badge_and_play_music(rank)

    def display_badge_and_play_music(self, rank):
        badge_image_path = os.path.join(self.badge_dir, f"badge{rank + 1}.png")
        badge_image = Image.open(badge_image_path)
        badge_image.show()

        music_file_path = os.path.join(self.music_dir, f"music{rank + 1}.wav")
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

# Example usage
if __name__ == "__main__":
    thresholds = [100, 200, 300]  # Example thresholds
    badge_dir = "badges"
    music_dir = "music"
    data_file = "honor_system_data.json"

    honor_system = HonorSystem(thresholds, badge_dir, music_dir, data_file)

    # Test the badge display and music play simultaneously
   # honor_system.display_badge_and_play_music(1)
    
    # Adjust the score (add or subtract points)
    honor_system.adjust_score(50)   # Adjust score by +50 points
    #honor_system.adjust_score(100)  # Adjust score by +100 points
    #honor_system.adjust_score(200)  # Adjust score by +200 points