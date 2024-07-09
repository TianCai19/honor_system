import os
import pygame
from PIL import Image
import time
import json
from tqdm import tqdm
import threading
from logger import Logger
import time
import subprocess

def activate_terminal():
    subprocess.run(["osascript", "-e", 'tell application "Terminal" to activate'])

# add llm enouragement chatbot
from encouragement_llm import show_encouragement

class HonorSystem:
    def __init__(self, thresholds, badge_dir, music_dir, data_file, log_file):
        self.thresholds = thresholds
        self.badge_dir = badge_dir
        self.music_dir = music_dir
        self.data_file = data_file
        self.logger = Logger(log_file)

        pygame.mixer.init()

        # Load data from file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.score = data.get('score', 0)
                self.current_rank = data.get('current_rank', -1)

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
        self.logger.log_score_adjustment(self.score)
        self.check_for_badge()
        self.save_data()

    def check_for_badge(self):
        for i, threshold in enumerate(self.thresholds):
            if self.score >= threshold and i > self.current_rank:
                self.award_badge(i)
                self.current_rank = i
                self.save_data()
# a new strategy for badge ,get 1 badge at 5 scores and then 10 mins after and 15 and 30 ,always
        


    def award_badge(self, rank):
        print(f"Congratulations! You've reached rank {rank + 1}! with score {self.score}")
        self.logger.log_rank(rank + 1)
        #self.display_badge_and_play_music(0)
        threading.Thread(target=show_encouragement(self.score,self.current_rank)).start()
        threading.Thread(target=activate_terminal).start()

    def display_badge_and_play_music(self, rank):
        badge_image_path = os.path.join(self.badge_dir, f"badge{rank + 1}.png")
        badge_image = Image.open(badge_image_path)
        badge_image.show()

        music_file_path = os.path.join(self.music_dir, f"music{rank + 1}.wav")
        threading.Thread(target=self.play_music, args=(music_file_path,)).start()

    def play_music(self, music_file_path):
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def adjust_score_over_time(self, duration_seconds):
        # for _ in tqdm(range(duration_seconds), desc="Adjusting Score"):
        #     self.adjust_score(1)
        #     time.sleep(1)
        while(1):
            time_for_next_rank=self.thresholds[self.current_rank+1]-self.score
            for _ in tqdm(range(time_for_next_rank), desc="Adjusting Score"):
                self.adjust_score(1)
                time.sleep(1)
            if self.current_rank==len(self.thresholds)-1:
                break

